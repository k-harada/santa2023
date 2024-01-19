import numpy as np
import pandas as pd
from typing import List
from puzzle import Puzzle
from heapq import heappop, heappush
from collections import deque
from rubik48.magic4X_edge import compress_magic


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


def solve_greed_4x(initial_state: List[str], goal_state: List[str]):

    assert len(initial_state) == 48

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
    _n = 4
    _initial_state_all = ['N15', 'N14', 'N2', 'N60', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'N10', 'N11', 'N28', 'N13', 'N1', 'N31', 'N80', 'N17', 'N50', 'N83', 'N20', 'N21', 'N22', 'N23', 'N24', 'N25', 'N26', 'N27', 'N35', 'N29', 'N30', 'N0', 'N44', 'N33', 'N34', 'N47', 'N36', 'N37', 'N38', 'N39', 'N40', 'N41', 'N42', 'N43', 'N64', 'N45', 'N46', 'N76', 'N95', 'N49', 'N18', 'N19', 'N52', 'N53', 'N54', 'N55', 'N56', 'N57', 'N58', 'N59', 'N92', 'N61', 'N62', 'N67', 'N32', 'N65', 'N66', 'N79', 'N68', 'N69', 'N70', 'N71', 'N72', 'N73', 'N74', 'N75', 'N12', 'N77', 'N78', 'N48', 'N3', 'N81', 'N82', 'N51', 'N84', 'N85', 'N86', 'N87', 'N88', 'N89', 'N90', 'N91', 'N16', 'N93', 'N94', 'N63']
    _goal_state_all = [f"N{_i}" for _i in range(96)]
    _initial_state = []
    _goal_state = []
    for _j in range(6):
        _initial_state.append(_initial_state_all[_n * _n * _j + 1])
        _initial_state.append(_initial_state_all[_n * _n * _j + 2])
        _initial_state.append(_initial_state_all[_n * _n * _j + 4])
        _initial_state.append(_initial_state_all[_n * _n * _j + 7])
        _initial_state.append(_initial_state_all[_n * _n * _j + 8])
        _initial_state.append(_initial_state_all[_n * _n * _j + 11])
        _initial_state.append(_initial_state_all[_n * _n * _j + 13])
        _initial_state.append(_initial_state_all[_n * _n * _j + 14])
        _goal_state.append(_goal_state_all[_n * _n * _j + 1])
        _goal_state.append(_goal_state_all[_n * _n * _j + 2])
        _goal_state.append(_goal_state_all[_n * _n * _j + 4])
        _goal_state.append(_goal_state_all[_n * _n * _j + 7])
        _goal_state.append(_goal_state_all[_n * _n * _j + 8])
        _goal_state.append(_goal_state_all[_n * _n * _j + 11])
        _goal_state.append(_goal_state_all[_n * _n * _j + 13])
        _goal_state.append(_goal_state_all[_n * _n * _j + 14])
    print(solve_greed_4x(_initial_state, _goal_state))
