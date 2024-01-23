import numpy as np
import pandas as pd
from typing import List
from puzzle import Puzzle
from heapq import heappop, heappush
from collections import deque
from rubik72.magic5X import compress_magic


def _modify_path(path_left, path_right):
    path = path_left
    for m in reversed(path_right):
        if m[0] == "-":
            path.append(m[1:])
        else:
            path.append("-" + m)
    return path


def heuristic(current_state: np.array, goal_state: np.array):
    return 0


def goal_surrogate(goal_state: List[str]):
    assert len(goal_state) == 72
    goal_state_surrogate_1 = goal_state.copy()
    goal_state_surrogate_1[0] = goal_state[14]
    goal_state_surrogate_1[1] = goal_state[13]
    goal_state_surrogate_1[2] = goal_state[12]
    goal_state_surrogate_1[9] = goal_state[38]
    goal_state_surrogate_1[10] = goal_state[37]
    goal_state_surrogate_1[11] = goal_state[36]
    goal_state_surrogate_1[12] = goal_state[2]
    goal_state_surrogate_1[13] = goal_state[1]
    goal_state_surrogate_1[14] = goal_state[0]
    goal_state_surrogate_1[36] = goal_state[11]
    goal_state_surrogate_1[37] = goal_state[10]
    goal_state_surrogate_1[38] = goal_state[9]
    goal_state_surrogate_2 = goal_state.copy()
    goal_state_surrogate_3 = goal_state_surrogate_1.copy()
    goal_state_surrogate_2[0] = goal_state[38]
    goal_state_surrogate_2[1] = goal_state[37]
    goal_state_surrogate_2[2] = goal_state[36]
    goal_state_surrogate_2[9] = goal_state[12]
    goal_state_surrogate_2[10] = goal_state[13]
    goal_state_surrogate_2[11] = goal_state[14]
    goal_state_surrogate_2[12] = goal_state[9]
    goal_state_surrogate_2[13] = goal_state[10]
    goal_state_surrogate_2[14] = goal_state[11]
    goal_state_surrogate_2[36] = goal_state[2]
    goal_state_surrogate_2[37] = goal_state[1]
    goal_state_surrogate_2[38] = goal_state[0]

    goal_state_surrogate_3[0] = goal_state_surrogate_1[38]
    goal_state_surrogate_3[1] = goal_state_surrogate_1[37]
    goal_state_surrogate_3[2] = goal_state_surrogate_1[36]
    goal_state_surrogate_3[9] = goal_state_surrogate_1[12]
    goal_state_surrogate_3[10] = goal_state_surrogate_1[13]
    goal_state_surrogate_3[11] = goal_state_surrogate_1[14]
    goal_state_surrogate_3[12] = goal_state_surrogate_1[9]
    goal_state_surrogate_3[13] = goal_state_surrogate_1[10]
    goal_state_surrogate_3[14] = goal_state_surrogate_1[11]
    goal_state_surrogate_3[36] = goal_state_surrogate_1[2]
    goal_state_surrogate_3[37] = goal_state_surrogate_1[1]
    goal_state_surrogate_3[38] = goal_state_surrogate_1[0]

    return goal_state_surrogate_1, goal_state_surrogate_2, goal_state_surrogate_3


def solve_greed_5x(initial_state: List[str], goal_state: List[str]):

    assert len(initial_state) == 72

    open_set_left = []
    open_set_right = deque()
    closed_set_left = set()
    closed_set_right = set()

    path_dict_left = dict()
    path_dict_right = dict()

    goal_state_surrogate_1, goal_state_surrogate_2, goal_state_surrogate_3 = goal_surrogate(goal_state)
    _initial_state = "_".join(initial_state)
    _goal_state = "_".join(goal_state)
    _goal_state_surrogate_1 = "_".join(goal_state_surrogate_1)
    _goal_state_surrogate_2 = "_".join(goal_state_surrogate_2)
    _goal_state_surrogate_3 = "_".join(goal_state_surrogate_3)
    goal_state_arr = np.array(goal_state)
    print("initial:", _initial_state)
    print("goal:", _goal_state)

    heappush(open_set_left, (0, _initial_state, []))
    open_set_right.append((0, _goal_state, []))
    closed_set_right.add(_goal_state_surrogate_1)
    path_dict_right[_goal_state_surrogate_1] = []
    closed_set_right.add(_goal_state_surrogate_2)
    path_dict_right[_goal_state_surrogate_2] = []
    closed_set_right.add(_goal_state_surrogate_3)
    path_dict_right[_goal_state_surrogate_3] = []

    arr_dict, command_dict = compress_magic()
    magic_list = list(arr_dict.keys())
    magic_list_right = []

    while len(open_set_left):

        _, _current_state, path = heappop(open_set_left)
        current_state = np.array(list(_current_state.split("_")))
        # print(_current_state)
        h_now = heuristic(current_state, goal_state_arr)
        if np.random.uniform() < 0.001:
            print(len(closed_set_left), len(closed_set_right))
            print(h_now)
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
                h = heuristic(new_state, goal_state_arr)
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


if __name__ == "__main__":
    _n = 5
    _initial_state_all = ['B', 'D', 'D', 'A', 'D', 'A', 'B', 'E', 'D', 'A', 'A', 'B', 'F', 'F', 'A', 'A', 'E', 'D', 'A', 'A', 'B', 'B', 'B', 'A', 'B', 'A', 'A', 'A', 'D', 'A', 'B', 'B', 'C', 'B', 'B', 'B', 'D', 'B', 'C', 'B', 'B', 'E', 'E', 'A', 'B', 'C', 'B', 'B', 'B', 'B', 'E', 'C', 'C', 'C', 'A', 'C', 'F', 'E', 'F', 'C', 'C', 'E', 'E', 'D', 'C', 'C', 'F', 'A', 'A', 'C', 'F', 'C', 'C', 'C', 'D', 'C', 'B', 'A', 'A', 'F', 'D', 'C', 'D', 'E', 'D', 'D', 'C', 'D', 'F', 'D', 'D', 'C', 'B', 'F', 'D', 'A', 'D', 'D', 'D', 'D', 'C', 'E', 'E', 'E', 'C', 'E', 'B', 'C', 'D', 'E', 'E', 'A', 'C', 'B', 'E', 'E', 'E', 'B', 'C', 'E', 'E', 'E', 'E', 'E', 'F', 'D', 'F', 'F', 'F', 'E', 'F', 'D', 'A', 'D', 'F', 'F', 'F', 'A', 'F', 'F', 'F', 'C', 'A', 'A', 'F', 'F', 'F', 'F', 'F', 'E']
    _goal_state_all = ["A"] * 25 + ["B"] * 25 + ["C"] * 25 + ["D"] * 25 + ["E"] * 25 + ["F"] * 25
    _initial_state = []
    _goal_state = []
    for _j in range(6):
        _initial_state.append(_initial_state_all[_n * _n * _j + 1])
        _initial_state.append(_initial_state_all[_n * _n * _j + 2])
        _initial_state.append(_initial_state_all[_n * _n * _j + 3])
        _initial_state.append(_initial_state_all[_n * _n * _j + 5])
        _initial_state.append(_initial_state_all[_n * _n * _j + 9])
        _initial_state.append(_initial_state_all[_n * _n * _j + 10])
        _initial_state.append(_initial_state_all[_n * _n * _j + 14])
        _initial_state.append(_initial_state_all[_n * _n * _j + 15])
        _initial_state.append(_initial_state_all[_n * _n * _j + 19])
        _initial_state.append(_initial_state_all[_n * _n * _j + 21])
        _initial_state.append(_initial_state_all[_n * _n * _j + 22])
        _initial_state.append(_initial_state_all[_n * _n * _j + 23])
        _goal_state.append(_goal_state_all[_n * _n * _j + 1])
        _goal_state.append(_goal_state_all[_n * _n * _j + 2])
        _goal_state.append(_goal_state_all[_n * _n * _j + 3])
        _goal_state.append(_goal_state_all[_n * _n * _j + 5])
        _goal_state.append(_goal_state_all[_n * _n * _j + 9])
        _goal_state.append(_goal_state_all[_n * _n * _j + 10])
        _goal_state.append(_goal_state_all[_n * _n * _j + 14])
        _goal_state.append(_goal_state_all[_n * _n * _j + 15])
        _goal_state.append(_goal_state_all[_n * _n * _j + 19])
        _goal_state.append(_goal_state_all[_n * _n * _j + 21])
        _goal_state.append(_goal_state_all[_n * _n * _j + 22])
        _goal_state.append(_goal_state_all[_n * _n * _j + 23])
    # print(solve_greed_5x(_initial_state, _goal_state))
    _initial_state = ["N2", "N1", "N0"] + [
        f"N{i}" for i in range(3, 9)
    ] + ["N11", "N10", "N9"] + ["N14", "N13", "N12"] + [
        f"N{i}" for i in range(15, 36)
    ] + ["N38", "N37", "N36"] + [f"N{i}" for i in range(39, 72)]
    _goal_state = [f"N{i}" for i in range(72)]
    print(solve_greed_5x(_initial_state, _goal_state))
