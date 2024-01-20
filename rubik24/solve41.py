import numpy as np
import pandas as pd
from typing import List
from puzzle import Puzzle
from heapq import heappop, heappush
from collections import deque

from rubik24.compress_magic412 import compress_magic


def _modify_path(path_left, path_right):
    path = path_left
    for m in reversed(path_right):
        if m[0] == "-":
            path.append(m[1:])
        else:
            path.append("-" + m)
    return path


def heuristic(current_state: np.array, goal_state: np.array, two_side: bool = False):
    h = 0
    for i in range(24):
        x, y = current_state[i], goal_state[i]
        if x != y:
            h += 1
            if (i < 4 or i >= 20) and two_side:
                h += 10000
            elif (i < 8 or i >= 26) and two_side:
                h += 100
    # print(current_state, goal_state, h)
    return h * 10


def solve_greed_41(initial_state: List[str], goal_state: List[str], two_side: bool = True, first: bool = False):

    assert len(initial_state) == 24

    open_set_left = []
    open_set_right = deque()
    closed_set_left = set()
    closed_set_right = set()

    path_dict_left = dict()
    path_dict_right = dict()
    _initial_state = "_".join(initial_state)
    _goal_state = "_".join(goal_state)
    goal_state_arr = np.array(goal_state)
    print("initial:", _initial_state)
    print("goal:", _goal_state)

    heappush(open_set_left, (0, _initial_state, []))
    open_set_right.append((0, _goal_state, []))
    arr_dict, command_dict = compress_magic(first=first)

    if not first:
        magic_list = []
        for k in arr_dict.keys():
            if len(command_dict[k]) > 1:
                magic_list.append(k)
    else:
        magic_list = list(arr_dict.keys())
    magic_list_right = []
    for k in magic_list:
        if len(command_dict[k]) == 1:
            magic_list_right.append(k)
    # print("hogege", magic_list_right)

    while len(open_set_left):

        _, _current_state, path = heappop(open_set_left)
        current_state = np.array(list(_current_state.split("_")))
        # print(_current_state)
        if np.random.uniform() < 0.001:
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
            new_state = current_state[arr_dict[magic]]
            _new_state = "_".join(new_state)
            if _new_state not in closed_set_left:
                h = heuristic(new_state, goal_state_arr, two_side)
                priority = len(path) + len(command_dict[magic]) + h
                heappush(open_set_left, (priority, _new_state, path + command_dict[magic]))

        # right
        if len(open_set_right):
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

            for magic in magic_list_right:
                new_state = current_state[arr_dict[magic]]
                _new_state = "_".join(new_state)
                if _new_state not in closed_set_right:
                    priority = len(path) + len(command_dict[magic])
                    open_set_right.append((priority, _new_state, path + command_dict[magic]))

    return None


def test_41(initial_state, goal_state):
    path = solve_greed_41(initial_state, goal_state, True)
    print(path)
    n = 4

    initial_state_ext = ["O"] * (n * n * 6)
    goal_state_ext = ["O"] * (n * n * 6)
    for i in range(6):
        initial_state_ext[n * n * i + 5] = initial_state[4 * i]
        initial_state_ext[n * n * i + 6] = initial_state[4 * i + 1]
        initial_state_ext[n * n * i + 9] = initial_state[4 * i + 2]
        initial_state_ext[n * n * i + 10] = initial_state[4 * i + 3]
        goal_state_ext[n * n * i + 5] = goal_state[4 * i]
        goal_state_ext[n * n * i + 6] = goal_state[4 * i + 1]
        goal_state_ext[n * n * i + 9] = goal_state[4 * i + 2]
        goal_state_ext[n * n * i + 10] = goal_state[4 * i + 3]

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
    _initial_state = ["U", "U", "U", "U"] + ["F"] * 4 + ["R"] * 4 + ["B"] * 4 + ["L"] * 4 + ["D", "D", "D", "D"]
    np.random.shuffle(_initial_state)
    _initial_state = list(_initial_state)
    _goal_state = ["U", "U", "U", "U"] + ["F"] * 4 + ["R"] * 4 + ["B"] * 4 + ["L"] * 4 + ["D", "D", "D", "D"]
    test_41(_initial_state, _goal_state)

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

        _initial_state_pick = []
        _goal_state_pick = []
        for _j in range(6):
            _initial_state_pick.append(_q4.state[_n * _n * _j + 5])
            _initial_state_pick.append(_q4.state[_n * _n * _j + 6])
            _initial_state_pick.append(_q4.state[_n * _n * _j + 9])
            _initial_state_pick.append(_q4.state[_n * _n * _j + 10])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 5])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 6])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 9])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 10])

        _path = solve_greed_41(_initial_state_pick, _goal_state_pick, first=True)
        for _m in _path:
            _q4.operate(_m)
        print(len(_path))
        print(_q4.state)
