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


def state_to_int(state: List[List[int]]):
    res = 0
    for st in state:
        for x in st:
            res *= 10
            res += x
    return res


def int_to_state(state_int: int, m: int, n: int, length_list: List[int]):
    x = state_int
    state_rev = []
    for _ in range(m):
        state_rev.append(x % 10)
        x //= 10
    res = [[], []]
    rr = 0
    for a in reversed(state_rev):
        if rr < 2 * n:
            res[0].append(a)
        else:
            res[1].append(a)
        rr += length_list[a]
    return res


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
    assert max(initial_state[0] + initial_state[1]) < 10
    n = sum([length_list[p] for p in initial_state[0]]) // 2
    m = len(initial_state[0] + initial_state[1])

    open_set = []
    c_0 = length_list[initial_state[0][-1]]
    c_1 = length_list[initial_state[1][-1]]
    initial_state_int = state_to_int(initial_state)
    # right-right
    heappush(open_set, (r_0 + r_1, state_to_int(initial_state), initial_state_int))
    # left-right
    new_state = [[initial_state[0][-1]] + initial_state[0][:-1], initial_state[1]]
    if c_0 > r_0:
        heappush(open_set, ((c_0 - r_0) + r_1, state_to_int(new_state), initial_state_int))
    else:
        heappush(open_set, ((r_0 - c_0) + r_1, state_to_int(new_state), initial_state_int))
    # right-left
    new_state = [initial_state[0], [initial_state[1][-1]] + initial_state[1][:-1]]
    if c_1 > r_1:
        heappush(open_set, ((c_1 - r_1) + r_0, state_to_int(new_state), initial_state_int))
    else:
        heappush(open_set, ((r_1 - c_1) + r_0, state_to_int(new_state), initial_state_int))
    # left-left
    new_state = [[initial_state[0][-1]] + initial_state[0][:-1], [initial_state[1][-1]] + initial_state[1][:-1]]

    if c_0 > r_0:
        if c_1 > r_1:
            heappush(open_set, (abs(c_0 - r_0) + abs(c_1 - r_1), state_to_int(new_state), initial_state_int))
        else:
            heappush(open_set, (abs(c_0 - r_0) + abs(c_1 - r_1), state_to_int(new_state), initial_state_int))
    else:
        if c_1 > r_1:
            heappush(open_set, (abs(c_0 - r_0) + abs(c_1 - r_1), state_to_int(new_state), initial_state_int))
        else:
            heappush(open_set, (abs(c_0 - r_0) + abs(c_1 - r_1), state_to_int(new_state), initial_state_int))

    closed_set = dict()
    goal_state_int = state_to_int(goal_state)

    while len(open_set):

        p, current_state_int, previous_state_int = heappop(open_set)

        if current_state_int == goal_state_int:
            return current_state_int, previous_state_int

        if current_state_int in closed_set.keys():
            continue

        closed_set[current_state_int] = previous_state_int
        if np.random.uniform() < 0.00001:
            print(len(closed_set))

        current_state = int_to_state(current_state_int, m, n, length_list)

        # r0
        new_state = current_state.copy()
        action = ["r0"] * length_list[new_state[0][0]]
        new_state[0] = new_state[0][1:] + [new_state[0][0]]
        new_state_int = state_to_int(new_state)
        if new_state_int not in closed_set.keys():
            priority = p + len(action) + heuristic(new_state, goal_state)
            heappush(open_set, (priority, new_state_int, current_state_int))

        # -r0
        new_state = current_state.copy()
        action = ["-r0"] * length_list[new_state[0][-1]]
        new_state[0] = [new_state[0][-1]] + new_state[0][:-1]
        new_state_int = state_to_int(new_state)
        if new_state_int not in closed_set.keys():
            priority = p + len(action) + heuristic(new_state, goal_state)
            heappush(open_set, (priority, new_state_int, current_state_int))

        # r1
        new_state = current_state.copy()
        action = ["r1"] * length_list[new_state[1][0]]
        new_state[1] = new_state[1][1:] + [new_state[1][0]]
        new_state_int = state_to_int(new_state)
        if new_state_int not in closed_set.keys():
            priority = p + len(action) + heuristic(new_state, goal_state)
            heappush(open_set, (priority, new_state_int, current_state_int))

        # -r1
        new_state = current_state.copy()
        action = ["-r1"] * length_list[new_state[1][-1]]
        new_state[1] = [new_state[1][-1]] + new_state[1][:-1]
        new_state_int = state_to_int(new_state)
        if new_state_int not in closed_set.keys():
            priority = p + len(action) + heuristic(new_state, goal_state)
            heappush(open_set, (priority, new_state_int, current_state_int))

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
            new_state_int = state_to_int(new_state)
            if new_state_int not in closed_set.keys():
                priority = p + len(action) + heuristic(new_state, goal_state)
                heappush(open_set, (priority, new_state_int, current_state_int))
    return None, None


if __name__ == "__main__":

    # fake problems
    _solution_state = [[0, 1, 2, 3, 3, 3], [4, 5, 6, 7, 7, 7]]
    _xx = np.array([0, 1, 2, 3, 3, 3, 4, 5, 6, 7, 7, 7])
    _n = 15
    _length_list = [_n, 1, _n - 2, 1, _n, 1, _n - 2, 1]
    while True:
        np.random.shuffle(_xx)
        _initial_state = [list(_xx[:6]), list(_xx[6:])]
        if sum([_length_list[a] for a in _xx[:6]]) == 2 * _n + 2:
            break
    print(_initial_state)

    _state, _sol = solve_greed(_initial_state, _solution_state, _length_list, 0, 0)
    print(_state)
    print(_sol)
