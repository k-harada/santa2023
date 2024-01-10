from typing import Dict, List, Optional
from heapq import heappop, heappush

import numpy as np
from sympy.combinatorics import Permutation

from puzzle import Puzzle


def solve_greed(initial_state: np.array, goal_state: np.array):
    n = len(initial_state) // 4
    assert len(initial_state) % 4 == 0
    assert len(initial_state) == len(goal_state)
    _initial_state = "".join(initial_state)
    _goal_state = "".join(goal_state)

    allowed_moves: Dict[str, Permutation] = dict()
    allowed_moves["r0"] = Permutation(list(range(1, 2 * n)) + [0] + list(range(2 * n, 4 * n)))
    allowed_moves["-r0"] = allowed_moves["r0"] ** (-1)
    allowed_moves["r1"] = Permutation(list(range(2 * n)) + list(range(2 * n + 1, 4 * n)) + [2 * n])
    allowed_moves["-r1"] = allowed_moves["r1"] ** (-1)
    allowed_moves["f0"] = Permutation(
        list(range(3 * n - 1, 2 * n - 1, -1)) + list(
            range(n, 2 * n)
        ) + list(range(n - 1, -1, -1)) + list(range(3 * n, 4 * n))
    )
    for i in range(1, 2 * n):
        allowed_moves[f"f{i}"] = allowed_moves["-r0"] * allowed_moves["-r1"] * allowed_moves[f"f{i - 1}"] * allowed_moves["r0"] * allowed_moves["r1"]

    open_set = []
    open_set_right = []
    closed_set = set()
    closed_set_right = set()

    path_dict = dict()
    path_dict_right = dict()

    heappush(open_set, (0, _initial_state, []))
    heappush(open_set_right, (0, _goal_state, []))
    action_list = ["r0", "-r0", "r1", "-r1", f"f{n}"]
    allowed_moves_arr: Dict[str, np.array] = dict()
    for k in allowed_moves.keys():
        xxx = allowed_moves[k](np.arange(4 * n))
        allowed_moves_arr[k] = np.arange(4 * n)[xxx]
    # print(allowed_moves_arr)

    while len(open_set):

        _, _current_state, path = heappop(open_set)
        current_state = np.array(list(_current_state))
        path_dict[_current_state] = path
        # print(_current_state)
        if np.random.uniform() < 0.0001:
            print(len(closed_set), len(closed_set_right))

        if _current_state == _goal_state:
            return path, []
        if _current_state in closed_set:
            continue
        if _current_state in closed_set_right:
            return path, path_dict_right[_current_state]
        closed_set.add(_current_state)

        for action in action_list:
            new_state = current_state[allowed_moves_arr[action]]
            _new_state = "".join(new_state)
            if _new_state not in closed_set:
                priority = len(path) + 1
                heappush(open_set, (priority, _new_state, path + [action]))

        # right
        _, _current_state, path = heappop(open_set_right)
        current_state = np.array(list(_current_state))
        path_dict_right[_current_state] = path
        # print(_current_state)
        if np.random.uniform() < 0.0001:
            print(len(closed_set), len(closed_set_right))

        if _current_state == _initial_state:
            return [], path
        if _current_state in closed_set_right:
            continue
        if _current_state in closed_set:
            return path_dict[_current_state], path
        closed_set_right.add(_current_state)

        for action in action_list:
            new_state = current_state[allowed_moves_arr[action]]
            _new_state = "".join(new_state)
            if _new_state not in closed_set_right:
                priority = len(path) + 1
                heappush(open_set_right, (priority, _new_state, path + [action]))
    return None, None




if __name__ == "__main__":

    _sol_left, _sol_right = solve_greed(
        np.array([
            "0", "1", "2", "5", "4", "3", "6", "7",
            "8", "9", "C", "B", "A", "D", "E", "F"
        ]),
        np.array([
            "0", "1", "2", "3", "4", "5", "6", "7",
            "8", "9", "A", "B", "C", "D", "E", "F"
        ]),
    )

    _sol = _sol_left
    for _m in reversed(_sol_right):
        if _m[0] == "f":
            _sol.append(_m)
        elif _m[0] == "-":
            _sol.append(_m[1:])
        else:
            _sol.append("-" + _m)
    print(_sol)
    k = 2
    # _sol = ['f4', '-r0'] + ['-r1'] * k + ['f4', 'r0', '-r1', 'f4'] + ['r1'] * (k + 1) + ['f4']
    _sol = ['f4'] + ['r1'] * k + ['f4']

    _p = Puzzle(9999, "globe_3/33",
                [str(_i) for _i in range(66*4)],
                [str(_i) for _i in range(66*4)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f33")
        elif _m == "r1":
            _p.operate("r3")
        elif _m == "-r1":
            _p.operate("-r3")
        else:
            _p.operate(_m)
    print("f33", _p)
    print("f33", [str(_i) for _i in range(66*4)])

    _p = Puzzle(9999, "globe_1/8",
                [str(_i) for _i in range(32)],
                [str(_i) for _i in range(32)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f8")
        else:
            _p.operate(_m)
    print("f8", _p)

    _p = Puzzle(9999, "globe_1/8",
                [str(_i) for _i in range(32)],
                [str(_i) for _i in range(32)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f2")
        else:
            _p.operate(_m)
    print("f2", _p)

    _p = Puzzle(9999, "globe_1/8",
                [str(_i) for _i in range(32)],
                [str(_i) for _i in range(32)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f0")
        else:
            _p.operate(_m)
    print("f0", _p)

    _p = Puzzle(9999, "globe_1/8",
                [str(_i) for _i in range(32)],
                [str(_i) for _i in range(32)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f4")
        else:
            _p.operate(_m)
    print("f4", _p)

    _p = Puzzle(9999, "globe_1/16",
                [str(_i) for _i in range(64)],
                [str(_i) for _i in range(64)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f16")
        else:
            _p.operate(_m)
    print(_p)
    _p = Puzzle(9999, "globe_1/16",
                [str(_i) for _i in range(64)],
                [str(_i) for _i in range(64)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f2")
        else:
            _p.operate(_m)
    print(_p)

    _state, _sol = solve_greed(
        ["0", "1", "2", "7", "4", "5", "6", "3"],
        ["0", "1", "2", "3", "4", "5", "6", "7"]
    )
    print(_state)
    print(_sol)

    for _ in range(10):
        # fake problems
        _solution_state = [str(_i) for _i in range(8)]
        _xx = np.array(_solution_state)
        np.random.shuffle(_xx)

        _state, _sol = solve_greed(list(_xx), _solution_state)
        print(_state)
        print(_sol)
