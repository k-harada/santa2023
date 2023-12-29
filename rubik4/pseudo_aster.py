from sympy.combinatorics import Permutation
from ast import literal_eval
from typing import Dict, List
from collections import deque

from heapq import heappop, heappush
import numpy as np
import pandas as pd


puzzle_info_df = pd.read_csv('../input/puzzle_info.csv', index_col='puzzle_type')
puzzles_df = pd.read_csv('../input/puzzles.csv')

allowed_moves_ = literal_eval(puzzle_info_df.loc['cube_4/4/4', 'allowed_moves'])
allowed_moves: Dict[str, Permutation] = dict()
for k, v_ in allowed_moves_.items():
    v = Permutation(v_)
    allowed_moves[k] = v
    allowed_moves["-" + k] = v ** (-1)
    print(k, v)

action_list = [[], []]
# stage 0
for k in allowed_moves.keys():
    action_list[0].append([k])
# stage 1
action_list[1] = [
    ["d0"], ["-d0"],
]
action_list[1].append(["r1", "d0", "-r1"])
action_list[1].append(["r1", "d0", "d0", "-r1"])
action_list[1].append(["r1", "-d0", "-r1"])

action_list[1].append(["-r1", "d0", "r1"])
action_list[1].append(["-r1", "d0", "d0", "r1"])
action_list[1].append(["-r1", "-d0", "r1"])

action_list[1].append(["r2", "d0", "-r2"])
action_list[1].append(["r2", "d0", "d0", "-r2"])
action_list[1].append(["r2", "-d0", "-r2"])

action_list[1].append(["r2", "d0", "-r2"])
action_list[1].append(["-r2", "d0", "d0", "r2"])
action_list[1].append(["-r2", "-d0", "r2"])

action_list[1].append(["f1", "d0", "-f1"])
action_list[1].append(["f1", "d0", "d0", "-f1"])
action_list[1].append(["f1", "-d0", "-f1"])

action_list[1].append(["-f1", "d0", "f1"])
action_list[1].append(["-f1", "d0", "d0", "f1"])
action_list[1].append(["-f1", "-d0", "f1"])

action_list[1].append(["f2", "d0", "-f2"])
action_list[1].append(["f2", "d0", "d0", "-f2"])
action_list[1].append(["f2", "-d0", "-f2"])

action_list[1].append(["-f2", "d0", "f2"])
action_list[1].append(["-f2", "d0", "d0", "f2"])
action_list[1].append(["-f2", "-d0", "f2"])


def heuristic(x, y, stage):
    res = 0
    if stage == 0:
        for i in range(96):
            if x[i] != y[i] and i in [5, 6, 9, 10]:
                res += 1
    elif stage == 1:
        for i in range(96):
            if x[i] != y[i] and i in [5, 6, 9, 10, 85, 86, 89, 90]:
                res += 1
    return res


def a_star_search(initial_state, goal_state, stage):
    open_set = []
    heappush(open_set, (0, initial_state, []))
    closed_set = set()

    while len(open_set):

        _, current_state, path = heappop(open_set)

        if heuristic(current_state, goal_state, stage) == 0:
            return current_state, path

        closed_set.add(tuple(current_state))

        for action in action_list[stage]:
            new_state = current_state.copy()
            for move_name in action:
                move = allowed_moves[move_name]
                new_state = move(new_state)
            if tuple(new_state) not in closed_set:
                priority = len(path) + 1 + heuristic(new_state, goal_state, stage)
                heappush(open_set, (priority, new_state, path + action))


if __name__ == "__main__":
    puzzles_df_4x4 = puzzles_df[puzzles_df["puzzle_type"] == "cube_4/4/4"]
    _id_list = []
    _moves_list = []
    for _i, _row in puzzles_df_4x4.iterrows():
        _initial_state = list(_row["initial_state"].split(";"))
        _goal_state = list(_row["solution_state"].split(";"))
        print(_row)
        _state, _path = a_star_search(_initial_state, _goal_state, stage=0)
        print(_path)
        _state, _path = a_star_search(_state, _goal_state, stage=1)
        print(_path)
        print(_state)
        _id_list.append(_i)
        _moves_list.append(".".join(_path))



