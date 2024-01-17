import numpy as np
import pandas as pd
from itertools import combinations
from typing import Dict, List, Optional
from puzzle import Puzzle
from collections import deque

from rubik24.allowed_moves import get_allowed_moves_24


def _modify_path(path_left, path_right):
    path = path_left
    for m in reversed(path_right):
        if m[0] == "-":
            path.append(m[1:])
        else:
            path.append("-" + m)
    return path


def solve_greed_41(initial_state: List[str], goal_state: List[str], two_side: bool):
    # ABAB, N1等には使えない
    allowed_moves = get_allowed_moves_24("cube_4/4/4")
    assert len(initial_state) == 24

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
    if two_side:
        action_list = list(allowed_moves.keys())
    else:
        action_list = ["r0", "-r0", "r3", "-r3", "f0", "-f0", "f3", "-f3", "d1", "-d1", "d2", "-d2"]

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


def test_phase1(initial_state, goal_state):
    path = solve_greed_41(initial_state, goal_state, two_side=True)
    print(path)

    initial_state_ext = ["O"] * (4 * 4 * 6)
    goal_state_ext = ["O"] * (4 * 4 * 6)
    for i in range(6):
        initial_state_ext[4 * 4 * i + 5] = initial_state[4 * i]
        initial_state_ext[4 * 4 * i + 6] = initial_state[4 * i + 1]
        initial_state_ext[4 * 4 * i + 9] = initial_state[4 * i + 2]
        initial_state_ext[4 * 4 * i + 10] = initial_state[4 * i + 3]
        goal_state_ext[4 * 4 * i + 5] = goal_state[4 * i]
        goal_state_ext[4 * 4 * i + 6] = goal_state[4 * i + 1]
        goal_state_ext[4 * 4 * i + 9] = goal_state[4 * i + 2]
        goal_state_ext[4 * 4 * i + 10] = goal_state[4 * i + 3]

    q4 = Puzzle(
        puzzle_id=10101, puzzle_type=f"cube_4/4/4",
        solution_state=goal_state_ext, initial_state=initial_state_ext,
        num_wildcards=0
    )
    for m in path:
        q4.operate(m)
    print(q4)
    return None


def test_phase2(initial_state, goal_state):
    path = solve_greed_41(initial_state, goal_state, two_side=False)
    print(path)

    initial_state_ext = ["O"] * (4 * 4 * 6)
    goal_state_ext = ["O"] * (4 * 4 * 6)
    for i in range(6):
        initial_state_ext[4 * 4 * i + 5] = initial_state[4 * i]
        initial_state_ext[4 * 4 * i + 6] = initial_state[4 * i + 1]
        initial_state_ext[4 * 4 * i + 9] = initial_state[4 * i + 2]
        initial_state_ext[4 * 4 * i + 10] = initial_state[4 * i + 3]
        goal_state_ext[4 * 4 * i + 5] = goal_state[4 * i]
        goal_state_ext[4 * 4 * i + 6] = goal_state[4 * i + 1]
        goal_state_ext[4 * 4 * i + 9] = goal_state[4 * i + 2]
        goal_state_ext[4 * 4 * i + 10] = goal_state[4 * i + 3]

    q4 = Puzzle(
        puzzle_id=10101, puzzle_type=f"cube_4/4/4",
        solution_state=goal_state_ext, initial_state=initial_state_ext,
        num_wildcards=0
    )
    for m in path:
        q4.operate(m)
    print(q4)
    return None


if __name__ == "__main__":
    np.random.seed(3)
    _initial_state = ["U", "U", "U", "U"] + ["X"] * 16 + ["D", "D", "D", "D"]
    _goal_state = ["U", "U", "U", "U"] + ["X"] * 16 + ["D", "D", "D", "D"]
    np.random.shuffle(_initial_state)
    _initial_state = list(_initial_state)
    test_phase1(_initial_state, _goal_state)

    _initial_state = ["F"] * 4 + ["R"] * 4 + ["B"] * 4 + ["L"] * 4
    np.random.shuffle(_initial_state)
    _initial_state = ["U", "U", "U", "U"] + list(_initial_state) + ["D", "D", "D", "D"]
    _goal_state = ["U", "U", "U", "U"] + ["F"] * 4 + ["R"] * 4 + ["B"] * 4 + ["L"] * 4 + ["D", "D", "D", "D"]
    test_phase2(_initial_state, _goal_state)

    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == "cube_4/4/4"]

    for _i, _row in puzzles_df_pick.iterrows():
        _q4 = Puzzle(
            puzzle_id=_row["id"], puzzle_type="cube_4/4/4",
            solution_state=list(_row["solution_state"].split(";")),
            initial_state=list(_row["initial_state"].split(";")),
            num_wildcards=0
        )
        _initial_state = list(_row["initial_state"].split(";"))
        _goal_state = list(_row["solution_state"].split(";"))
        if _goal_state[0] != _goal_state[1]:
            continue
        _initial_state_pick = []
        _goal_state_pick = []
        for _j in range(6):
            _initial_state_pick.append(_q4.state[4 * 4 * _j + 5])
            _initial_state_pick.append(_q4.state[4 * 4 * _j + 6])
            _initial_state_pick.append(_q4.state[4 * 4 * _j + 9])
            _initial_state_pick.append(_q4.state[4 * 4 * _j + 10])
            if _j in [0, 5]:
                _goal_state_pick.append(_goal_state[4 * 4 * _j + 5])
                _goal_state_pick.append(_goal_state[4 * 4 * _j + 6])
                _goal_state_pick.append(_goal_state[4 * 4 * _j + 9])
                _goal_state_pick.append(_goal_state[4 * 4 * _j + 10])
            else:
                _goal_state_pick = _goal_state_pick + ["X"] * 4
        _initial_state_pick_mask = []
        for _x in _initial_state_pick:
            if _x in _goal_state_pick:
                _initial_state_pick_mask.append(_x)
            else:
                _initial_state_pick_mask.append("X")
        print(_initial_state_pick_mask)
        print(_goal_state_pick)
        _path = solve_greed_41(_initial_state_pick_mask, _goal_state_pick, two_side=True)
        for _m in _path:
            _q4.operate(_m)

        _initial_state_pick = []
        _goal_state_pick = []
        for _j in range(6):
            _initial_state_pick.append(_q4.state[4 * 4 * _j + 5])
            _initial_state_pick.append(_q4.state[4 * 4 * _j + 6])
            _initial_state_pick.append(_q4.state[4 * 4 * _j + 9])
            _initial_state_pick.append(_q4.state[4 * 4 * _j + 10])
            _goal_state_pick.append(_goal_state[4 * 4 * _j + 5])
            _goal_state_pick.append(_goal_state[4 * 4 * _j + 6])
            _goal_state_pick.append(_goal_state[4 * 4 * _j + 9])
            _goal_state_pick.append(_goal_state[4 * 4 * _j + 10])

        _path = solve_greed_41(_initial_state_pick, _goal_state_pick, two_side=False)
        for _m in _path:
            _q4.operate(_m)
        print(_q4.state)
