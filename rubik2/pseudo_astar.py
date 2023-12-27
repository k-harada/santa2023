from sympy.combinatorics import Permutation
from ast import literal_eval
from typing import Dict, List
from collections import deque

from heapq import heappop, heappush
import numpy as np
import pandas as pd


puzzle_info_df = pd.read_csv('../input/puzzle_info.csv', index_col='puzzle_type')
puzzles_df = pd.read_csv('../input/puzzles.csv')

allowed_moves_ = literal_eval(puzzle_info_df.loc['cube_2/2/2', 'allowed_moves'])
allowed_moves: Dict[str, Permutation] = dict()
for k, v_ in allowed_moves_.items():
    v = Permutation(v_)
    allowed_moves[k] = v
    allowed_moves["-" + k] = v ** (-1)


def heuristic(x, y):
    return sum(s != g for s, g in zip(x, y))


def a_star_search(initial_state, goal_state):
    open_set = []
    heappush(open_set, (0, initial_state, []))
    closed_set = set()

    while len(open_set):

        _, current_state, path = heappop(open_set)

        if current_state == goal_state:
            return path

        closed_set.add(tuple(current_state))

        for move_name, move in allowed_moves.items():
            new_state = move(current_state)
            if tuple(new_state) not in closed_set:
                priority = len(path) + 1 + heuristic(new_state, goal_state)
                heappush(open_set, (priority, new_state, path + [move_name]))


if __name__ == "__main__":
    puzzles_df_2x2 = puzzles_df[puzzles_df["puzzle_type"] == "cube_2/2/2"]
    _id_list = []
    _moves_list = []
    for _i, _row in puzzles_df_2x2.iterrows():
        _initial_state = list(_row["initial_state"].split(";"))
        _goal_state = list(_row["solution_state"].split(";"))
        print(_row)
        res = a_star_search(_initial_state, _goal_state)
        _id_list.append(_i)
        _moves_list.append(".".join(res))
    pd.DataFrame({"id": _id_list, "moves": _moves_list}).to_csv(
        "../output/solve_2x2_pseudo_astar_1227.csv", index=False
    )

