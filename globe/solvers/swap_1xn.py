from typing import List, Dict, Optional
import numpy as np
import numba

from globe.solvers.base_1xn import BaseSolver
from globe.solvers.trivial_center import solve_trivial
from globe.solvers.magic import *


@numba.njit("i4(i4, i4[:], i4[:])")
def heuristic_numba(n, state_list_int, counter):
    if state_list_int.min() == 0:
        h_upper = np.int32(10 ** 9)
        for upper_ind in range(2 * n):
            if state_list_int[upper_ind] == 0:
                h_upper_ = 0
                for i in range(2 * n):
                    c = state_list_int[(i + upper_ind) % (2 * n)]
                    if i < c:
                        h_upper_ += abs(i - c)
                    elif c <= i < c + counter[c]:
                        h_upper_ += 0
                    else:
                        h_upper_ += abs(i - (c + counter[c] - 1))
                h_upper = min(h_upper, h_upper_)
        return h_upper
    else:
        h_lower = 10 ** 9
        for lower_ind in range(2 * n):
            if state_list_int[lower_ind] == 2 * n:
                h_lower_ = 0
                for i in range(2 * n):
                    c = state_list_int[(i + lower_ind) % (2 * n)] - 2 * n
                    if i < c:
                        h_lower_ += abs(i - c)
                    elif c <= i < c + counter[c + 2 * n]:
                        h_lower_ += 0
                    else:
                        h_lower_ += abs(i - (c + counter[c + 2 * n] - 1))
                h_lower = min(h_lower, h_lower_)
        return h_lower


@numba.njit("i4[:, :](i4, i4[:], i4[:], i4)")
def calc_heuristic(n, state, counter, hard_flag):
    res = 10000000 * np.ones((2 * n, n + 1), dtype=np.int32)
    for d in range(1, n + 1):
        for i in range(2 * n):
            x = np.zeros(2 * n, dtype=np.int32)
            for j in range(2 * n):
                x[j] = state[(j + i) % (2 * n)]
            x[0], x[d] = x[d], x[0]
            if d % 2 == 1 and (state[i] % (2 * n) == 0 or state[(i + d) % (2 * n)] % (2 * n) == 0) and hard_flag == 1:
                continue
            res[i, d] = heuristic_numba(n, x, counter)
    return res.astype(np.int32)


class SwapSolver(BaseSolver):

    def __init__(self, n: int):
        super().__init__(n)
        self.initial_state_int = np.zeros(4 * n, dtype=np.int32)
        self.state_int = np.zeros(4 * n, dtype=np.int32)
        self.goal_state_int = np.zeros(4 * n, dtype=np.int32)
        self.counter = np.zeros(4 * n, dtype=np.int32)
        self.char_to_int = dict()
        self.temperature: Optional[float] = 0.0
        self.p_cost: Optional[float] = 0.0

    def initialize(
            self, initial_state: List[str], goal_state: List[str],
            temperature: Optional[float] = None, p_cost: Optional[float] = None
    ):
        super().initialize(initial_state, goal_state)
        for i, c in enumerate(self.goal_state):
            if c not in self.char_to_int.keys():
                self.char_to_int[c] = i
        for c in self.goal_state:
            self.counter[self.char_to_int[c]] += 1
        for i, c in enumerate(self.initial_state):
            self.initial_state_int[i] = self.char_to_int[c]
        for i, c in enumerate(self.goal_state):
            self.goal_state_int[i] = self.char_to_int[c]
        self._update_int()
        if temperature is not None:
            self.temperature = temperature
        if p_cost is not None:
            self.p_cost = p_cost
        return None

    def _update_int(self):
        for i, c in enumerate(self.state):
            self.state_int[i]= self.char_to_int[c]
        return None

    def solve(self, random: bool = False):
        n = self.n
        pi, pj = self.align_up_down(random)
        if (pi - pj) % 2 == 1 and self.goal_state[0] != self.goal_state[1]:
            print("parity check failed")
            self.path = None
            return None
        else:
            pass
            # print("parity check passed")
            # print(self.state)
        h_up, h_low = self._heuristic(self.state[:2 * n], self.state[2 * n:])
        while max(h_up, h_low) > 0:
            if len(self.path) > 5000:
                print("maybe infinite loop")
                self.path = None
                return None
            d, ui, li = self._find_good_swap()
            # print(d, ui, li)
            # print(self.state[:n])
            # print(self.state[n:2 * n])
            # print(self.state[2 * n:3 * n])
            # print(self.state[3 * n:4 * n])
            self._run_swap(d, ui, li)
            h_up, h_low = self._heuristic(self.state[:2 * n], self.state[2 * n:])
            # print(h_up, h_low)
            # print(self._check_parity(list(self.state[:2 * n]), list(self.state[2 * n:])))
            # print(self.state[:n])
            # print(self.state[n:2 * n])
            # print(self.state[2 * n:3 * n])
            # print(self.state[3 * n:4 * n])
            # print(self.state_int)
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
        while True:
            le = len(self.path)
            self._post_process()
            if le == len(self.path):
                break
        return None

    def align_up_down(self, random: bool = False):
        n = self.n

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
                    if random:
                        if np.random.uniform() < 0.5:
                            continue
                    self.operate_list(magic_updown2(i, 0, n))
            # magic_updown1
            # 下段からc番目を上に上げて上段のc-1番目を下に落とす魔法
            continue_flag = True
            while continue_flag:
                continue_flag = False
                for i in range(2 * n):
                    if self.state[i + 2 * n] in upper_set and self.state[(i - 1) % (2 * n)] in lower_set:
                        if random:
                            if np.random.uniform() < 0.2:
                                continue
                        self.operate_list(magic_updown1(i, 0, n))
                        continue_flag = True

            mismatch = 0
            for i in range(2 * n):
                if self.state[i] in lower_set:
                    mismatch += 1
        self._update_int()
        pi, pj = self._check_parity(list(self.state[:2 * n]), list(self.state[2 * n:]))
        return pi, pj

    def _find_good_swap(self):
        n = self.n
        temperature = self.temperature
        p_cost = self.p_cost
        if self.goal_state[0] != self.goal_state[1]:
            hard_flag = 1
        else:
            hard_flag = 0
        res_h_up = calc_heuristic(n, self.state_int[:2 * n], self.counter, hard_flag)
        res_h_low = calc_heuristic(n, self.state_int[2 * n:], self.counter, hard_flag)

        h_up_now, h_low_now = self._heuristic(self.state[:2 * n], self.state[2 * n:])
        h_min = h_up_now + h_low_now

        cost_all = h_min * np.ones((2 * n, 2 * n, n + 1), dtype=np.float32)
        for i in range(2 * n):
            cost_all[:, i, :] -= res_h_up
            cost_all[i, :, :] -= res_h_low
        cost_all[cost_all <= 0] -= 10000
        for i in range(2 * n):
            for j in range(2 * n):
                cost_all[i, j, :] -= p_cost * min(abs(i - j), 2 * n - abs(i - j))
        cost_all -= cost_all.max()

        if temperature <= 0:
            res = np.where(cost_all == 0)
            ui = res[0][0]
            li = res[1][0]
            d = res[2][0]
        else:
            cost_all = np.exp(cost_all / temperature)
            cost_all /= cost_all.sum()
            r = np.random.choice(4 * n * n * (n + 1), p=cost_all.flatten())
            ui, r = r // (2 * n * (n + 1)), r % (2 * n * (n + 1))
            li, d = r // (n + 1), r % (n + 1)

        return d, ui, li

    def _rotate(self, d, ui, li, dif, target_f):
        n = self.n
        if d % 2 == 0:
            c_target = (- (d // 2) - 1 + target_f) % (2 * n)
        else:
            c_target = (- ((d + 1) // 2) + target_f) % (2 * n)
        if min(
                (ui - c_target) % (2 * n), (c_target - ui) % (2 * n)
        ) + min(
            (li - c_target) % (2 * n), (c_target - li) % (2 * n)
        ) == abs(dif):
            if (ui - c_target) % (2 * n) <= (c_target - ui) % (2 * n):
                self.operate_list(["r0"] * ((ui - c_target) % (2 * n)))
            else:
                self.operate_list(["-r0"] * ((c_target - ui) % (2 * n)))
            if (li - c_target) % (2 * n) <= (c_target - li) % (2 * n):
                self.operate_list(["r1"] * ((li - c_target) % (2 * n)))
            else:
                self.operate_list(["-r1"] * ((c_target - li) % (2 * n)))
            return c_target, True
        else:
            return c_target, False

    def _run_swap(self, d, ui, li):
        n = self.n
        # li -> ui
        dif = (ui - li) % (2 * n)
        # print(dif)
        if dif > n:
            dif = dif - 2 * n
        if n == 4:
            try_list = [0, 4, 2, 6]
        elif n == 6:
            try_list = [0, 6, 3, 9]
        elif n == 8:
            try_list = [0, 8, 4, 12, 2, 6, 10, 14]
        elif n == 10:
            try_list = [0, 10, 5, 15, 3, 7, 13, 17]
        elif n == 16:
            try_list = [0, 16, 8, 24, 4, 12, 20, 28]
        elif n == 25:
            try_list = [0, 25, 12, 38, 6, 18, 32, 44]
        elif n == 33:
            try_list = [0, 33, 11, 22, 44, 55, 5, 16, 27, 38, 49, 60]
        else:
            print(f"Unknown n: {n}")
            try_list = []
        short_cut = False
        for t in try_list:
            base, short_cut = self._rotate(d, ui, li, dif, t)
            if short_cut:
                break
        if not short_cut:
            base = ui
            if dif >= 0:
                self.operate_list(["-r1"] * dif)
            else:
                self.operate_list(["r1"] * (-dif))
        if d % 2 == 0:
            d_ = d // 2
            c_ = (base + d // 2) % (2 * n)
            if c_ > n:
                c_ -= n
                d_ = n - d_
            # index c（0-base）を中心に上下ともに距離kを置換する魔法（cは動かない）
            sol = magic_swap1(c_, d_, n)
        else:
            # index c（0-base）を右、その前を左とする中心線で距離kを上下とも置換する魔法（cは動かない）
            c = (base + (d + 1) // 2) % (2 * n)
            sol = magic_swap2(c, (d - 1) // 2, n)
        # print(self.state[:n])
        # print(self.state[n:2 * n])
        # print(self.state[2 * n:3 * n])
        # print(self.state[3 * n:4 * n])
        self.operate_list(sol)
        self._update_int()

    def _heuristic(self, upper_list, lower_list):
        n = np.int32(self.n)
        upper_list_int = np.zeros(2 * n, dtype=np.int32)
        lower_list_int = np.zeros(2 * n, dtype=np.int32)
        for i, c in enumerate(upper_list):
            upper_list_int[i] = self.char_to_int[c]
        for i, c in enumerate(lower_list):
            lower_list_int[i] = self.char_to_int[c]
        # print(upper_list_int)
        # print(lower_list_int)
        h_upper = heuristic_numba(n, upper_list_int, self.counter)
        h_lower = heuristic_numba(n, lower_list_int, self.counter)
        return h_upper, h_lower

    def _heuristic_old(self, upper_list, lower_list):
        # switched to numba version
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

    def _post_process(self):
        n = self.n
        new_list = []
        r0 = 0
        r1 = 0
        fn = -1
        for m in self.path:
            if m == "r0":
                r0 += 1
            elif m == "-r0":
                r0 -= 1
            elif m == "r1":
                r1 += 1
            elif m == "-r1":
                r1 -= 1
            else:
                r0 %= (2 * n)
                r1 %= (2 * n)
                if r0 > n:
                    r0 -= 2 * n
                if r1 > n:
                    r1 -= 2 * n
                if r0 >= 0:
                    new_list = new_list + ["r0"] * r0
                else:
                    new_list = new_list + ["-r0"] * (-r0)
                if r1 >= 0:
                    new_list = new_list + ["r1"] * r1
                else:
                    new_list = new_list + ["-r1"] * (-r1)

                if len(new_list) > 0:
                    if new_list[-1] == m:
                        _ = new_list.pop()
                    else:
                        new_list.append(m)
                else:
                    new_list.append(m)
                r0 = 0
                r1 = 0
                _fn = int(m[1:])
                if fn == _fn:
                    fn = -1
                else:
                    fn = _fn
        if r0 >= 0:
            new_list = new_list + ["r0"] * r0
        else:
            new_list = new_list + ["-r0"] * (-r0)
        if r1 >= 0:
            new_list = new_list + ["r1"] * r1
        else:
            new_list = new_list + ["-r1"] * (-r1)
        # print(len(new_list), len(self.path))
        self.path = new_list
        return None


if __name__ == "__main__":
    solver = SwapSolver(4)
    solver.initialize([str(i) for i in range(15, -1, -1)], [str(i) for i in range(16)])
    solver.solve()
    print(solver.state)
    print(solver.path)

# 28 C B
# 29 C H
# 26 C D
# 21 A F
# 9 I N
# 14 K F
# 14 I D
# 10 G P
# 21 M J
# 11 G P
# 17 I F
# 3 A P
# 17 I D
# 27 M H
# 29 O J
# 30 O J

# 28 C B
# 29 C H
# 25 C D
# 24 A F
# 12 I N
# 26 K F
# 26 I D
# 22 G P
# 1 M J
# 23 G P
# 29 I L
