import numpy as np
import pandas as pd
import os
from itertools import combinations
from ast import literal_eval
from typing import Dict, List, Optional
from sympy.combinatorics import Permutation
from puzzle import Puzzle
from collections import deque


puzzle_info_df = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "../input/puzzle_info.csv"), index_col='puzzle_type'
)


def _modify_path(path_left, path_right):
    path = path_left
    for m in reversed(path_right):
        if m[0] == "-":
            path.append(m[1:])
        else:
            path.append("-" + m)
    return path


def get_allowed_moves(puzzle_type: str):
    assert puzzle_type in ["cube_4/4/4", "cube_5/5/5", "cube_6/6/6"]
    if puzzle_type == "cube_4/4/4":
        n = 4
    elif puzzle_type == "cube_5/5/5":
        n = 5
    else:
        n = 6
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


def solve_bruce_all4(initial_state: List[str], goal_state: List[str]):

    # print(initial_state)
    # print(goal_state)

    allowed_moves = get_allowed_moves("cube_4/4/4")
    assert len(initial_state) == 96

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
    action_list = list(allowed_moves.keys())

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
    pass
