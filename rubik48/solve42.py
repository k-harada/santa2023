import numpy as np
import pandas as pd
from typing import List
from puzzle import Puzzle
from heapq import heappop, heappush
from collections import deque

from rubik48.compress_magic42 import compress_magic
from rubik24.solve41 import solve_greed_41  # for test
from rubik48.solve_bruce_all4 import solve_bruce_all4
from rubik48.magic4X_edge import magic44
from rubik48.solve4X import solve_greed_4x


def _modify_path(path_left, path_right):
    path = path_left
    for m in reversed(path_right):
        if m[0] == "-":
            path.append(m[1:])
        else:
            path.append("-" + m)
    return path


def map_pair(x: np.array):
    res_list = [
        [x[0], x[25], x[1], x[24]], [x[6], x[7], x[8], x[9]],
        [x[4], x[32], x[5], x[33]], [x[7], x[17], x[11], x[16]],
        [x[10], x[35], x[12], x[37]], [x[11], x[18], x[13], x[20]],
        [x[19], x[26], x[21], x[28]], [x[27], x[34], x[29], x[36]],
        [x[14], x[40], x[15], x[41]], [x[38], x[44], x[39], x[42]],
        [x[22], x[43], x[23], x[45]], [x[46], x[0], x[47], x[1]],
    ]
    res = ["_".join(list(sorted(xx))) for xx in res_list]
    return res


def heuristic(current_state: np.array, goal_state: np.array, two_side: bool = False):
    h = 0
    # cur_st = map_pair(current_state)
    # goal_st = map_pair(goal_state)
    for i in range(48):
        x, y = current_state[i], goal_state[i]
        if two_side:
            if x != y:
                h += 1
        else:
            if x != y:
                if i not in [0, 1, 6, 7, 8, 9, 24, 25]:
                    h += 10
                else:
                    h += 1
    # print(h)
    return h * 100


def heuristic_pair(current_state: np.array, goal_state: np.array, two_side: bool = False):
    h = 0
    cur_st = map_pair(current_state)
    goal_st = map_pair(goal_state)
    if two_side:
        for i, x in enumerate(cur_st):
            if x not in goal_st:
                h += 4
    else:
        for i, x in enumerate(cur_st):
            if x not in goal_st:
                if i not in [0, 1]:
                    h += 40
                else:
                    h += 4
    # print(h)
    return h * 100


def solve_greed_42(initial_state: List[str], goal_state: List[str], two_side: bool = True, first: bool = False):

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
    # print("initial:", _initial_state)
    # print("goal:", _goal_state)

    heappush(open_set_left, (0, _initial_state, []))
    open_set_right.append((0, _goal_state, []))
    arr_dict, command_dict = compress_magic()
    magic_list = list(arr_dict.keys())
    magic_list_right = []
    for k in magic_list:
        if len(command_dict[k]) == 1:
            magic_list_right.append(k)
    # print(magic_list_right)

    while len(open_set_left):

        _, _current_state, path = heappop(open_set_left)
        current_state = np.array(list(_current_state.split("_")))
        # print(_current_state)
        h_now = heuristic(current_state, goal_state_arr, two_side)
        if np.random.uniform() < 0.001:
            print(len(closed_set_left), len(closed_set_right))
            print(h_now)
            print(_current_state)

        if h_now <= 800:
            # print(h_now)
            return path

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


def test_40(q4: Puzzle):
    assert q4.puzzle_type == "cube_4/4/4"
    initial_state_pick = []
    goal_state_pick = []
    n = 4
    for j in range(6):
        initial_state_pick.append(q4.state[n * n * j + 5])
        initial_state_pick.append(q4.state[n * n * j + 6])
        initial_state_pick.append(q4.state[n * n * j + 9])
        initial_state_pick.append(q4.state[n * n * j + 10])
        goal_state_pick.append(q4.solution_state[n * n * j + 5])
        goal_state_pick.append(q4.solution_state[n * n * j + 6])
        goal_state_pick.append(q4.solution_state[n * n * j + 9])
        goal_state_pick.append(q4.solution_state[n * n * j + 10])
    path = solve_greed_41(initial_state_pick, goal_state_pick, True, True)
    for m in path:
        q4.operate(m)
    return q4


def test_41(q4: Puzzle):
    assert q4.puzzle_type == "cube_4/4/4"
    initial_state_pick = []
    goal_state_pick = []
    n = 4
    for j in range(6):
        initial_state_pick.append(q4.state[n * n * j + 1])
        initial_state_pick.append(q4.state[n * n * j + 2])
        initial_state_pick.append(q4.state[n * n * j + 4])
        initial_state_pick.append(q4.state[n * n * j + 7])
        initial_state_pick.append(q4.state[n * n * j + 8])
        initial_state_pick.append(q4.state[n * n * j + 11])
        initial_state_pick.append(q4.state[n * n * j + 13])
        initial_state_pick.append(q4.state[n * n * j + 14])
        goal_state_pick.append(q4.solution_state[n * n * j + 1])
        goal_state_pick.append(q4.solution_state[n * n * j + 2])
        goal_state_pick.append(q4.solution_state[n * n * j + 4])
        goal_state_pick.append(q4.solution_state[n * n * j + 7])
        goal_state_pick.append(q4.solution_state[n * n * j + 8])
        goal_state_pick.append(q4.solution_state[n * n * j + 11])
        goal_state_pick.append(q4.solution_state[n * n * j + 13])
        goal_state_pick.append(q4.solution_state[n * n * j + 14])
    # 4箇所以外を揃える
    path = solve_greed_42(initial_state_pick, goal_state_pick, True)
    for m in path:
        q4.operate(m)
    print(q4.state)
    initial_state_pick = []
    for j in range(6):
        initial_state_pick.append(q4.state[n * n * j + 1])
        initial_state_pick.append(q4.state[n * n * j + 2])
        initial_state_pick.append(q4.state[n * n * j + 4])
        initial_state_pick.append(q4.state[n * n * j + 7])
        initial_state_pick.append(q4.state[n * n * j + 8])
        initial_state_pick.append(q4.state[n * n * j + 11])
        initial_state_pick.append(q4.state[n * n * j + 13])
        initial_state_pick.append(q4.state[n * n * j + 14])
    path = solve_greed_42(initial_state_pick, goal_state_pick, False)
    for m in path:
        q4.operate(m)

    return q4


def test_42(q4: Puzzle):
    assert q4.puzzle_type == "cube_4/4/4"
    initial_state_pick = []
    goal_state_pick = []
    n = 4
    for j in range(6):
        initial_state_pick.append(q4.state[n * n * j + 1])
        initial_state_pick.append(q4.state[n * n * j + 2])
        initial_state_pick.append(q4.state[n * n * j + 4])
        initial_state_pick.append(q4.state[n * n * j + 7])
        initial_state_pick.append(q4.state[n * n * j + 8])
        initial_state_pick.append(q4.state[n * n * j + 11])
        initial_state_pick.append(q4.state[n * n * j + 13])
        initial_state_pick.append(q4.state[n * n * j + 14])
        goal_state_pick.append(q4.solution_state[n * n * j + 1])
        goal_state_pick.append(q4.solution_state[n * n * j + 2])
        goal_state_pick.append(q4.solution_state[n * n * j + 4])
        goal_state_pick.append(q4.solution_state[n * n * j + 7])
        goal_state_pick.append(q4.solution_state[n * n * j + 8])
        goal_state_pick.append(q4.solution_state[n * n * j + 11])
        goal_state_pick.append(q4.solution_state[n * n * j + 13])
        goal_state_pick.append(q4.solution_state[n * n * j + 14])

    path = solve_greed_4x(initial_state_pick, goal_state_pick)
    for m in path:
        q4.operate(m)
    return q4


if __name__ == "__main__":
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
        print("initial:", _initial_state)
        print("goal:", _goal_state)

        _q4 = test_40(_q4)
        # print(_q4.state)
        _q4 = test_41(_q4)
        # print(_q4.state)
        _q4 = test_42(_q4)
        print("solved edge:", _i, "length:", len(_q4.move_history))
        print(_q4.state)
