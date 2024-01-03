import numpy as np
import pandas as pd
import json
import kociemba
from ast import literal_eval
from typing import Dict, List
from sympy.combinatorics import Permutation
from heapq import heappop, heappush
from puzzle import Puzzle


action_list = [
    ["r0"], ["-r0"], ["r1"], ["-r1"],
    # ["f0"], ["f1"], ["f2"], ["f3"],
    ["f4"],
    # ["f5"], ["f6"], ["f7"],
]
allowed_moves: Dict[str, Permutation] = dict()
allowed_moves["r0"] = Permutation([1, 2, 3, 4, 5, 6, 7, 0, 8, 9, 10, 11, 12, 13, 14, 15])
allowed_moves["r1"] = Permutation([0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 8])
allowed_moves["f0"] = Permutation([11, 10, 9, 8, 4, 5, 6, 7, 3, 2, 1, 0, 12, 13, 14, 15])
allowed_moves["f1"] = Permutation([0, 12, 11, 10, 9, 5, 6, 7, 8, 4, 3, 2, 1, 13, 14, 15])
allowed_moves["f2"] = Permutation([0, 1, 13, 12, 11, 10, 6, 7, 8, 9, 5, 4, 3, 2, 14, 15])
allowed_moves["f3"] = Permutation([0, 1, 2, 14, 13, 12, 11, 7, 8, 9, 10, 6, 5, 4, 3, 15])
allowed_moves["f4"] = Permutation([0, 1, 2, 3, 15, 14, 13, 12, 8, 9, 10, 11, 7, 6, 5, 4])
allowed_moves["f5"] = Permutation([13, 1, 2, 3, 4, 8, 15, 14, 5, 9, 10, 11, 12, 0, 7, 6])
allowed_moves["f6"] = Permutation([15, 14, 2, 3, 4, 5, 9, 8, 7, 6, 10, 11, 12, 13, 1, 0])
allowed_moves["f7"] = Permutation([9, 8, 15, 3, 4, 5, 6, 10, 1, 0, 7, 11, 12, 13, 14, 2])

allowed_moves["-r0"] = allowed_moves["r0"] ** (-1)
allowed_moves["-r1"] = allowed_moves["r1"] ** (-1)


def heuristic(x, y, stage=0):

    sol_up = [y[0] + y[1], y[4] + y[5], y[13] + y[12]]
    sol_down = [y[8] + y[9], y[12] + y[13], y[5] + y[4]]
    res = 4
    for i in range(8):
        if x[i] + x[(i + 1) % 8] in sol_up:
            res -= 1
        if x[i + 8] + x[(i + 1) % 8 + 8] in sol_down:
            res -= 1

    if stage >= 1:
        res = res * 10 + 4
        sol_up = [y[0] + y[1] + y[2], y[4] + y[5] + y[6], y[14] + y[13] + y[12]]
        sol_down = [y[8] + y[9] + y[10], y[12] + y[13] + y[14], y[6] + y[5] + y[4]]
        for i in range(8):
            if x[i] + x[(i + 1) % 8] + x[(i + 2) % 8] in sol_up:
                res -= 1
            if x[i + 8] + x[(i + 1) % 8 + 8] + x[(i + 2) % 8 + 8] in sol_down:
                res -= 1
    if stage >= 2:
        res = res * 10 + 4
        sol_up = [y[0] + y[1] + y[2] + y[3], y[4] + y[5] + y[6] + y[7], y[15] + y[14] + y[13] + y[12]]
        sol_down = [y[8] + y[9] + y[10] + y[11], y[12] + y[13] + y[14] + y[15], y[7] + y[6] + y[5] + y[4]]
        for i in range(8):
            if x[i] + x[(i + 1) % 8] + x[(i + 2) % 8] + x[(i + 3) % 8] in sol_up:
                res -= 1
            if x[i + 8] + x[(i + 1) % 8 + 8] + x[(i + 2) % 8 + 8] + x[(i + 3) % 8 + 8] in sol_down:
                res -= 1
    return res


def solve_1x4(initial_state, goal_state, stage):
    open_set = []
    heappush(open_set, (0, initial_state, []))
    closed_set = set()

    while len(open_set):

        _, current_state, path = heappop(open_set)

        if heuristic(current_state, goal_state, stage) == 0:
            # print(current_state, path)
            return current_state, path
        # print(current_state, path, heuristic(current_state, goal_state, stage))
        if current_state == goal_state:
            return current_state, path

        closed_set.add(tuple(current_state))

        for action in action_list:
            new_state = current_state.copy()
            for move_name in action:
                move = allowed_moves[move_name]
                new_state = move(new_state)
            if tuple(new_state) not in closed_set:
                priority = len(path) + len(action) + heuristic(new_state, goal_state, stage)
                heappush(open_set, (priority, new_state, path + action))


if __name__ == "__main__":

    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_1x4 = puzzles_df[puzzles_df["puzzle_type"] == "globe_3/4"]

    # fake problems
    for _i, _row in puzzles_df_1x4.iterrows():
        _solution_state_base = list(_row["solution_state"].split(";"))
        _solution_state = _solution_state_base[:8] + _solution_state_base[-8:]
        _initial_state_base = list(_row["initial_state"].split(";"))
        _initial_state = _initial_state_base[:8] + _initial_state_base[-8:]

        _p = Puzzle(
            1000, 'globe_1/4', _solution_state,
            _initial_state, 0, True
        )
        _p.allowed_moves = allowed_moves
        print(_i, _solution_state)
        print(_initial_state)
        _state, _sol = solve_1x4(_initial_state, _solution_state, 0)
        for _m in _sol:
            _p.operate(_m)
        print(_state)
        _state, _sol = solve_1x4(_state, _solution_state, 1)
        for _m in _sol:
            _p.operate(_m)
        print(_state)
        _state, _sol = solve_1x4(_state, _solution_state, 2)
        for _m in _sol:
            _p.operate(_m)
        print(_state)
        print(_p.move_history)
