import numpy as np
from itertools import permutations
from typing import Dict, List
from sympy.combinatorics import Permutation
from heapq import heappop, heappush
from puzzle import Puzzle


action_list = [[
    ["r0"], ["-r0"], ["r1"], ["-r1"],
    # ["f0"], ["f1"],
    ["f2"],
    # ["f3"]
]]
allowed_moves: Dict[str, Permutation] = dict()
allowed_moves["r0"] = Permutation([1, 2, 3, 0, 4, 5, 6, 7])
allowed_moves["r1"] = Permutation([0, 1, 2, 3, 5, 6, 7, 4])
allowed_moves["f0"] = Permutation([5, 4, 2, 3, 1, 0, 6, 7])
allowed_moves["f1"] = Permutation([0, 6, 5, 3, 4, 2, 1, 7])
allowed_moves["f2"] = Permutation([0, 1, 7, 6, 4, 5, 3, 2])
allowed_moves["f3"] = Permutation([7, 1, 2, 4, 3, 5, 6, 0])
allowed_moves["-r0"] = allowed_moves["r0"] ** (-1)
allowed_moves["-r1"] = allowed_moves["r1"] ** (-1)


def heuristic(x, y, stage=0):
    # BFS
    return 0


def solve_1x2(puzzle: Puzzle):
    initial_state = puzzle.initial_state
    goal_state = puzzle.solution_state
    stage = 0
    open_set = []
    heappush(open_set, (0, initial_state, []))
    closed_set = set()

    while len(open_set):

        _, current_state, path = heappop(open_set)

        if current_state == goal_state:
            return current_state, path

        closed_set.add(tuple(current_state))

        for action in action_list[stage]:
            new_state = current_state.copy()
            for move_name in action:
                move = allowed_moves[move_name]
                new_state = move(new_state)
            if tuple(new_state) not in closed_set:
                priority = len(path) + len(action) + heuristic(new_state, goal_state, stage)
                heappush(open_set, (priority, new_state, path + action))


if __name__ == "__main__":
    # fake problems
    _solution_state = ["A1", "A2", "B1", "B2", "C1", "C2", "D", "D"]
    for _i, _pp in enumerate(permutations(list(range(8)))):
        _xx = np.arange(8)
        np.random.shuffle(_xx)
        _initial_state = []
        for _x in _pp:
            _initial_state.append(_solution_state[_x])
        _p = Puzzle(
            1000, 'globe_1/2', _solution_state,
            _initial_state, 0, True
        )
        _p.allowed_moves = allowed_moves
        _state, _sol = solve_1x2(_p)
        for _m in _sol:
            _p.operate(_m)
        print(_i, _pp)
        print(_p)
        print(_p.move_history)
        print(_p.solution_state)
        # not all
        if _i == 320:
            break
