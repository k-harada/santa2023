from typing import List, Dict, Optional
from sympy.combinatorics import Permutation
from abc import abstractmethod
import numpy as np


class BaseSolver:

    def __init__(self, n: int):
        self.n: int = n
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
            allowed_moves[f"f{i}"] = allowed_moves["-r0"] * allowed_moves["-r1"] * allowed_moves[f"f{i - 1}"] * \
                                     allowed_moves["r0"] * allowed_moves["r1"]

        self.state: Optional[np.array] = None
        self.initial_state: Optional[np.array] = None
        self.goal_state: Optional[np.array] = None
        self.path: List[str] = []
        self.allowed_moves_arr: Dict[str, np.array] = dict()
        for k in allowed_moves.keys():
            xxx = allowed_moves[k](np.arange(4 * n))
            self.allowed_moves_arr[k] = np.arange(4 * n)[xxx]

    def operate(self, m: str):
        # self.state = (self.allowed_moves[m])(self.state)
        self.state = self.state[self.allowed_moves_arr[m]]
        self.path.append(m)

    def operate_list(self, m_list: List[str]):
        for m in m_list:
            self.operate(m)

    def initialize(self, initial_state: List[str], goal_state: List[str]):
        self.initial_state = np.array(initial_state)
        self.goal_state = np.array(goal_state)
        self.state = self.initial_state.copy()
        self.path = []
        return None

    def reset(self):
        self.path = []
        self.state = self.initial_state.copy()
        return None

    @abstractmethod
    def solve(self):
        return None

    def is_solved(self):
        return list(self.state) == list(self.goal_state)

    def get_length(self):
        return len(self.path)

    def get_path(self):
        return self.path
