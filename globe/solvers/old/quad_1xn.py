from typing import Dict, List, Optional
from heapq import heappop, heappush
import numpy as np
from sympy.combinatorics import Permutation

from globe.solvers.base_1xn import BaseSolver


class QuadSolver(BaseSolver):

    def __init__(self, n: int):
        super().__init__(n)
        self.allowed_f = -1
        self.fixed_list: List[List[str]] = []

    def initialize(self, initial_state: List[str], goal_state: List[str], allowed_f: int = -1):
        super().initialize(initial_state, goal_state)
        self.fixed_list = []
        self.allowed_f = allowed_f
        return None

    def _heuristic_phase_1(self, state: List[str]):
        n = self.n
        points = list(sorted([
            self.goal_state[0], self.goal_state[n], self.goal_state[3 * n - 1], self.goal_state[4 * n - 1]
        ]))
        for i in range(n):
            for j in range(n):
                if list(sorted([state[i], state[i + n], state[j + 2 * n], state[j + 3 * n]])) == points:
                    return 0
        else:
            return 1

    def _phase_1(self):
        n = self.n
        open_set = []
        closed_set = set()

        if self.allowed_f == -1:
            action_list = ["r0", "-r0", "r1", "-r1"] + [f"f{i}" for i in range(2 * n)]
        else:
            assert 0 <= self.allowed_f < 2 * n
            action_list = ["r0", "-r0", "r1", "-r1"] + [f"f{self.allowed_f}"]

        _initial_state = "_".join(self.initial_state)
        _goal_state = "_".join(self.goal_state)

        heappush(open_set, (0, _initial_state, []))

        while len(open_set):

            _, _current_state, path = heappop(open_set)
            current_state = np.array(list(_current_state.split("_")))
            # print(_current_state)
            if np.random.uniform() < 0.0001:
                print(len(closed_set))

            if self._heuristic_phase_1(list(current_state)) == 0:
                self.operate_list(path)
                return None

            if _current_state in closed_set:
                continue

            closed_set.add(_current_state)

            for action in action_list:
                new_state = current_state[self.allowed_moves_arr[action]]
                _new_state = "_".join(new_state)
                if _new_state not in closed_set:
                    priority = len(path) + 1
                    heappush(open_set, (priority, _new_state, path + [action]))

    def solve(self):
        pass


if __name__ == "__main__":
    solver = QuadSolver(4)
    a = np.array([str(i) for i in range(64)])
    b = np.array([str(i) for i in range(64)])
    np.random.shuffle(a)
    solver.initialize(list(a), list(b))
    solver._phase_1()
    print(a)
    print(solver.state)
    print(solver.path)


