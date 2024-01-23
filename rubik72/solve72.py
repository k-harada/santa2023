import numpy as np
import pandas as pd
from typing import List
from puzzle import Puzzle
from heapq import heappop, heappush
from collections import deque

from rubik72.solve52 import solve_greed_52, test_51
from rubik72.solve5X import solve_greed_5x


def align_pair_edges_with_center(initial_state: List[str], goal_state: List[str], named: bool = False):
    n = 5
    initial_state_dummy = ["O"] * 150
    goal_state_dummy = ["O"] * 150
    for j in range(6):
        initial_state_dummy[n * n * j + 1] = initial_state[12 * j + 0]
        initial_state_dummy[n * n * j + 2] = initial_state[12 * j + 1]
        initial_state_dummy[n * n * j + 3] = initial_state[12 * j + 2]
        initial_state_dummy[n * n * j + 5] = initial_state[12 * j + 3]
        initial_state_dummy[n * n * j + 9] = initial_state[12 * j + 4]
        initial_state_dummy[n * n * j + 10] = initial_state[12 * j + 5]
        initial_state_dummy[n * n * j + 14] = initial_state[12 * j + 6]
        initial_state_dummy[n * n * j + 15] = initial_state[12 * j + 7]
        initial_state_dummy[n * n * j + 19] = initial_state[12 * j + 8]
        initial_state_dummy[n * n * j + 21] = initial_state[12 * j + 9]
        initial_state_dummy[n * n * j + 22] = initial_state[12 * j + 10]
        initial_state_dummy[n * n * j + 23] = initial_state[12 * j + 11]

        goal_state_dummy[n * n * j + 1] = goal_state[12 * j + 0]
        goal_state_dummy[n * n * j + 2] = goal_state[12 * j + 1]
        goal_state_dummy[n * n * j + 3] = goal_state[12 * j + 2]
        goal_state_dummy[n * n * j + 5] = goal_state[12 * j + 3]
        goal_state_dummy[n * n * j + 9] = goal_state[12 * j + 4]
        goal_state_dummy[n * n * j + 10] = goal_state[12 * j + 5]
        goal_state_dummy[n * n * j + 14] = goal_state[12 * j + 6]
        goal_state_dummy[n * n * j + 15] = goal_state[12 * j + 7]
        goal_state_dummy[n * n * j + 19] = goal_state[12 * j + 8]
        goal_state_dummy[n * n * j + 21] = goal_state[12 * j + 9]
        goal_state_dummy[n * n * j + 22] = goal_state[12 * j + 10]
        goal_state_dummy[n * n * j + 23] = goal_state[12 * j + 11]

    q5 = Puzzle(
        puzzle_id=4444, puzzle_type=f"cube_{n}/{n}/{n}",
        solution_state=goal_state_dummy,
        initial_state=initial_state_dummy,
        num_wildcards=0
    )
    # 4箇所以外を揃える
    if named:
        initial_state_mod = []
        for a in initial_state:
            if a in goal_state[0:12]:
                initial_state_mod.append("A")
            elif a in goal_state[12:24]:
                initial_state_mod.append("B")
            elif a in goal_state[24:36]:
                initial_state_mod.append("C")
            elif a in goal_state[36:48]:
                initial_state_mod.append("D")
            elif a in goal_state[48:60]:
                initial_state_mod.append("E")
            else:
                initial_state_mod.append("F")
        goal_state_mod = ["A"] * 12 + ["B"] * 12 + ["C"] * 12 + ["D"] * 12 + ["E"] * 12 + ["F"] * 12
        print(initial_state_mod)
        print(goal_state_mod)
        path = solve_greed_52(initial_state_mod, goal_state_mod, True)
    else:
        path = solve_greed_52(initial_state, goal_state, True)

    for m in path:
        q5.operate(m)
    # print(q5.state)
    initial_state_pick = []
    for j in range(6):
        initial_state_pick.append(q5.state[n * n * j + 1])
        initial_state_pick.append(q5.state[n * n * j + 2])
        initial_state_pick.append(q5.state[n * n * j + 3])
        initial_state_pick.append(q5.state[n * n * j + 5])
        initial_state_pick.append(q5.state[n * n * j + 9])
        initial_state_pick.append(q5.state[n * n * j + 10])
        initial_state_pick.append(q5.state[n * n * j + 14])
        initial_state_pick.append(q5.state[n * n * j + 15])
        initial_state_pick.append(q5.state[n * n * j + 19])
        initial_state_pick.append(q5.state[n * n * j + 21])
        initial_state_pick.append(q5.state[n * n * j + 22])
        initial_state_pick.append(q5.state[n * n * j + 23])

    if named:
        initial_state_pick_mod = []
        for a in initial_state_pick:
            if a in goal_state[0:12]:
                initial_state_pick_mod.append("A")
            elif a in goal_state[12:24]:
                initial_state_pick_mod.append("B")
            elif a in goal_state[24:36]:
                initial_state_pick_mod.append("C")
            elif a in goal_state[36:48]:
                initial_state_pick_mod.append("D")
            elif a in goal_state[48:60]:
                initial_state_pick_mod.append("E")
            else:
                initial_state_pick_mod.append("F")

        goal_state_mod = ["A"] * 12 + ["B"] * 12 + ["C"] * 12 + ["D"] * 12 + ["E"] * 12 + ["F"] * 12
        path = solve_greed_52(initial_state_pick_mod, goal_state_mod, False)
    else:
        path = solve_greed_52(initial_state_pick, goal_state, False)

    for m in path:
        q5.operate(m)

    print(q5.state)
    print(q5.solution_state)

    initial_state_pick = []
    for j in range(6):
        initial_state_pick.append(q5.state[n * n * j + 1])
        initial_state_pick.append(q5.state[n * n * j + 2])
        initial_state_pick.append(q5.state[n * n * j + 3])
        initial_state_pick.append(q5.state[n * n * j + 5])
        initial_state_pick.append(q5.state[n * n * j + 9])
        initial_state_pick.append(q5.state[n * n * j + 10])
        initial_state_pick.append(q5.state[n * n * j + 14])
        initial_state_pick.append(q5.state[n * n * j + 15])
        initial_state_pick.append(q5.state[n * n * j + 19])
        initial_state_pick.append(q5.state[n * n * j + 21])
        initial_state_pick.append(q5.state[n * n * j + 22])
        initial_state_pick.append(q5.state[n * n * j + 23])
    if named:
        initial_state_pick_mod = []
        for a in initial_state_pick:
            if a in goal_state[0:12]:
                initial_state_pick_mod.append("A")
            elif a in goal_state[12:24]:
                initial_state_pick_mod.append("B")
            elif a in goal_state[24:36]:
                initial_state_pick_mod.append("C")
            elif a in goal_state[36:48]:
                initial_state_pick_mod.append("D")
            elif a in goal_state[48:60]:
                initial_state_pick_mod.append("E")
            else:
                initial_state_pick_mod.append("F")

        goal_state_mod = ["A"] * 12 + ["B"] * 12 + ["C"] * 12 + ["D"] * 12 + ["E"] * 12 + ["F"] * 12
        path = solve_greed_5x(initial_state_pick_mod, goal_state_mod)
    else:
        path = solve_greed_5x(initial_state_pick, goal_state)
    for m in path:
        q5.operate(m)
    print(q5.state)
    return q5.move_history


if __name__ == "__main__":
    _n = 5
    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == f"cube_{_n}/{_n}/{_n}"]

    for _i, _row in puzzles_df_pick.iterrows():
        _q5 = Puzzle(
            puzzle_id=_row["id"], puzzle_type=f"cube_{_n}/{_n}/{_n}",
            solution_state=list(_row["solution_state"].split(";")),
            initial_state=list(_row["initial_state"].split(";")),
            num_wildcards=0
        )
        _initial_state = list(_row["initial_state"].split(";"))
        _goal_state = list(_row["solution_state"].split(";"))
        print("initial:", _initial_state)
        print("goal:", _goal_state)

        _initial_state_pick = []
        _goal_state_pick = []
        for _j in range(6):
            _initial_state_pick.append(_q5.state[_n * _n * _j + 1])
            _initial_state_pick.append(_q5.state[_n * _n * _j + 2])
            _initial_state_pick.append(_q5.state[_n * _n * _j + 3])
            _initial_state_pick.append(_q5.state[_n * _n * _j + 5])
            _initial_state_pick.append(_q5.state[_n * _n * _j + 9])
            _initial_state_pick.append(_q5.state[_n * _n * _j + 10])
            _initial_state_pick.append(_q5.state[_n * _n * _j + 14])
            _initial_state_pick.append(_q5.state[_n * _n * _j + 15])
            _initial_state_pick.append(_q5.state[_n * _n * _j + 19])
            _initial_state_pick.append(_q5.state[_n * _n * _j + 21])
            _initial_state_pick.append(_q5.state[_n * _n * _j + 22])
            _initial_state_pick.append(_q5.state[_n * _n * _j + 23])
            _goal_state_pick.append(_q5.solution_state[_n * _n * _j + 1])
            _goal_state_pick.append(_q5.solution_state[_n * _n * _j + 2])
            _goal_state_pick.append(_q5.solution_state[_n * _n * _j + 3])
            _goal_state_pick.append(_q5.solution_state[_n * _n * _j + 5])
            _goal_state_pick.append(_q5.solution_state[_n * _n * _j + 9])
            _goal_state_pick.append(_q5.solution_state[_n * _n * _j + 10])
            _goal_state_pick.append(_q5.solution_state[_n * _n * _j + 14])
            _goal_state_pick.append(_q5.solution_state[_n * _n * _j + 15])
            _goal_state_pick.append(_q5.solution_state[_n * _n * _j + 19])
            _goal_state_pick.append(_q5.solution_state[_n * _n * _j + 21])
            _goal_state_pick.append(_q5.solution_state[_n * _n * _j + 22])
            _goal_state_pick.append(_q5.solution_state[_n * _n * _j + 23])

        _path = align_pair_edges_with_center(_initial_state_pick, _goal_state_pick)
        for _m in _path:
            _q5.operate(_m)
        print("solved edge:", _i, "length:", len(_path))
        print(_q5.state)
