import numpy as np
from itertools import permutations
from typing import Dict, List, Optional
from dataclasses import dataclass
from sympy.combinatorics import Permutation
from heapq import heappop, heappush
from puzzle import Puzzle


def heuristic(x, y, stage=0):
    # BFS
    return 0


def solve_greed(
        initial_state: List[List[int]], goal_state: List[List[int]], length_list: Optional[List[int]] = None,
        r_0: int = 0, r_1: int = 0
):
    assert len(initial_state) == len(goal_state) == 2
    assert list(sorted(initial_state[0] + initial_state[1])) == list(sorted(goal_state[0] + goal_state[1]))
    if length_list is None:
        length_list = [1] * (max(initial_state[0] + initial_state[1]) + 1)
    assert sum([length_list[p] for p in initial_state[0]]) == sum([length_list[p] for p in initial_state[1]])
    assert sum([length_list[p] for p in goal_state[0]]) == sum([length_list[p] for p in goal_state[1]])
    assert sum([length_list[p] for p in initial_state[0]]) == sum([length_list[p] for p in goal_state[0]])

    assert sum([length_list[p] for p in initial_state[0]]) % 2 == 0
    n = sum([length_list[p] for p in initial_state[0]]) // 2

    open_set = []
    # right-right
    heappush(open_set, (0, initial_state, ["r0"] * r_0 + ["r1"] * r_1))
    # left-right
    new_state = [[initial_state[0][-1]] + initial_state[0][:-1], initial_state[1]]
    c = length_list[initial_state[0][-1]]
    if c > r_0:
        heappush(open_set, (0, new_state, ["-r0"] * (c - r_0) + ["r1"] * r_1))
    else:
        heappush(open_set, (0, new_state, ["r0"] * (r_0 - c) + ["r1"] * r_1))
    # right-left
    new_state = [initial_state[0], [initial_state[1][-1]] + initial_state[1][:-1]]
    c = length_list[initial_state[1][-1]]
    if c > r_1:
        heappush(open_set, (0, new_state, ["-r1"] * (c - r_1) + ["r0"] * r_0))
    else:
        heappush(open_set, (0, new_state, ["r1"] * (r_1 - c) + ["r0"] * r_0))
    # left-left
    new_state = [[initial_state[0][-1]] + initial_state[0][:-1], [initial_state[1][-1]] + initial_state[1][:-1]]
    c_0 = length_list[initial_state[0][-1]]
    c_1 = length_list[initial_state[1][-1]]
    if c_0 > r_0:
        if c_1 > r_1:
            heappush(open_set, (0, new_state, ["-r0"] * (c_0 - r_0) + ["-r1"] * (c_1 - r_1)))
        else:
            heappush(open_set, (0, new_state, ["-r0"] * (c_0 - r_0) + ["r1"] * (r_1 - c_1)))
    else:
        if c_1 > r_1:
            heappush(open_set, (0, new_state, ["r0"] * (r_0 - c_0) + ["-r1"] * (c_1 - r_1)))
        else:
            heappush(open_set, (0, new_state, ["r0"] * (r_0 - c_0) + ["r1"] * (r_1 - c_1)))

    closed_set = set()

    while len(open_set):

        _, current_state, path = heappop(open_set)

        if current_state == goal_state:
            return current_state, path

        closed_set.add(tuple(current_state[0] + current_state[1]))

        # r0
        new_state = current_state.copy()
        action = ["r0"] * length_list[new_state[0][0]]
        new_state[0] = new_state[0][1:] + [new_state[0][0]]
        if tuple(new_state[0] + new_state[1]) not in closed_set:
            priority = len(path) + len(action) + heuristic(new_state, goal_state)
            heappush(open_set, (priority, new_state, path + action))

        # -r0
        new_state = current_state.copy()
        action = ["-r0"] * length_list[new_state[0][-1]]
        new_state[0] = [new_state[0][-1]] + new_state[0][:-1]
        if tuple(new_state[0] + new_state[1]) not in closed_set:
            priority = len(path) + len(action) + heuristic(new_state, goal_state)
            heappush(open_set, (priority, new_state, path + action))

        # r1
        new_state = current_state.copy()
        action = ["r1"] * length_list[new_state[1][0]]
        new_state[1] = new_state[1][1:] + [new_state[1][0]]
        if tuple(new_state[0] + new_state[1]) not in closed_set:
            priority = len(path) + len(action) + heuristic(new_state, goal_state)
            heappush(open_set, (priority, new_state, path + action))

        # -r1
        new_state = current_state.copy()
        action = ["-r1"] * length_list[new_state[1][-1]]
        new_state[1] = [new_state[1][-1]] + new_state[1][:-1]
        if tuple(new_state[0] + new_state[1]) not in closed_set:
            priority = len(path) + len(action) + heuristic(new_state, goal_state)
            heappush(open_set, (priority, new_state, path + action))

        # fn
        up_total = 0
        i_up = -1
        for i, a in enumerate(current_state[0]):
            up_total += length_list[a]
            if up_total == n:
                i_up = i + 1
        down_total = 0
        i_down = -1
        for i, a in enumerate(current_state[1]):
            down_total += length_list[a]
            if down_total == n:
                i_down = i + 1
        if i_up > 0 and i_down > 0:
            new_state = [
                current_state[0][:i_up] + list(reversed(current_state[1][i_down:])),
                current_state[1][:i_down] + list(reversed(current_state[0][i_up:]))
            ]
            action = [f"f{n}"]
            if tuple(new_state[0] + new_state[1]) not in closed_set:
                priority = len(path) + len(action) + heuristic(new_state, goal_state)
                heappush(open_set, (priority, new_state, path + action))
    return None, None


if __name__ == "__main__":
    # 解けないケースを探す
    _initial_state = [[0, 1, 2, 5, 3, 4], [6, 7, 8, 9, 10, 11]]
    _solution_state = [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]]
    print(_initial_state)

    _state, _sol = solve_greed(_initial_state, _solution_state)
    print(_state)
    print(_sol)

    # fake problems
    _solution_state = [[0, 1, 2, 3, 3], [4, 5, 6, 7, 7]]
    _xx = np.array([0, 1, 2, 3, 3, 4, 5, 6, 7, 7])
    _n = 7
    _length_list = [_n, 1, _n - 1, 1, _n, 1, _n - 1, 1, 1]
    while True:
        np.random.shuffle(_xx)
        _initial_state = [list(_xx[:4]), list(_xx[4:])]
        if sum([_length_list[a] for a in _xx[:4]]) == 2 * _n + 2:
            break
    print(_initial_state)

    _state, _sol = solve_greed(_initial_state, _solution_state, _length_list, 0, 0)
    print(_state)
    print(_sol)
