import numpy as np
import pandas as pd
from itertools import combinations
from typing import Dict, List, Optional
from puzzle import Puzzle
from heapq import heappop, heappush
from collections import deque

from rubik24.allowed_moves import get_allowed_moves_24
from rubik_abstract.magic51 import magic51


def _modify_path(path_left, path_right):
    path = path_left
    for m in reversed(path_right):
        if m[0] == "-":
            path.append(m[1:])
        else:
            path.append("-" + m)
    return path


def heuristic(current_state: np.array, goal_state: np.array):
    h = 0
    for x, y in zip(current_state, goal_state):
        if x != y:
            h += 1
    # print(current_state, goal_state, h)
    return h * 1000


def solve_greed_51(initial_state: List[str], goal_state: List[str], puzzle_type: str, two_side: bool):

    allowed_moves_arr = get_allowed_moves_24(puzzle_type)
    assert len(initial_state) == 24
    n = 5
    open_set_left = deque()
    open_set_right = deque()
    closed_set_left = set()
    closed_set_right = set()

    path_dict_left = dict()
    path_dict_right = dict()
    _initial_state = "_".join(initial_state)
    _goal_state = "_".join(goal_state)
    goal_state_arr = np.array(goal_state)
    print(_initial_state)
    print(_goal_state)

    open_set_left.append((0, _initial_state, []))
    open_set_right.append((0, _goal_state, []))
    action_list = ["r0", "-r0", "r4", "-r4", "f0", "-f0", "f4", "-f4", "d0", "-d0", "d4", "-d4"]
    if two_side:
        # magic_list = [[a] for a in action_list]
        magic_list = []
        for d1 in ["d", "r", "f"]:
            for d2 in ["d", "r", "f"]:
                if d1 == d2:
                    continue
                for flag_int in range(4):
                    magic_list.append(magic51(2, 3, 5, d1, d2, flag_int, False))
                    magic_list.append(magic51(2, 3, 5, d1, d2, flag_int, True))
                    magic_list.append(magic51(3, 2, 5, d1, d2, flag_int, False))
                    magic_list.append(magic51(3, 2, 5, d1, d2, flag_int, True))
                    magic_list.append(magic51(2, 1, 5, d1, d2, flag_int, False))
                    magic_list.append(magic51(2, 1, 5, d1, d2, flag_int, True))
                    magic_list.append(magic51(1, 2, 5, d1, d2, flag_int, False))
                    magic_list.append(magic51(1, 2, 5, d1, d2, flag_int, True))
    else:
        # magic_list = [[a] for a in action_list]
        magic_list = []
        for d1 in ["d"]:
            for d2 in ["d", "r", "f"]:
                if d1 == d2:
                    continue
                for flag_int in range(4):
                    magic_list.append(magic51(2, 3, 5, d1, d2, flag_int, False))
                    magic_list.append(magic51(2, 3, 5, d1, d2, flag_int, True))
                    magic_list.append(magic51(3, 2, 5, d1, d2, flag_int, False))
                    magic_list.append(magic51(3, 2, 5, d1, d2, flag_int, True))
                    magic_list.append(magic51(2, 1, 5, d1, d2, flag_int, False))
                    magic_list.append(magic51(2, 1, 5, d1, d2, flag_int, True))
                    magic_list.append(magic51(1, 2, 5, d1, d2, flag_int, False))
                    magic_list.append(magic51(1, 2, 5, d1, d2, flag_int, True))
    print(len(magic_list))
    while len(open_set_left):

        _, _current_state, path = open_set_left.popleft()
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

        for magic in magic_list:
            new_state = current_state.copy()
            for action in magic:
                new_state = new_state[allowed_moves_arr[action]]
            _new_state = "_".join(new_state)
            if _new_state not in closed_set_left:
                priority = len(path) + len(magic)
                open_set_left.append((priority, _new_state, path + magic))

        # right
        _, _current_state, path = open_set_right.popleft()
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

        for magic in magic_list:
            new_state = current_state.copy()
            for action in magic:
                new_state = new_state[allowed_moves_arr[action]]
            h = heuristic(new_state, goal_state_arr)
            _new_state = "_".join(new_state)
            if _new_state not in closed_set_right:
                priority = len(path) + len(magic) + h
                open_set_right.append((priority, _new_state, path + magic))

    return None


def test_phase1(initial_state, goal_state):
    path = solve_greed_51(initial_state, goal_state, "cube_5/5/5", two_side=True)
    print(path)

    initial_state_ext = ["O"] * (5 * 5 * 6)
    goal_state_ext = ["O"] * (5 * 5 * 6)
    for i in range(6):
        initial_state_ext[5 * 5 * i + 7] = initial_state[4 * i]
        initial_state_ext[5 * 5 * i + 11] = initial_state[4 * i + 1]
        initial_state_ext[5 * 5 * i + 13] = initial_state[4 * i + 2]
        initial_state_ext[5 * 5 * i + 17] = initial_state[4 * i + 3]
        goal_state_ext[5 * 5 * i + 7] = goal_state[4 * i]
        goal_state_ext[5 * 5 * i + 11] = goal_state[4 * i + 1]
        goal_state_ext[5 * 5 * i + 13] = goal_state[4 * i + 2]
        goal_state_ext[5 * 5 * i + 17] = goal_state[4 * i + 3]

    q5 = Puzzle(
        puzzle_id=10101, puzzle_type=f"cube_5/5/5",
        solution_state=goal_state_ext, initial_state=initial_state_ext,
        num_wildcards=0
    )
    for m in path:
        q5.operate(m)
    print(q5)
    return None


def test_phase2(initial_state, goal_state):
    path = solve_greed_51(initial_state, goal_state, "cube_5/5/5", two_side=False)
    print(path)

    initial_state_ext = ["O"] * (5 * 5 * 6)
    goal_state_ext = ["O"] * (5 * 5 * 6)
    for i in range(6):
        initial_state_ext[5 * 5 * i + 7] = initial_state[4 * i]
        initial_state_ext[5 * 5 * i + 11] = initial_state[4 * i + 1]
        initial_state_ext[5 * 5 * i + 13] = initial_state[4 * i + 2]
        initial_state_ext[5 * 5 * i + 17] = initial_state[4 * i + 3]
        goal_state_ext[5 * 5 * i + 7] = goal_state[4 * i]
        goal_state_ext[5 * 5 * i + 11] = goal_state[4 * i + 1]
        goal_state_ext[5 * 5 * i + 13] = goal_state[4 * i + 2]
        goal_state_ext[5 * 5 * i + 17] = goal_state[4 * i + 3]

    q5 = Puzzle(
        puzzle_id=10101, puzzle_type=f"cube_5/5/5",
        solution_state=goal_state_ext, initial_state=initial_state_ext,
        num_wildcards=0
    )
    for m in path:
        q5.operate(m)
    print(q5)
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
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == "cube_5/5/5"]

    for _i, _row in puzzles_df_pick.iterrows():
        _q5 = Puzzle(
            puzzle_id=_row["id"], puzzle_type="cube_5/5/5",
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
            _initial_state_pick.append(_q5.state[5 * 5 * _j + 7])
            _initial_state_pick.append(_q5.state[5 * 5 * _j + 11])
            _initial_state_pick.append(_q5.state[5 * 5 * _j + 13])
            _initial_state_pick.append(_q5.state[5 * 5 * _j + 17])
            if _j in [0, 5]:
                _goal_state_pick.append(_goal_state[5 * 5 * _j + 7])
                _goal_state_pick.append(_goal_state[5 * 5 * _j + 11])
                _goal_state_pick.append(_goal_state[5 * 5 * _j + 13])
                _goal_state_pick.append(_goal_state[5 * 5 * _j + 17])
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
        _path = solve_greed_51(_initial_state_pick_mask, _goal_state_pick, "cube_5/5/5", two_side=True)
        for _m in _path:
            _q5.operate(_m)

        _initial_state_pick = []
        _goal_state_pick = []
        for _j in range(6):
            _initial_state_pick.append(_q5.state[5 * 5 * _j + 7])
            _initial_state_pick.append(_q5.state[5 * 5 * _j + 11])
            _initial_state_pick.append(_q5.state[5 * 5 * _j + 13])
            _initial_state_pick.append(_q5.state[5 * 5 * _j + 17])
            _goal_state_pick.append(_goal_state[5 * 5 * _j + 7])
            _goal_state_pick.append(_goal_state[5 * 5 * _j + 11])
            _goal_state_pick.append(_goal_state[5 * 5 * _j + 13])
            _goal_state_pick.append(_goal_state[5 * 5 * _j + 17])

        _path = solve_greed_51(_initial_state_pick, _goal_state_pick, "cube_5/5/5", two_side=False)
        for _m in _path:
            _q5.operate(_m)
        print(_q5.state)