from typing import List, Dict, Optional
import numpy as np

from globe.solvers.base_1xn import BaseSolver
from globe.solvers.trivial_center import solve_trivial
from globe.solvers.magic import *


class SwapSolver(BaseSolver):

    def __init__(self, n: int):
        super().__init__(n)
        self.seed = -1
        self.aligned: bool = False

    def initialize(self, initial_state: List[str], goal_state: List[str], seed: int = -1):
        super().initialize(initial_state, goal_state)
        self.aligned = False
        self.seed = seed
        return None

    def solve(self):
        n = self.n
        self._align_up_down_greed()
        if not self.aligned:
            self.path = None
            return None
        h_up, h_low = self._heuristic(self.state[:2 * n], self.state[2 * n:])
        while max(h_up, h_low) > 0:
            d, ui, li = self._find_max_swap()
            # print(d, ui, li)
            # print(self.state[:n])
            # print(self.state[n:2 * n])
            # print(self.state[2 * n:3 * n])
            # print(self.state[3 * n:4 * n])
            self._run_swap(d, ui, li)
            h_up, h_low = self._heuristic(self.state[:2 * n], self.state[2 * n:])
            print(h_up, h_low)
            # print(self.state[:n])
            # print(self.state[n:2 * n])
            # print(self.state[2 * n:3 * n])
            # print(self.state[3 * n:4 * n])
        # do trivial
        _sol = solve_trivial(list(self.state[:2 * n]), list(self.goal_state[:2 * n]))
        self.operate_list(_sol)
        _sol = solve_trivial(list(self.state[2 * n:]), list(self.goal_state[2 * n:]))
        _sol_mod = []
        for _m in _sol:
            if _m == "r0":
                _sol_mod.append("r1")
            else:
                _sol_mod.append("-r1")
        self.operate_list(_sol_mod)
        return None

    def _align_up_down_greed(self):
        n = self.n
        seed = self.seed
        if seed != -1:
            np.random.seed(seed)

        # 上下を合わせる
        upper_set = set()
        lower_set = set()
        for i in range(2 * n):
            upper_set.add(self.goal_state[i])
            lower_set.add(self.goal_state[i + 2 * n])
        mismatch = 0
        for i in range(2 * n):
            if self.state[i] in lower_set:
                mismatch += 1
        while mismatch > 0:

            self.operate("r0")
            # magic_updown2
            # cとc+nで上下を入れ替える魔法
            for i in range(n):
                if (self.state[i] in lower_set and self.state[i + n] in lower_set) and (
                        self.state[i + 2 * n] in upper_set and self.state[i + 3 * n] in upper_set
                ):
                    self.operate_list(magic_updown2(i, 0, n))
            # magic_updown1
            # 下段からc番目を上に上げて上段のc-1番目を下に落とす魔法

            continue_flag = True
            while continue_flag:
                continue_flag = False
                for i in range(2 * n):
                    if self.state[i + 2 * n] in upper_set and self.state[(i - 1) % (2 * n)] in lower_set:
                        if seed != -1:
                            if np.random.uniform() < 0.2:
                                continue
                        self.operate_list(magic_updown1(i, 0, n))
                        continue_flag = True

            mismatch = 0
            for i in range(2 * n):
                if self.state[i] in lower_set:
                    mismatch += 1

        pi, pj = self._check_parity(list(self.state[:2 * n]), list(self.state[2 * n:]))
        if (pi - pj) % 2 == 1:
            print("parity check failed")
            self.aligned = False
        else:
            self.aligned = True
        return None

    def _find_max_swap(self):
        n = self.n
        h_min = 10 ** 9
        d_min = -1
        ui = -1
        li = -1
        for d in range(1, n + 1):
            best_uh = 10 ** 9
            best_ui = -1
            for i in range(2 * n):
                base_list = list(self.state[i:2 * n]) + list(self.state[:i])
                h_up, _ = self._heuristic([base_list[d]] + base_list[1:d] + [base_list[0]] + base_list[d + 1:],
                                          self.state[2 * n:])
                if h_up < best_uh:
                    best_uh = h_up
                    best_ui = i

            best_lh = 10 ** 9
            best_li = -1
            for i in range(2 * n):
                base_list = list(self.state[2 * n + i:4 * n]) + list(self.state[2 * n:2 * n + i])
                _, h_low = self._heuristic(self.state[:2 * n],
                                           [base_list[d]] + base_list[1:d] + [base_list[0]] + base_list[d + 1:])
                if h_low < best_lh:
                    best_lh = h_low
                    best_li = i
            h = max(best_uh, best_lh)
            # print(d, h, best_ui, best_li)
            if h < h_min:
                h_min = h
                d_min = d
                ui = best_ui
                li = best_li
        print(h_min, d_min, ui, li, self.get_length())
        return d_min, ui, li

    def _run_swap(self, d, ui, li):
        n = self.n
        # li -> ui
        dif = (ui - li) % (2 * n)
        print(dif)
        if dif <= n:
            self.operate_list(["-r1"] * dif)
        else:
            self.operate_list(["r1"] * (2 * n - dif))
        if d % 2 == 0:
            c = ui + d // 2
            # index c（0-base）を中心に上下ともに距離kを置換する魔法（cは動かない）
            sol = magic_swap1(c, d//2, n)
        else:
            # index c（0-base）を右、その前を左とする中心線で距離kを上下とも置換する魔法（cは動かない）
            c = ui + (d + 1) // 2
            sol = magic_swap2(c, (d - 1) // 2, n)
        # print(self.state[:n])
        # print(self.state[n:2 * n])
        # print(self.state[2 * n:3 * n])
        # print(self.state[3 * n:4 * n])
        self.operate_list(sol)

    def _heuristic(self, upper_list, lower_list):
        n = self.n
        upper_ind_list = [i for i in range(2 * n) if upper_list[i] == self.goal_state[0]]
        lower_ind_list = [i for i in range(2 * n) if lower_list[i] == self.goal_state[2 * n]]
        index_dict = dict()
        count_dict = dict()
        for i, c in enumerate(self.goal_state[:2 * n]):
            if c not in index_dict.keys():
                index_dict[c] = i
                count_dict[c] = 1
            else:
                count_dict[c] += 1
        for i, c in enumerate(self.goal_state[2 * n:]):
            if c not in index_dict.keys():
                index_dict[c] = i
                count_dict[c] = 1
            else:
                count_dict[c] += 1
        # print(index_dict, count_dict)
        h_upper = 10 ** 9
        for upper_ind in upper_ind_list:
            c_list = []
            v_list = []
            h_upper_ = 0
            for i in range(2 * n):
                c = upper_list[(i + upper_ind) % (2 * n)]
                c_list.append(c)
                if i < index_dict[c]:
                    h_upper_ += abs(i - index_dict[c])
                elif index_dict[c] <= i < index_dict[c] + count_dict[c]:
                    h_upper_ += 0
                else:
                    h_upper_ += abs(i - (index_dict[c] + count_dict[c] - 1))
                v_list.append(h_upper_)
            # print(c_list, v_list)
            h_upper = min(h_upper, h_upper_)

        h_lower = 10 ** 9
        for lower_ind in lower_ind_list:
            h_lower_ = 0
            for i in range(2 * n):
                c = lower_list[(i + lower_ind) % (2 * n)]
                if i < index_dict[c]:
                    h_lower_ += abs(i - index_dict[c])
                elif index_dict[c] <= i < index_dict[c] + count_dict[c]:
                    h_lower_ += 0
                else:
                    h_lower_ += abs(i - (index_dict[c] + count_dict[c] - 1))
            h_lower = min(h_lower, h_lower_)

        return h_upper, h_lower

    def _check_parity(self, upper_list, lower_list):
        # 転倒数
        n = self.n
        upper_ind_list = [i for i in range(2 * n) if upper_list[i] == self.goal_state[0]]
        lower_ind_list = [i for i in range(2 * n) if lower_list[i] == self.goal_state[2 * n]]
        index_dict = dict()
        count_dict = dict()
        for i, c in enumerate(self.goal_state[:2 * n]):
            if c not in index_dict.keys():
                index_dict[c] = i
                count_dict[c] = 1
            else:
                count_dict[c] += 1
        for i, c in enumerate(self.goal_state[2 * n:]):
            if c not in index_dict.keys():
                index_dict[c] = i
                count_dict[c] = 1
            else:
                count_dict[c] += 1
        # print(index_dict, count_dict)
        h_upper = 10 ** 9
        for upper_ind in upper_ind_list:
            # 転倒数
            h_upper_ = 0
            for i in range(2 * n):
                for j in range(i + 1, 2 * n):
                    ci = upper_list[(i + upper_ind) % (2 * n)]
                    cj = upper_list[(j + upper_ind) % (2 * n)]
                    if index_dict[ci] > index_dict[cj]:
                        h_upper_ += 1
            h_upper = min(h_upper, h_upper_)

        h_lower = 10 ** 9
        for lower_ind in lower_ind_list:
            # 転倒数
            h_lower_ = 0
            for i in range(2 * n):
                for j in range(i + 1, 2 * n):
                    ci = lower_list[(i + lower_ind) % (2 * n)]
                    cj = lower_list[(j + lower_ind) % (2 * n)]
                    if index_dict[ci] > index_dict[cj]:
                        h_lower_ += 1
            h_lower = min(h_lower, h_lower_)

        return h_upper, h_lower


if __name__ == "__main__":
    solver = SwapSolver(4)
    solver.initialize([str(i) for i in range(15, -1, -1)], [str(i) for i in range(16)])
    solver.solve()
    print(solver.state)
    print(solver.path)
