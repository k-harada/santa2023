import numpy as np
import pandas as pd
from typing import List
from puzzle import Puzzle
from heapq import heappop, heappush
from collections import deque
from datetime import datetime

from magic612.magic3 import Magic3, magic3, magic_from_command
from rubik_large.magic61 import magic61
from rubik_large.large_cube import RubiksCubeLarge
from rubik_large.solve61_parallel import MultiCube


def parse_magic(path):
    count_dict = dict()
    cnt_nonzero = 0
    parsed_path = [[]]
    for mv in path:
        if mv[0] != "-":
            mv_ = mv
            v = 1
        else:
            mv_ = mv[1:]
            v = -1

        if mv_ not in count_dict.keys():
            count_dict[mv_] = v
            cnt_nonzero += 1
        else:
            if count_dict[mv_] == 0:
                cnt_nonzero += 1
            count_dict[mv_] += v
            if count_dict[mv_] == 0:
                cnt_nonzero -= 1
        # print(mv, mv_, cnt_nonzero)
        parsed_path[-1].append(mv)
        if cnt_nonzero == 0:
            parsed_path.append([])
    return parsed_path[:-1]


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

back = {
    "A": "F", "B": "A", "C": "B", "D": "C", "E": "D", "F": "E"
}


class Shiritori:

    def __init__(self, n: int, p: Puzzle):
        self.n = n
        self.cube = p
        self.score = self.eval_score()

    def eval_score(self):
        score = 0
        for x, y in zip(self.cube.state, self.cube.solution_state):
            if x != y:
                score += 1
        return score

    def try_magic(self, magic: List[str]):
        base_score = self.score
        for mv in magic:
            self.cube.operate(mv)
        new_score = self.eval_score()
        for mv in magic:
            self.cube.undo()
        return new_score - base_score

    def random_magic(self):
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
        r = np.random.choice(2)
        d3 = d2
        if r == 1:
            for x in ["r", "d", "f"]:
                if x != d1 and x != d2:
                    d3 = x
        # add -
        r = np.random.choice(8)
        if r & 4:
            d1 = "-" + d1
        if r & 2:
            d2 = "-" + d2
        if r & 1:
            d3 = "-" + d3

        # add number
        r = np.random.choice(2)
        if r == 0:
            d1 = d1 + "0"
        else:
            d1 = d1 + str(self.n - 1)

        n2, n3 = np.random.choice(range(1, n - 1), 2, False)
        d2 = d2 + str(n2)
        d3 = d3 + str(n3)

        return magic3(n, d1, d2, d3, reverse=True)

    def next_magic_random(self, m: Magic3):
        n = self.n
        assert n >= 4
        if not m.rev:
            r = np.random.choice(2)
            d3 = m.dim2
            if r == 1:
                for x in ["r", "d", "f"]:
                    if x != m.dim1 and x != m.dim2:
                        d3 = x
            r = np.random.choice(2)
            if r == 1:
                d3 = "-" + d3
            if m.flag2 == 1:
                v2 = int(m.m2[1:])
            else:
                v2 = int(m.m2[2:])
            while True:
                v = np.random.choice(range(1, n - 1))
                if v != v2:
                    d3 = d3 + str(v)
                    break
            new_magic = magic3(n, m.m1, m.m2, d3, reverse=True)
            return new_magic
        else:
            r = np.random.choice(2)
            d2 = m.dim3
            if r == 1:
                for x in ["r", "d", "f"]:
                    if x != m.dim1 and x != m.dim3:
                        d2 = x
            r = np.random.choice(2)
            if r == 1:
                d2 = "-" + d2

            if m.flag3 == 1:
                v3 = int(m.m3[1:])
            else:
                v3 = int(m.m3[2:])
            while True:
                v = np.random.choice(range(1, n - 1))
                if v != v3:
                    d2 = d2 + str(v)
                    break
            new_magic = magic3(n, m.m1, d2, m.m3, reverse=False)
            return new_magic

    def run_shiritori(self):
        t = 0
        n = self.n
        best_magic = []
        best_res = 0
        for _ in range(1000):
            random_magic = _s.random_magic()
            res = self.try_magic(random_magic)
            if res < best_res:
                best_res = res
                best_magic = random_magic
        if best_res == 0:
            print(t, self.score)
            print("No More Shiritori")
            return None
        else:
            # print(best_res)
            pass
        for mv in best_magic:
            self.cube.operate(mv)
        self.score = self.eval_score()
        t += 1

        last_magic = magic_from_command(n, best_magic)

        while True:
            best_res = 0
            for _ in range(100):
                random_magic = _s.next_magic_random(last_magic)
                res = self.try_magic(random_magic)
                if res < best_res:
                    best_res = res
                    best_magic = random_magic
            if best_res == 0:
                print(t, self.score)
                m0 = self.cube.move_history[-1]
                if m0[0] == "-":
                    v0 = int(m0[2:])
                else:
                    v0 = int(m0[1:])
                if v0 in [0, n - 1]:
                    print("Shiritori End")
                else:
                    print("Shiritori End")
                return None
            else:
                # print(best_res)
                pass
            for mv in best_magic:
                self.cube.operate(mv)
            self.score = self.eval_score()
            t += 1
            last_magic = magic_from_command(n, best_magic)

        return None


c_list = ["A", "B", "C", "D", "E", "F"]


if __name__ == "__main__":
    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[(puzzles_df["id"] == 283)]
    _q = None

    for _ii, _row in puzzles_df_pick.iterrows():
        _n = 33
        _m = (_n - 1) // 2
        _q = RubiksCubeLarge(
            puzzle_id=_row["id"], size=_n,
            solution_state=list(_row["solution_state"].split(";")),
            initial_state=list(_row["initial_state"].split(";")),
            num_wildcards=_row["num_wildcards"]
        )

        # solve dummy
        solution_state_dummy = []
        initial_state_dummy = []
        for _j, (_x, _y) in enumerate(zip(_q.cube.state, _q.cube.solution_state)):
            _xi = int(_x[1:])
            _yi = int(_y[1:])
            initial_state_dummy.append(c_list[_xi // (_n * _n)])
            solution_state_dummy.append(c_list[_yi // (_n * _n)])
        _p = RubiksCubeLarge(
            puzzle_id=_row["id"], size=_n,
            solution_state=solution_state_dummy,
            initial_state=initial_state_dummy,
            num_wildcards=_row["num_wildcards"]
        )
        _p.align_center()
        _p.solve_bone()

        print(len(_p.cube.move_history))
        for _m in _p.cube.move_history:
            _q.cube.operate(_m)

        _s = Shiritori(_n, _q.cube)
        print(_s.score)
        for _t in range(500):
            print(_t)
            _s.run_shiritori()

        _m = (_n - 1) // 2
        _path_list = [[] for _ in range(200)]
        for _i in range(1, _m):
            for _j in range(1, _m + 1):
                if _i != _j and _j != _m:
                    continue
                _path = _q.run_subset(_i, _j, only_path=True)
                # print(_path)
                _parsed_path = parse_magic(_path)
                # print(_parsed_path)
                for _k, _path in enumerate(_parsed_path):
                    _path_list[_k] = _path_list[_k] + _path
        for _i in range(1, _m):
            for _j in range(_i + 1, _m):
                _path = _q.run_subset_2(_i, _j, only_path=True)
                # print(_path)
                _parsed_path = parse_magic(_path)
                # print(_parsed_path)
                for _k, _path in enumerate(_parsed_path):
                    _path_list[_k] = _path_list[_k] + _path
        for _path in _path_list:
            for _mv in _path:
                _q.cube.operate(_mv)
        print(_row["id"], len(_q.cube.move_history))

    print(_q.cube.puzzle_id, _p.count_solver_5, _q.count_41, _q.count_51, _q.count_61, _p.count_start)
    for _i, (_x, _y) in enumerate(zip(_q.cube.state, _q.cube.solution_state)):
        if _x != _y:
            print(_i, _x, _y)
    assert _q.cube.state == _q.cube.solution_state
    _id_list = [283]
    _moves_list = [".".join(_q.cube.move_history)]
    pd.DataFrame(
        {"id": _id_list, "moves": _moves_list}
    ).to_csv(f"../output/large-283_shiritori_{len(_q.cube.move_history)}.csv", index=False)

