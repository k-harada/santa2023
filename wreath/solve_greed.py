import numpy as np
import pandas as pd
from itertools import combinations
from typing import Dict, List, Optional
from puzzle import Puzzle
from collections import deque

from wreath.allowed_moves import get_allowed_moves


def _modify_path(path_left, path_right):
    path = path_left
    for _m in reversed(path_right):
        if _m[0] == "-":
            path.append(_m[1:])
        else:
            path.append("-" + _m)
    return path


def solve_greed(
        initial_state: List[str], goal_state: List[str], puzzle_type: str, num_wildcards: int = 0
):
    allowed_moves = get_allowed_moves(puzzle_type)
    n = len(initial_state)

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
    if num_wildcards == 2:
        for p, q in combinations(range(n), 2):
            if initial_state[p] == initial_state[q]:
                continue
            _initial_state_2 = "_".join(initial_state[:p] + [
                initial_state[q]
            ] + initial_state[p + 1:q] + [
                initial_state[p]
            ] + initial_state[q + 1:])
            open_set_left.append((_initial_state_2, []))

    action_list = ["l", "-l", "r", "-r"]

    while len(open_set_left):

        _current_state, path = open_set_left.popleft()
        current_state = list(_current_state.split("_"))
        # print(_current_state)
        if np.random.uniform() < 0.0001:
            if len(closed_set_left) > 1000000:
                print(len(closed_set_left), len(closed_set_right))

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
            new_state = (allowed_moves[action])(current_state)
            _new_state = "_".join(new_state)
            if _new_state not in closed_set_left:
                open_set_left.append((_new_state, path + [action]))

        # right
        _current_state, path = open_set_right.popleft()
        current_state = list(_current_state.split("_"))
        # print(_current_state)
        if np.random.uniform() < 0.0001:
            if len(closed_set_left) > 1000000:
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
            new_state = (allowed_moves[action])(current_state)
            _new_state = "_".join(new_state)
            if _new_state not in closed_set_right:
                open_set_right.append((_new_state, path + [action]))
    return None


if __name__ == "__main__":
    puzzle_df = pd.read_csv("../input/puzzles.csv")
    wreath_df = puzzle_df[puzzle_df["puzzle_type"].str.slice(0, 3) == "wre"]
    # print(wreath_df)
    _id_list = []
    _moves_list = []
    for _i, _row in wreath_df.iterrows():
        puzzle_type = _row["puzzle_type"]
        if puzzle_type in ["wreath_21/21", "wreath_33/33", "wreath_100/100"]:
            continue
        _initial_state = list(_row["initial_state"].split(";"))
        _goal_state = list(_row["solution_state"].split(";"))
        _path = solve_greed(
            _initial_state, _goal_state, puzzle_type, _row["num_wildcards"]
        )
        _id_list.append(_row["id"])
        _moves_list.append(".".join(_path))
        print(_i, _row["num_wildcards"], _path)
        p = Puzzle(
            puzzle_id=_row["id"], puzzle_type=puzzle_type,
            solution_state=_goal_state, initial_state=_initial_state, num_wildcards=_row["num_wildcards"]
        )
        for m in _path:
            p.operate(m)
        wrongs = 0
        for p, q in zip(p.state, p.solution_state):
            if p != q:
                wrongs += 1
        assert wrongs <= _row["num_wildcards"]
    res_df = pd.DataFrame({"id": _id_list, "moves": _moves_list})
    res_df.to_csv("../output/wreath_small_greed.csv", index=False)
