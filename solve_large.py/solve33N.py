import numpy as np
import pandas as pd
from typing import List
from puzzle import Puzzle

from rubik24.solve41 import solve_greed_41
from rubik24.solve51 import solve_greed_51
from rubik24.solve61 import solve_greed_61


class RubiksCubeLarge:

    def __init__(
            self, puzzle_id: int, size: int, initial_state: List[str], solution_state: List[str],
            num_wildcards: int = 0
    ):
        self.n = size
        self.cube = Puzzle(
            puzzle_id=puzzle_id, puzzle_type=f"cube_{size}/{size}/{size}",
            solution_state=solution_state,
            initial_state=initial_state,
            num_wildcards=0
        )

    def align_center(self):
        n = self.n
        if n % 2 == 0:
            print("No Center")
            return None
        k = (n - 1) // 2
        a = (n ** 2 - 1) // 2
        # greedy
        if self.cube.state[a] != self.cube.solution_state[a]:
            for m in [f"f{k}", f"-f{k}", f"r{k}", f"-r{k}"]:
                self.cube.operate(m)
                if self.cube.state[a] == self.cube.solution_state[a]:
                    break
                else:
                    self.cube.undo()
            else:
                self.cube.operate(f"f{k}")
                self.cube.operate(f"f{k}")
        if self.cube.state[a + n * n] != self.cube.solution_state[a + n * n]:
            for m in [f"d{k}", f"-d{k}"]:
                self.cube.operate(m)
                if self.cube.state[a + n * n] == self.cube.solution_state[a + n * n]:
                    break
                else:
                    self.cube.undo()
            else:
                self.cube.operate(f"d{k}")
                self.cube.operate(f"d{k}")

    def get_subset(self, i: int, j: int):
        n = self.n
        assert max(i, j) <= (n - 1) // 2
        assert i < (n - 1) // 2
        current_state_sub = []
        goal_state_sub = []
        for z in range(6):
            current_state_sub.append(self.cube.state[z * n * n + i * n + j])
            goal_state_sub.append(self.cube.solution_state[z * n * n + i * n + j])
            if j * 2 == n - 1:
                current_state_sub.append(self.cube.state[z * n * n + (n - 1 - j) * n + i])
                goal_state_sub.append(self.cube.solution_state[z * n * n + (n - 1 - j) * n + i])
                current_state_sub.append(self.cube.state[z * n * n + j * n + (n - 1 - i)])
                goal_state_sub.append(self.cube.solution_state[z * n * n + j * n + (n - 1 - i)])
            else:
                current_state_sub.append(self.cube.state[z * n * n + j * n + (n - 1 - i)])
                goal_state_sub.append(self.cube.solution_state[z * n * n + j * n + (n - 1 - i)])
                current_state_sub.append(self.cube.state[z * n * n + (n - 1 - j) * n + i])
                goal_state_sub.append(self.cube.solution_state[z * n * n + (n - 1 - j) * n + i])

            current_state_sub.append(self.cube.state[z * n * n + (n - 1 - i) * n + (n - 1 - j)])
            goal_state_sub.append(self.cube.solution_state[z * n * n + (n - 1 - i) * n + (n - 1 - j)])
        return current_state_sub, goal_state_sub

    def run_subset(self, i: int, j: int):
        n = self.n
        assert max(i, j) <= n - 1 - max(i, j)
        assert i < n - 1 - i
        if i == j:
            # ここは賢い方法に変えたい
            print(i)
            if n == 33:
                if i in [14, 13, 12, 11, 6, 5, 4, 2]:
                    self.cube.operate(f"r{i}")
            elif n == 5:
                if i == 1:
                    self.cube.operate(f"r{i}")
            if i + 1 == n - 1 - i - 1:
                first_flag = True
            else:
                first_flag = False
            current_state_sub, goal_state_sub = self.get_subset(i, i)
            path = solve_greed_41(current_state_sub, goal_state_sub, two_side=True, first=first_flag)
            path = translate_41(path, n, i)
            print(path)
            for m in path:
                self.cube.operate(m)
            print(self.cube.state)
        elif 2 * j == n - 1:
            current_state_sub, goal_state_sub = self.get_subset(i, j)
            print(current_state_sub)
            path = solve_greed_51(current_state_sub, goal_state_sub)
            path = translate_51(path, n, i, j)
            print(path)
            for m in path:
                self.cube.operate(m)
            print(self.cube.state)
        else:
            current_state_sub, goal_state_sub = self.get_subset(i, j)
            print(current_state_sub)
            path = solve_greed_61(current_state_sub, goal_state_sub)
            path = translate_61(path, n, i, j)
            print(path)
            for m in path:
                self.cube.operate(m)
            print(self.cube.state)
        return None


def translate_41(path, n, k):
    assert k < n - 1 - k
    res_path = []
    for m in path:
        if m[-1] == "3":
            res_path.append(m[:-1] + str(n - 1))
        elif m[-1] == "2":
            res_path.append(m[:-1] + str(n - 1 - k))
        elif m[-1] == "1":
            res_path.append(m[:-1] + str(k))
        else:
            res_path.append(m)
    return res_path


def translate_51(path, n, i, j):
    assert i < j
    assert j == n - 1 - j
    res_path = []
    for m in path:
        if m[-1] == "4":
            res_path.append(m[:-1] + str(n - 1))
        elif m[-1] == "3":
            res_path.append(m[:-1] + str(n - 1 - i))
        elif m[-1] == "2":
            res_path.append(m[:-1] + str(j))
        elif m[-1] == "1":
            res_path.append(m[:-1] + str(i))
        else:
            res_path.append(m)
    return res_path


def translate_61(path, n, i, j):
    assert max(i, j) < n - 1 - max(i, j)
    res_path = []
    for m in path:
        if m[-1] == "5":
            res_path.append(m[:-1] + str(n - 1))
        elif m[-1] == "4":
            res_path.append(m[:-1] + str(n - 1 - i))
        elif m[-1] == "3":
            res_path.append(m[:-1] + str(n - 1 - j))
        elif m[-1] == "2":
            res_path.append(m[:-1] + str(j))
        elif m[-1] == "1":
            res_path.append(m[:-1] + str(i))
        else:
            res_path.append(m)
    return res_path


if __name__ == "__main__":
    _n = 5
    assert _n % 2 == 1
    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == f"cube_{_n}/{_n}/{_n}"]
    _q = None
    for _i, _row in puzzles_df_pick.iterrows():
        if _row["solution_state"].split(";")[1] != "N1":
            continue
        _q = RubiksCubeLarge(
            puzzle_id=_row["id"], size=_n,
            solution_state=list(_row["solution_state"].split(";")),
            initial_state=list(_row["initial_state"].split(";")),
            num_wildcards=_row["num_wildcards"]
        )
    _q.align_center()
    print(_q.cube.move_history)
    _m = (_n - 1) // 2
    for _i in range(_m - 1, 0, -1):
        for _j in range(_i, _m + 1):
            _q.run_subset(_i, _j)
            if _i != _j and _j != _m:
                _q.run_subset(_j, _i)
    print(len(_q.cube.move_history))
