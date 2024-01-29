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

        double_int = 0
        r = np.random.choice(3)
        if r == 0:
            double_int += 1
        r = np.random.choice(3)
        if r == 0:
            double_int += 2

        return magic3(n, d1, d2, d3, reverse=True, double_int=double_int)

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
            v = np.random.choice(range(1, n - 1))
            d3 = d3 + str(v)

            double_int = 0
            if m.double_int >= 2:
                double_int += 2
            r = np.random.choice(3)
            if r == 0:
                double_int += 1

            new_magic = magic3(n, m.m1, m.m2, d3, reverse=True, double_int=double_int)
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
            v = np.random.choice(range(1, n - 1))
            d2 = d2 + str(v)

            double_int = 0
            if m.double_int % 2 == 1:
                double_int += 1
            r = np.random.choice(3)
            if r == 0:
                double_int += 2

            new_magic = magic3(n, m.m1, d2, m.m3, reverse=False, double_int=double_int)
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
                    self.cube.undo()
                    self.score = self.eval_score()
                    print("Shiritori End, Undo")
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


if __name__ == "__main__":

    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[(puzzles_df["id"] >= 267) & (puzzles_df["id"] < 283)]

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
        _q.solve_bone(no_last=True)

        # _q.get_sub_cubes()
        # mc = MultiCube(_q.sub_cubes)
        # print(sum([sum(_s) for _s in mc.score_list]))

        # for _ in range(100):
        #     mc.random_magic_large()
        #     print("---")
        # continue

        # res = mc.loop_random(1000, 2.5)
        # print(res)
        # res = mc.loop_random(1000, 3.0)
        # print(res)

        # for _move in mc.move_history:
        #     _q.cube.operate(_move)

        _s = Shiritori(_n, _q.cube)
        print(_s.score)
        for _t in range(100):
            print(_t)
            _s.run_shiritori()

        _q.solve_3x3()
        _q.solve_inner_face()
        print(_row["id"], len(_q.cube.move_history))
        _id_list.append(_row["id"])
        _moves_list.append(".".join(_q.cube.move_history))

    dt_now = datetime.now()
    pd.DataFrame(
        {"id": _id_list, "moves": _moves_list}
    ).to_csv(f"../output/shiritori_temp_{dt_now.strftime('%Y-%m-%d-%H:%M')}.csv", index=False)
