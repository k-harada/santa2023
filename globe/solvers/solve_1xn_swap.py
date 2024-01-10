from typing import List, Dict, Optional

from sympy.combinatorics import Permutation


class SwapSolver:

    def __init__(self, n: int):
        self.n: int = n
        self.allowed_moves: Dict[str, Permutation] = dict()
        self.allowed_moves["r0"] = Permutation(list(range(1, 2 * n)) + [0] + list(range(2 * n, 4 * n)))
        self.allowed_moves["-r0"] = self.allowed_moves["r0"] ** (-1)
        self.allowed_moves["r1"] = Permutation(list(range(2 * n)) + list(range(2 * n + 1, 4 * n)) + [2 * n])
        self.allowed_moves["-r1"] = self.allowed_moves["r1"] ** (-1)
        self.allowed_moves[f"f{n}"] = Permutation(
            list(range(n)) + list(range(4 * n - 1, 3 * n - 1, -1)) + list(range(2 * n, 3 * n)) + list(
                range(2 * n - 1, n - 1, -1))
        )
        self.state: Optional[List[str]] = None
        self.initial_state: Optional[List[str]] = None
        self.goal_state: Optional[List[str]] = None
        self.path: List[str] = []
        self.aligned = False

    def operate(self, m: str):
        self.state = (self.allowed_moves[m])(self.state)
        self.path.append(m)

    def operate_list(self, m_list: List[str]):
        for m in m_list:
            self.operate(m)

    def initialize(self, initial_state: List[str], goal_state: List[str]):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.state = initial_state.copy()
        self.path = []
        self.aligned = False
        return None

    def solve(self):
        n = self.n
        self.align_up_down()
        h_up, h_low = self.heuristic(self.state[:2 * n], self.state[2 * n:])
        while max(h_up, h_low) > 0:
            d, ui, li = self.find_max_swap()
            self.run_swap(d, ui, li)
            h_up, h_low = self.heuristic(self.state[:2 * n], self.state[2 * n:])
            print(h_up, h_low)
            print(self.state)
        return None

    def align_up_down(self):
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
            while self.state[2 * n - 1] in upper_set:
                self.operate("-r0")
            while self.state[2 * n] in lower_set:
                self.operate("r1")
            c = 0
            for i in range(n):
                if self.state[2 * n - 1 - i] in lower_set and self.state[2 * n + i] in upper_set:
                    c += 1
                else:
                    break
            # print(c)
            self.operate_list([f"f{n}"] + ['r1'] * c + [f"f{n}"])

            mismatch = 0
            for i in range(2 * n):
                if self.state[i] in lower_set:
                    mismatch += 1
        self.aligned = True
        return None

    def find_max_swap(self):
        assert self.aligned
        n = self.n
        h_min = 10 ** 9
        d_min = -1
        ui = -1
        li = -1
        for d in range(1, n + 1):
            best_uh = 10 ** 9
            best_ui = -1
            for i in range(2 * n):
                base_list = self.state[i:2 * n] + self.state[:i]
                h_up, _ = self.heuristic(
                    [base_list[d]] + base_list[1:d] + [base_list[0]] + base_list[d + 1:],
                    self.state[2 * n:]
                )
                if h_up < best_uh:
                    best_uh = h_up
                    best_ui = i

            best_lh = 10 ** 9
            best_li = -1
            for i in range(2 * n):
                base_list = self.state[2 * n + i:4 * n] + self.state[2 * n:2 * n + i]
                _, h_low = self.heuristic(
                    self.state[:2 * n],
                    [base_list[d]] + base_list[1:d] + [base_list[0]] + base_list[d + 1:]
                )
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
        print(h_min, d_min, ui, li)
        return d_min, ui, li

    def run_swap(self, d, ui, li):
        n = self.n
        # ui -> n - 1
        if ui < n:
            self.operate_list(["-r0"] * (n - 1 - ui))
        else:
            self.operate_list(["r0"] * (ui - (n - 1)))
        # li + d -> n
        lid = (li + d) % (2 * n)
        if lid <= n:
            self.operate_list(["-r1"] * (n - lid))
        else:
            self.operate_list(["r1"] * (lid - n))
        # print(self.state)
        self.operate_list(
            [f"f{n}", "-r0"] + ["-r1"] * (d - 1) + [f"f{n}", "r0", "-r1", f"f{n}"] + ["r1"] * d + [f"f{n}"]
        )

    def heuristic(self, upper_list, lower_list):
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


if __name__ == "__main__":
    solver = SwapSolver(4)
    solver.initialize([str(i) for i in range(8, 16)] + [str(i) for i in range(8)], [str(i) for i in range(16)])
    solver.solve()
    print(solver.state)
    print(solver.path)
