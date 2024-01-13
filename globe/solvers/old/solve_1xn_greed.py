from typing import Dict, List, Optional
from heapq import heappop, heappush
import numpy as np
from sympy.combinatorics import Permutation

from globe.solvers.base_1xn import BaseSolver


class GreedySolver(BaseSolver):

    def __init__(self, n: int):
        super().__init__(n)
        self.num_wildcards = 0
        self.force_pair = False

    def initialize(
            self, initial_state: List[str], goal_state: List[str],
            num_wildcards: int = 0, force_pair: bool = False
    ):
        super().initialize(initial_state, goal_state)
        self.num_wildcards = num_wildcards
        self.force_pair = force_pair

    def solve(self):
        n = self.n
        open_set_left = []
        open_set_right = []
        closed_set_left = set()
        closed_set_right = set()

        path_dict_left = dict()
        path_dict_right = dict()
        _initial_state = "_".join(self.initial_state)
        _goal_state = "_".join(self.goal_state)

        heappush(open_set_left, (0, _initial_state, []))
        heappush(open_set_right, (0, _goal_state, []))
        # action_list = ["r0", "-r0", "r1", "-r1", f"f{n}"]
        # [11, 11, 9, 12, 12, 10, 7, 13, 9, 13]
        action_list = ["r0", "-r0", "r1", "-r1"] + [f"f{i}" for i in range(2 * n)]
        # [9, 9, 11, 8, 11, 12, 6, 11, 9, 11]

        while len(open_set_left):

            _, _current_state, path = heappop(open_set_left)
            current_state = np.array(list(_current_state.split("_")))
            # print(_current_state)
            if np.random.uniform() < 0.0001:
                print(len(closed_set_left), len(closed_set_right))

            if _current_state == _goal_state:
                self.operate_list(path)
                return None
            if _current_state in closed_set_left:
                continue
            if _current_state in closed_set_right:
                path_joint = _modify_path(path, path_dict_right[_current_state])
                self.operate_list(path_joint)
                return None

            count_f = [0] * (2 * n)
            for _m in path:
                if _m[0] == "f":
                    count_f[int(_m[1:])] += 1
            odd = -1
            for i in range(2 * n):
                if count_f[i] % 2 == 1:
                    odd = i
            if not self.force_pair:
                odd = -1

            if self.force_pair and odd >= 0:
                pass
            else:
                path_dict_left[_current_state] = path
                closed_set_left.add(_current_state)

            for action in action_list:
                if odd != -1 and action[0] == "f" and action != f"f{odd}":
                    continue
                new_state = current_state[self.allowed_moves_arr[action]]
                _new_state = "_".join(new_state)
                if _new_state not in closed_set_left:
                    priority = len(path) + 1
                    heappush(open_set_left, (priority, _new_state, path + [action]))

            # right
            _, _current_state, path = heappop(open_set_right)
            current_state = np.array(list(_current_state.split("_")))
            # print(_current_state)
            if np.random.uniform() < 0.0001:
                print(len(closed_set_left), len(closed_set_right))

            if _current_state == _initial_state:
                path_joint = _modify_path([], path)
                self.operate_list(path_joint)
                return None
            if _current_state in closed_set_right:
                continue
            if _current_state in closed_set_left:
                path_joint = _modify_path(path_dict_left[_current_state], path)
                self.operate_list(path_joint)
                return None

            count_f = [0] * (2 * n)
            for _m in path:
                if _m[0] == "f":
                    count_f[int(_m[1:])] += 1
            odd = -1
            for i in range(2 * n):
                if count_f[i] % 2 == 1:
                    odd = i
            if not self.force_pair:
                odd = -1

            if self.force_pair and odd >= 0:
                pass
            else:
                path_dict_right[_current_state] = path
                closed_set_right.add(_current_state)

            for action in action_list:
                if odd != -1 and action[0] == "f" and action != f"f{odd}":
                    continue
                new_state = current_state[self.allowed_moves_arr[action]]
                _new_state = "_".join(new_state)
                if _new_state not in closed_set_right:
                    priority = len(path) + 1
                    heappush(open_set_right, (priority, _new_state, path + [action]))
        return None, None


def _modify_path(path_left, path_right):
    path = path_left
    for _m in reversed(path_right):
        if _m[0] == "f":
            path.append(_m)
        elif _m[0] == "-":
            path.append(_m[1:])
        else:
            path.append("-" + _m)
    return path


if __name__ == "__main__":

    solver = GreedySolver(2)
    solver.initialize(
        ["0", "1", "2", "7", "4", "5", "6", "3"],
        ["0", "1", "2", "3", "4", "5", "6", "7"]
    )
    solver.solve()
    print(solver.state)
    print(solver.path)
    np.random.seed(71)
    res = []
    for _ in range(10):
        # fake problems
        _solution_state = [str(_i) for _i in range(8)]
        _xx = np.array(_solution_state)
        np.random.shuffle(_xx)
        solver.initialize(list(_xx), _solution_state, force_pair=True)
        solver.solve()
        print(solver.state)
        print(solver.path)
        res.append(len(solver.path))
    print(res)

