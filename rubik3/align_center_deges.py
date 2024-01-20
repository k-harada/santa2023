import numpy as np
import pandas as pd
import os
from ast import literal_eval
from sympy.combinatorics import Permutation
from itertools import combinations
from typing import Dict, List, Optional
from puzzle import Puzzle
from collections import deque

from rubik24.allowed_moves import get_allowed_moves_24


puzzle_info_df = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "../input/puzzle_info.csv"), index_col='puzzle_type'
)


def get_allowed_moves_12(puzzle_type: str):
    assert puzzle_type == "cube_3/3/3"
    n = 3
    allowed_moves_ = literal_eval(puzzle_info_df.loc[puzzle_type, 'allowed_moves'])
    allowed_moves: Dict[str, Permutation] = {k: Permutation(v) for k, v in allowed_moves_.items()}
    # to numpy
    allowed_moves_arr: Dict[str, np.array] = dict()
    for k in allowed_moves.keys():
        xxx = allowed_moves[k](np.arange(n * n * 6))
        xxx_ = np.arange(n * n * 6)[xxx]
        allowed_moves_arr[k] = xxx_
        xxx = (allowed_moves[k] ** (-1))(np.arange(n * n * 6))
        xxx_ = np.arange(n * n * 6)[xxx]
        allowed_moves_arr["-" + k] = xxx_

    return allowed_moves_arr


def _modify_path(path_left, path_right):
    path = path_left
    for m in reversed(path_right):
        if m[0] == "-":
            path.append(m[1:])
        else:
            path.append("-" + m)
    return path


def solve_bruce_12(initial_state: List[str], goal_state: List[str]):
    allowed_moves = get_allowed_moves_12("cube_3/3/3")
    assert len(initial_state) == 54

    open_set_left = deque()
    open_set_right = deque()
    closed_set_left = set()
    closed_set_right = set()

    path_dict_left = dict()
    path_dict_right = dict()
    _initial_state = "_".join(initial_state)
    _goal_state = "_".join(goal_state)

    open_set_left.append((_initial_state, []))
    open_set_right.append((_goal_state, []))
    action_list = ["r0", "-r0", "r2", "-r2", "f0", "-f0", "f2", "-f2", "d0", "-d0", "d2", "-d2"]

    while len(open_set_left):

        _current_state, path = open_set_left.popleft()
        current_state = np.array(list(_current_state.split("_")))
        # print(_current_state)
        if np.random.uniform() < 0.0001:
            print(len(closed_set_left), len(closed_set_right))
            print(_current_state)

        if _current_state == _goal_state:
            return path
        if _current_state in closed_set_left:
            continue
        if _current_state in closed_set_right:
            path_joint = _modify_path(path, path_dict_right[_current_state])
            return path_joint

        path_dict_left[_current_state] = path
        closed_set_left.add(_current_state)

        for action in action_list:
            new_state = current_state[allowed_moves[action]]
            _new_state = "_".join(new_state)
            if _new_state not in closed_set_left:
                open_set_left.append((_new_state, path + [action]))

        # right
        _current_state, path = open_set_right.popleft()
        current_state = np.array(list(_current_state.split("_")))
        # print(_current_state)
        if np.random.uniform() < 0.0001:
            print(len(closed_set_left), len(closed_set_right))

        if _current_state == _initial_state:
            path_joint = _modify_path([], path)
            return path_joint
        if _current_state in closed_set_right:
            continue
        if _current_state in closed_set_left:
            path_joint = _modify_path(path_dict_left[_current_state], path)
            return path_joint

        path_dict_right[_current_state] = path
        closed_set_right.add(_current_state)

        for action in action_list:
            new_state = current_state[allowed_moves[action]]
            _new_state = "_".join(new_state)
            if _new_state not in closed_set_right:
                open_set_right.append((_new_state, path + [action]))
    return None


if __name__ == "__main__":

    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == "cube_3/3/3"]

    for _i, _row in puzzles_df_pick.iterrows():
        _q3 = Puzzle(
            puzzle_id=_row["id"], puzzle_type="cube_3/3/3",
            solution_state=list(_row["solution_state"].split(";")),
            initial_state=list(_row["initial_state"].split(";")),
            num_wildcards=0
        )
        _initial_state = list(_row["initial_state"].split(";"))
        _goal_state = list(_row["solution_state"].split(";"))
        for i in range(54):
            if i % 9 not in [1, 3, 5, 7]:
                _initial_state[i] = "O"
                _goal_state[i] = "O"
        _path = solve_bruce_12(_initial_state, _goal_state)
        for _m in _path:
            _q3.operate(_m)
        print(_q3.state)
        print(_q3.solution_state)
