import numpy as np
import pandas as pd
from typing import List
from puzzle import Puzzle
from heapq import heappop, heappush
from collections import deque

from rubik48.solve42 import solve_greed_42, test_40
from rubik48.solve4X import solve_greed_4x


def align_pair_edges(initial_state: List[str], goal_state: List[str]):
    n = 4
    initial_state_dummy = ["O"] * 96
    goal_state_dummy = ["O"] * 96
    for j in range(6):
        initial_state_dummy[n * n * j + 1] = initial_state[8 * j + 0]
        initial_state_dummy[n * n * j + 2] = initial_state[8 * j + 1]
        initial_state_dummy[n * n * j + 4] = initial_state[8 * j + 2]
        initial_state_dummy[n * n * j + 7] = initial_state[8 * j + 3]
        initial_state_dummy[n * n * j + 8] = initial_state[8 * j + 4]
        initial_state_dummy[n * n * j + 11] = initial_state[8 * j + 5]
        initial_state_dummy[n * n * j + 13] = initial_state[8 * j + 6]
        initial_state_dummy[n * n * j + 14] = initial_state[8 * j + 7]
        goal_state_dummy[n * n * j + 1] = goal_state[8 * j + 0]
        goal_state_dummy[n * n * j + 2] = goal_state[8 * j + 1]
        goal_state_dummy[n * n * j + 4] = goal_state[8 * j + 2]
        goal_state_dummy[n * n * j + 7] = goal_state[8 * j + 3]
        goal_state_dummy[n * n * j + 8] = goal_state[8 * j + 4]
        goal_state_dummy[n * n * j + 11] = goal_state[8 * j + 5]
        goal_state_dummy[n * n * j + 13] = goal_state[8 * j + 6]
        goal_state_dummy[n * n * j + 14] = goal_state[8 * j + 7]

    q4 = Puzzle(
        puzzle_id=4444, puzzle_type=f"cube_{n}/{n}/{n}",
        solution_state=goal_state_dummy,
        initial_state=initial_state_dummy,
        num_wildcards=0
    )
    # 4箇所以外を揃える
    path = solve_greed_42(initial_state, goal_state, True)
    for m in path:
        q4.operate(m)
    # print(q4.state)
    initial_state_pick = []
    for j in range(6):
        initial_state_pick.append(q4.state[n * n * j + 1])
        initial_state_pick.append(q4.state[n * n * j + 2])
        initial_state_pick.append(q4.state[n * n * j + 4])
        initial_state_pick.append(q4.state[n * n * j + 7])
        initial_state_pick.append(q4.state[n * n * j + 8])
        initial_state_pick.append(q4.state[n * n * j + 11])
        initial_state_pick.append(q4.state[n * n * j + 13])
        initial_state_pick.append(q4.state[n * n * j + 14])
    path = solve_greed_42(initial_state_pick, goal_state, False)
    for m in path:
        q4.operate(m)

    initial_state_pick = []
    for j in range(6):
        initial_state_pick.append(q4.state[n * n * j + 1])
        initial_state_pick.append(q4.state[n * n * j + 2])
        initial_state_pick.append(q4.state[n * n * j + 4])
        initial_state_pick.append(q4.state[n * n * j + 7])
        initial_state_pick.append(q4.state[n * n * j + 8])
        initial_state_pick.append(q4.state[n * n * j + 11])
        initial_state_pick.append(q4.state[n * n * j + 13])
        initial_state_pick.append(q4.state[n * n * j + 14])

    path = solve_greed_4x(initial_state_pick, goal_state)
    for m in path:
        q4.operate(m)
    print(q4.state)
    return q4.move_history


if __name__ == "__main__":
    _n = 4
    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == f"cube_{_n}/{_n}/{_n}"]

    for _i, _row in puzzles_df_pick.iterrows():
        _q4 = Puzzle(
            puzzle_id=_row["id"], puzzle_type=f"cube_{_n}/{_n}/{_n}",
            solution_state=list(_row["solution_state"].split(";")),
            initial_state=list(_row["initial_state"].split(";")),
            num_wildcards=0
        )
        _initial_state = list(_row["initial_state"].split(";"))
        _goal_state = list(_row["solution_state"].split(";"))
        print("initial:", _initial_state)
        print("goal:", _goal_state)

        _q4 = test_40(_q4)
        _initial_state_pick = []
        _goal_state_pick = []
        for _j in range(6):
            _initial_state_pick.append(_q4.state[_n * _n * _j + 1])
            _initial_state_pick.append(_q4.state[_n * _n * _j + 2])
            _initial_state_pick.append(_q4.state[_n * _n * _j + 4])
            _initial_state_pick.append(_q4.state[_n * _n * _j + 7])
            _initial_state_pick.append(_q4.state[_n * _n * _j + 8])
            _initial_state_pick.append(_q4.state[_n * _n * _j + 11])
            _initial_state_pick.append(_q4.state[_n * _n * _j + 13])
            _initial_state_pick.append(_q4.state[_n * _n * _j + 14])
            _goal_state_pick.append(_q4.solution_state[_n * _n * _j + 1])
            _goal_state_pick.append(_q4.solution_state[_n * _n * _j + 2])
            _goal_state_pick.append(_q4.solution_state[_n * _n * _j + 4])
            _goal_state_pick.append(_q4.solution_state[_n * _n * _j + 7])
            _goal_state_pick.append(_q4.solution_state[_n * _n * _j + 8])
            _goal_state_pick.append(_q4.solution_state[_n * _n * _j + 11])
            _goal_state_pick.append(_q4.solution_state[_n * _n * _j + 13])
            _goal_state_pick.append(_q4.solution_state[_n * _n * _j + 14])

        _path = align_pair_edges(_initial_state_pick, _goal_state_pick)
        for _m in _path:
            _q4.operate(_m)
        print("solved edge:", _i, "length:", len(_path))
        print(_q4.state)
