import numpy as np
import pandas as pd
from typing import List
from puzzle import Puzzle
from heapq import heappop, heappush
from collections import deque
from datetime import datetime

from rubik_large.magic61 import magic61
from rubik_large.large_cube import RubiksCubeLarge


def parse_command(m: str):
    if m[-2].isdigit():
        num = int(m[-2:])
        command = m[:-2]
    else:
        num = int(m[-1])
        command = m[:-1]
    if command[0] == "-":
        sign = "-"
        rot = command[1]
    else:
        sign = ""
        rot = command[0]
    return sign, rot, num


class MultiCube:

    def __init__(self, cube_list: List[List[Puzzle]]):
        self.cube_list = cube_list
        self.m = len(cube_list)
        self.n = self.m * 2 + 1
        self.move_history = []
        self.score_list = [[0] * self.m for _ in range(self.m)]
        self.eval_score()

    def operate(self, move: str):
        n = self.n
        m = self.m
        sign, rot, num = parse_command(move)
        if num == 0 or num == n - 1:
            if num == 0:
                move_ = move
            else:
                move_ = f"{sign}{rot}{5}"
            for i in range(m):
                for j in range(m):
                    self.cube_list[i][j].operate(move_)
        elif num < m:
            move_ = f"{sign}{rot}{1}"
            for j in range(m):
                self.cube_list[num][j].operate(move_)
            move_ = f"{sign}{rot}{2}"
            for i in range(m):
                self.cube_list[i][num].operate(move_)
        elif num > m:
            move_ = f"{sign}{rot}{4}"
            for j in range(m):
                self.cube_list[n - 1 - num][j].operate(move_)
            move_ = f"{sign}{rot}{3}"
            for i in range(m):
                self.cube_list[i][n - 1 - num].operate(move_)
        else:
            pass
        self.move_history.append(move)
        return None

    def undo(self):
        assert len(self.move_history) > 0
        move = self.move_history.pop()
        n = self.n
        m = self.m
        sign, rot, num = parse_command(move)
        if num == 0 or num == n - 1:
            for i in range(m):
                for j in range(m):
                    self.cube_list[i][j].undo()
        elif num < m:
            for j in range(m):
                self.cube_list[num][j].undo()
            for i in range(m):
                self.cube_list[i][num].undo()
        elif num > m:
            for j in range(m):
                self.cube_list[n - 1 - num][j].undo()
            for i in range(m):
                self.cube_list[i][n - 1 - num].undo()
        else:
            pass

    def loop_random(self, n_try: int = 100, bar: float = 4.0):
        s_sum = 0
        len_sum = 0
        for t in range(n_try):
            s, magic = self.random_magic()
            if len(magic) > 0:
                if len(magic) <= s * bar:
                    for move in magic:
                        mc.operate(move)
                    # print(s)
                    s_sum += s
                    len_sum += len(magic)
                    print(t, s_sum, len_sum)
        return s_sum, len_sum

    def eval_score(self):
        m = self.m
        for i in range(m):
            for j in range(m):
                q = self.cube_list[i][j]
                r = 0
                for x, y in zip(q.state, q.solution_state):
                    if x != y:
                        r += 1
                self.score_list[i][j] = r
        return None

    def random_magic(self):
        n = self.n
        j = np.random.choice(n - 2) + 1
        d12 = np.random.choice(6)
        if d12 == 0:
            d1, d2 = "r", "d"
        elif d12 == 1:
            d1, d2 = "r", "f"
        elif d12 == 2:
            d1, d2 = "d", "f"
        elif d12 == 3:
            d1, d2 = "d", "r"
        elif d12 == 4:
            d1, d2 = "f", "d"
        else:
            d1, d2 = "f", "r"
        flag_int = np.random.choice(4)
        rev = np.random.choice([True, False])
        diag = np.random.choice([True, False])
        add = np.random.choice(4)
        score, magic = self.try_magic(j, d1, d2, flag_int, rev=rev, diag=diag, add=add)
        # print(score, len(magic))
        return score, magic

    def random_magic_large(self):
        n = self.n
        d12 = np.random.choice(6)
        if d12 == 0:
            d1, d2 = "r", "d"
        elif d12 == 1:
            d1, d2 = "r", "f"
        elif d12 == 2:
            d1, d2 = "d", "f"
        elif d12 == 3:
            d1, d2 = "d", "r"
        elif d12 == 4:
            d1, d2 = "f", "d"
        else:
            d1, d2 = "f", "r"
        flag_int = np.random.choice(4)
        rev = np.random.choice([True, False])
        diag = np.random.choice([True, False])
        add = np.random.choice(4)
        self.try_magic_large(d1, d2, flag_int, rev=rev, diag=diag, add=add)
        # print(score, len(magic))
        return None

    def try_magic(self, j: int, d1: str, d2: str, flag_int: int = 0, rev: bool = False, diag: bool = False, add: int = 0):
        n = self.n
        m = (n - 1) // 2
        self.eval_score()
        base_score = sum([sum(self.score_list[ii]) for ii in range(m)])
        res_list = [0] * (n - 1)
        v_list = [0] * (n - 1)
        for i in range(1, n - 1):
            if i == j or i + j == n - 1:
                continue
            try_magic = magic61(k_list=[i], m=j, n=n, d1=d1, d2=d2, flag_int=flag_int, rev=rev, diag=diag, add=add, rev_i=False)
            # print(try_magic)
            for move in try_magic:
                self.operate(move)
            self.eval_score()
            new_score = sum([sum(self.score_list[ii]) for ii in range(m)])
            for _ in try_magic:
                self.undo()
            if new_score < base_score:
                res_list[i] = 1
                v_list[i] = base_score - new_score

        for i in range(1, n - 1):
            if i == j or i + j == n - 1:
                continue
            try_magic = magic61(k_list=[i], m=j, n=n, d1=d1, d2=d2, flag_int=flag_int, rev=rev, diag=diag, add=add, rev_i=True)
            # print(try_magic)
            for move in try_magic:
                self.operate(move)
            self.eval_score()
            new_score = sum([sum(self.score_list[ii]) for ii in range(m)])
            for _ in try_magic:
                self.undo()
            if new_score < base_score - v_list[i]:
                res_list[i] = -1
                v_list[i] = base_score - new_score
        # print(res_list)
        # print(v_list)
        # print(sum(v_list))
        k_list = []
        for i in range(1, n - 1):
            if res_list[i] != 0:
                k_list.append(i * res_list[i])
        # print(k_list)
        if len(k_list) == 0:
            return 0, []
        return sum(v_list), magic61(k_list=k_list, m=j, n=n, d1=d1, d2=d2, flag_int=flag_int, rev=rev, diag=diag, add=add, rev_i=False)

    def try_magic_large(self, d1: str, d2: str, flag_int: int = 0, rev: bool = False, diag: bool = False, add: int = 0):
        n = self.n
        m = (n - 1) // 2
        self.eval_score()
        base_score = sum([sum(self.score_list[ii]) for ii in range(m)])
        res_list_1 = [[0] * (n - 1) for _ in range(n - 1)]
        res_list_2 = [[0] * (n - 1) for _ in range(n - 1)]
        for i in range(1, n - 1):
            for j in range(1, n - 1):
                if i == j or i + j == n - 1:
                    continue
                try_magic = magic61(k_list=[i], m=j, n=n, d1=d1, d2=d2, flag_int=flag_int, rev=rev, diag=diag, add=add, rev_i=False)
                # print(try_magic)
                for move in try_magic:
                    self.operate(move)
                self.eval_score()
                new_score = sum([sum(self.score_list[ii]) for ii in range(m)])
                for _ in try_magic:
                    self.undo()
                res_list_1[i][j] = base_score - new_score

        for i in range(1, n - 1):
            for j in range(1, n - 1):
                if i == j or i + j == n - 1:
                    continue
                try_magic = magic61(k_list=[i], m=j, n=n, d1=d1, d2=d2, flag_int=flag_int, rev=rev, diag=diag, add=add, rev_i=True)
                # print(try_magic)
                for move in try_magic:
                    self.operate(move)
                self.eval_score()
                new_score = sum([sum(self.score_list[ii]) for ii in range(m)])
                for _ in try_magic:
                    self.undo()
                res_list_2[i][j] = base_score - new_score
        print(res_list_1)
        print(res_list_2)
        return None

back = {
    "A": "F", "B": "A", "C": "B", "D": "C", "E": "D", "F": "E"
}


if __name__ == "__main__":

    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[(puzzles_df["id"] >= 281) & (puzzles_df["id"] < 283)]

    _id_list = []
    _moves_list = []

    _q = None
    for _i, _row in puzzles_df_pick.iterrows():
        if _row["id"] < 272:
            _n = 9
        elif _row["id"] < 277:
            _n = 10
            continue
        elif _row["id"] < 281:
            _n = 19
        else:
            _n = 33
        _m = (_n - 1) // 2
        if _row["id"] != 282:
            _q = RubiksCubeLarge(
                puzzle_id=_row["id"], size=_n,
                solution_state=list(_row["solution_state"].split(";")),
                initial_state=list(_row["initial_state"].split(";")),
                num_wildcards=_row["num_wildcards"]
            )
        else:
            _initial_state = []
            _solution_state = []
            for _ijk, (_x, _y) in enumerate(zip(
                    list(_row["initial_state"].split(";")),
                    list(_row["solution_state"].split(";"))
            )):
                _uv, _w = _ijk % (_n * _n), _ijk // (_n * _n)
                _u, _v = _uv // _n, _uv % _n
                if (_u + _v) % 2 == 0:
                    _initial_state.append(_x)
                    _solution_state.append(_y)
                else:
                    _initial_state.append(back[_x])
                    _solution_state.append(back[_y])
            _q = RubiksCubeLarge(
                puzzle_id=_row["id"], size=_n,
                solution_state=_solution_state,
                initial_state=_initial_state,
                num_wildcards=_row["num_wildcards"]
            )
        _q.align_center()
        _q.solve_bone()
        _q.get_sub_cubes()
        mc = MultiCube(_q.sub_cubes)
        print(sum([sum(_s) for _s in mc.score_list]))

        # for _ in range(100):
        #     mc.random_magic_large()
        #     print("---")
        # continue

        res = mc.loop_random(10000, 2.5)
        print(res)
        res = mc.loop_random(1000, 3.0)
        print(res)

        for _move in mc.move_history:
            _q.cube.operate(_move)

        _q.solve_inner_face()
        print(_row["id"], len(_q.cube.move_history))
        _id_list.append(_row["id"])
        _moves_list.append(".".join(_q.cube.move_history))

    dt_now = datetime.now()
    pd.DataFrame(
        {"id": _id_list, "moves": _moves_list}
    ).to_csv(f"../output/parallel_temp_{dt_now.strftime('%Y-%m-%d-%H:%M')}.csv", index=False)
# 281 2559 0 23634 2 26195
# 4217
# (2629, 5872)
# 281 17837

