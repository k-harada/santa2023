import numpy as np
import pandas as pd
import os
from typing import List
from puzzle import Puzzle
import subprocess
import datetime
from itertools import permutations
from subprocess import PIPE
from rubik24.solve51 import solve_greed_51
from rubik24.solve51_diag import solve_greed_51 as solve_greed_51_diag
from magic612.solve61 import solve_greed_61
from rubik72.solve72 import align_pair_edges_with_center


os.chdir("../rubiks-cube-NxNxN-solver")


# for normal colored large cube
def kociemba_to_kaggle(s, n):
    base_dict = {
        "R": f"r0",
        "R2": f"r0.r0",
        "R'": f"-r0",
        "L": f"-r{n - 1}",
        "L2": f"r{n - 1}.r{n - 1}",
        "L'": f"r{n - 1}",
        "F": f"f0",
        "F2": f"f0.f0",
        "F'": f"-f0",
        "B": f"-f{n - 1}",
        "B2": f"f{n - 1}.f{n - 1}",
        "B'": f"f{n - 1}",
        "D": f"d0",
        "D2": f"d0.d0",
        "D'": f"-d0",
        "U": f"-d{n - 1}",
        "U2": f"d{n - 1}.d{n - 1}",
        "U'": f"d{n - 1}",
    }
    return base_dict[s]


v_map = {"A": "U", "B": "F", "C": "R", "D": "B", "E": "L", "F": "D"}


def move_translation(dim):
    M = {}
    M["U"] = f'-d{dim - 1}'
    M["R"] = "r0"
    M["B"] = f"-f{dim - 1}"
    M["F"] = "f0"
    M["L"] = f"-r{dim - 1}"
    M["D"] = "d0"

    if dim > 3:
        M["Uw"] = f'-d{dim - 2}.-d{dim - 1}'
        M["Rw"] = f"r0.r1"
        M["Bw"] = f'-f{dim - 2}.-f{dim - 1}'
        M["Fw"] = f"f0.f1"
        M["Lw"] = f'-r{dim - 2}.-r{dim - 1}'
        M["Dw"] = f"d0.d1"

    if dim >= 6:
        M["2Uw"] = f'-d{dim - 2}.-d{dim - 1}'
        M["2Rw"] = f"r0.r1"
        M["2Bw"] = f'-f{dim - 2}.-f{dim - 1}'
        M["2Fw"] = f"f0.f1"
        M["2Lw"] = f'-r{dim - 2}.-r{dim - 1}'
        M["2Dw"] = f"d0.d1"

        width_max = dim // 2
        for i in range(3, width_max + 1):
            M[f"{i}Uw"] = f'-d{dim - i}.' + M[f"{i - 1}Uw"]
            M[f"{i}Rw"] = M[f"{i - 1}Rw"] + f'.r{i - 1}'
            M[f"{i}Bw"] = f'-f{dim - i}.' + M[f"{i - 1}Bw"]
            M[f"{i}Fw"] = M[f"{i - 1}Fw"] + f'.f{i - 1}'
            M[f"{i}Lw"] = f'-r{dim - i}.' + M[f"{i - 1}Lw"]
            M[f"{i}Dw"] = M[f"{i - 1}Dw"] + f'.d{i - 1}'

    for m in list(M):
        M[m + "2"] = M[m] + '.' + M[m]
        if "-" in M[m]:
            M[m + "'"] = M[m].replace("-", "")
        else:
            M[m + "'"] = '.'.join(["-" + i for i in M[m].split('.')])

    return M


class RubiksCubeLarge:

    def __init__(
            self, puzzle_id: int, size: int, initial_state: List[str], solution_state: List[str],
            num_wildcards: int = 0
    ):
        assert size in [6, 8, 10]
        self.n = size
        self.cube = Puzzle(
            puzzle_id=puzzle_id, puzzle_type=f"cube_{size}/{size}/{size}",
            solution_state=solution_state,
            initial_state=initial_state,
            num_wildcards=0
        )
        self.m3 = move_translation(3)
        self.m4 = move_translation(4)
        self.m5 = move_translation(5)
        self.m6 = move_translation(6)
        self.count_solver_5 = 0
        self.count_start = 0
        self.count_41 = 0
        self.count_51 = 0
        self.count_61 = 0
        self.sub_cubes = None

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

        if len(self.cube.move_history) == 4:
            for _ in range(4):
                self.cube.undo()
            self.cube.operate(f"r{k}")
            self.cube.operate(f"r{k}")
        assert self.cube.state[a] == self.cube.solution_state[a]
        assert self.cube.state[a + n * n] == self.cube.solution_state[a + n * n]
        assert self.cube.state[a + 2 * n * n] == self.cube.solution_state[a + 2 * n * n]
        self.count_start = len(self.cube.move_history)
        return None

    def _check_center(self, centers: List[int]):
        n = self.n
        for z in range(6):
            check = []
            for i in centers:
                for j in centers:
                    check.append(self.cube.state[z * n * n + i * n + j])
            if len(set(check)) > 1:
                return False

        return True

    def _check_almost_done(self, ii: int):
        n = self.n
        m = (n - 1) // 2
        if not self._check_center([1, ii, m, n - 1 - ii, n - 2]):
            return False
        for z in range(6):
            check = []
            for p in [1, ii, m, n - 1 - ii, n - 2]:
                check.append(self.cube.state[z * n * n + p])
            if len(set(check)) > 1:
                return False
            check = []
            for p in [1, ii, m, n - 1 - ii, n - 2]:
                check.append(self.cube.state[z * n * n + p * p])
            if len(set(check)) > 1:
                return False
            check = []
            for p in [1, ii, m, n - 1 - ii, n - 2]:
                check.append(self.cube.state[z * n * n + p * n + (n - 1)])
            if len(set(check)) > 1:
                return False
            check = []
            for p in [1, ii, m, n - 1 - ii, n - 2]:
                check.append(self.cube.state[z * n * n + n * (n - 1) + p])
            if len(set(check)) > 1:
                return False

        return True

    def use_solver_4x4(self, ii: int, center_only: bool = True):
        n = self.n
        m = n // 2 - 1
        k = 4
        assert 0 < ii <= m
        pick_list = [0, ii, n - 1 - ii, n - 1]
        current_state_sub = []
        for z in range(6):
            for i in pick_list:
                for j in pick_list:
                    current_state_sub.append(self.cube.state[z * n * n + i * n + j])
        # transform
        nn = k * k
        res_list = []
        res_list = res_list + current_state_sub[:nn]
        res_list = res_list + current_state_sub[2 * nn:3 * nn]
        res_list = res_list + current_state_sub[nn:2 * nn]
        res_list = res_list + current_state_sub[5 * nn:]
        res_list = res_list + current_state_sub[4 * nn:5 * nn]
        res_list = res_list + current_state_sub[3 * nn:4 * nn]

        solver_input = "".join([v_map[r] for r in res_list])
        # print(solver_input)

        proc = subprocess.run(
            f"./rubiks-cube-solver.py --state {solver_input}",
            shell=True, stdout=PIPE, stderr=PIPE, text=True
        )
        # print(proc.stdout)
        action_list_solver = proc.stdout.split(": ")[1].split()
        action_list_dot = ".".join([self.m4[move] for move in action_list_solver])
        for action in action_list_dot.split("."):
            if action == "":
                continue
            # print(action)
            if action[-1] == "3":
                action_ = action[:-1] + str(n - 1)
            elif action[-1] == "2":
                action_ = action[:-1] + str(n - 1 - ii)
            elif action[-1] == "1":
                action_ = action[:-1] + str(ii)
            elif action[-1] == "0":
                action_ = action[:-1] + str(0)
            else:
                action_ = action
                print(action)
            self.cube.operate(action_)
            self.count_solver_5 += 1

        return None

    def use_solver_6x6(self, ii: int, center_only: bool = True):
        n = self.n
        m = n // 2 - 1
        k = 6
        assert 0 < ii <= m
        pick_list = [0, ii, m, m + 1, n - 1 - ii, n - 1]
        current_state_sub = []
        for z in range(6):
            for i in pick_list:
                for j in pick_list:
                    current_state_sub.append(self.cube.state[z * n * n + i * n + j])
        # transform
        nn = k * k
        res_list = []
        res_list = res_list + current_state_sub[:nn]
        res_list = res_list + current_state_sub[2 * nn:3 * nn]
        res_list = res_list + current_state_sub[nn:2 * nn]
        res_list = res_list + current_state_sub[5 * nn:]
        res_list = res_list + current_state_sub[4 * nn:5 * nn]
        res_list = res_list + current_state_sub[3 * nn:4 * nn]

        solver_input = "".join([v_map[r] for r in res_list])
        # print(solver_input)

        proc = subprocess.run(
            f"./rubiks-cube-solver.py --state {solver_input}",
            shell=True, stdout=PIPE, stderr=PIPE, text=True
        )
        print(proc.stdout)
        action_list_solver = proc.stdout.split(": ")[1].split()
        action_list_dot = ".".join([self.m6[move] for move in action_list_solver])
        for action in action_list_dot.split("."):
            if action == "":
                continue
            # print(action)
            if action[-1] == "5":
                action_ = action[:-1] + str(n - 1)
            elif action[-1] == "4":
                action_ = action[:-1] + str(n - 1 - ii)
            elif action[-1] == "3":
                action_ = action[:-1] + str(m + 1)
            elif action[-1] == "2":
                action_ = action[:-1] + str(m)
            elif action[-1] == "1":
                action_ = action[:-1] + str(ii)
            elif action[-1] == "0":
                action_ = action[:-1] + str(0)
            else:
                action_ = action
                print(action)
            self.cube.operate(action_)
            self.count_solver_5 += 1

        return None

    def get_subset_edge(self, i: int, j: int, with_center: bool = False):
        n = self.n
        m = (n - 1) // 2
        assert j < m
        assert i == 0
        current_state_sub = []
        goal_state_sub = []
        for z in range(6):
            current_state_sub.append(self.cube.state[z * n * n + i * n + j])
            goal_state_sub.append(self.cube.solution_state[z * n * n + i * n + j])
            if with_center:
                current_state_sub.append(self.cube.state[z * n * n + i * n + m])
                goal_state_sub.append(self.cube.solution_state[z * n * n + i * n + m])
            current_state_sub.append(self.cube.state[z * n * n + i * n + (n - 1 - j)])
            goal_state_sub.append(self.cube.solution_state[z * n * n + i * n + (n - 1 - j)])

            current_state_sub.append(self.cube.state[z * n * n + j * n + i])
            goal_state_sub.append(self.cube.solution_state[z * n * n + j * n + i])
            current_state_sub.append(self.cube.state[z * n * n + j * n + (n - 1 - i)])
            goal_state_sub.append(self.cube.solution_state[z * n * n + j * n + (n - 1 - i)])

            if with_center:
                current_state_sub.append(self.cube.state[z * n * n + m * n + i])
                goal_state_sub.append(self.cube.solution_state[z * n * n + m * n + i])
                current_state_sub.append(self.cube.state[z * n * n + m * n + (n - 1 - i)])
                goal_state_sub.append(self.cube.solution_state[z * n * n + m * n + (n - 1 - i)])

            current_state_sub.append(self.cube.state[z * n * n + (n - 1 - j) * n + i])
            goal_state_sub.append(self.cube.solution_state[z * n * n + (n - 1 - j) * n + i])
            current_state_sub.append(self.cube.state[z * n * n + (n - 1 - j) * n + (n - 1 - i)])
            goal_state_sub.append(self.cube.solution_state[z * n * n + (n - 1 - j) * n + (n - 1 - i)])

            current_state_sub.append(self.cube.state[z * n * n + (n - 1 - i) * n + j])
            goal_state_sub.append(self.cube.solution_state[z * n * n + (n - 1 - i) * n + j])
            if with_center:
                current_state_sub.append(self.cube.state[z * n * n + (n - 1 - i) * n + m])
                goal_state_sub.append(self.cube.solution_state[z * n * n + (n - 1 - i) * n + m])
            current_state_sub.append(self.cube.state[z * n * n + (n - 1 - i) * n + (n - 1 - j)])
            goal_state_sub.append(self.cube.solution_state[z * n * n + (n - 1 - i) * n + (n - 1 - j)])

        return current_state_sub, goal_state_sub

    def use_solver_fake_5x5_corner(self, ii: int, final: bool = False):
        n = self.n
        k = 5
        m = n // 2 - 1
        assert 0 < ii < m
        pick_list = [0, ii, m, n - 1 - ii, n - 1]
        current_state_sub = []
        for z in range(6):
            for i in pick_list:
                for j in pick_list:
                    if i == m and j in [ii, n - 1 - ii]:
                        current_state_sub.append(self.cube.solution_state[z * n * n + i * n + j])
                    elif i in [ii, n - 1 - ii] and j == m:
                        current_state_sub.append(self.cube.solution_state[z * n * n + i * n + j])
                    else:
                        current_state_sub.append(self.cube.state[z * n * n + i * n + j])

        # transform
        nn = k * k
        res_list = []
        res_list = res_list + current_state_sub[:nn]
        res_list = res_list + current_state_sub[2 * nn:3 * nn]
        res_list = res_list + current_state_sub[nn:2 * nn]
        res_list = res_list + current_state_sub[5 * nn:]
        res_list = res_list + current_state_sub[4 * nn:5 * nn]
        res_list = res_list + current_state_sub[3 * nn:4 * nn]

        solver_input = "".join([v_map[r] for r in res_list])
        # print(solver_input)

        proc = subprocess.run(
            f"./rubiks-cube-solver.py --state {solver_input}",
            shell=True, stdout=PIPE, stderr=PIPE, text=True
        )
        # success
        if ":" in proc.stdout:
            # print("success")
            action_list_solver = proc.stdout.split(": ")[1].split()
            action_list_dot = ".".join([self.m5[move] for move in action_list_solver])
            for action in action_list_dot.split("."):
                if action == "":
                    continue
                # print(action)
                if action[-1] == "4":
                    action_ = action[:-1] + str(n - 1)
                elif action[-1] == "3":
                    action_ = action[:-1] + str(n - 1 - ii)
                elif action[-1] == "2":
                    action_ = action[:-1] + str(m)
                elif action[-1] == "1":
                    action_ = action[:-1] + str(ii)
                elif action[-1] == "0":
                    action_ = action[:-1] + str(0)
                else:
                    action_ = action
                    print(action)
                self.cube.operate(action_)
                self.count_solver_5 += 1
                if not final:
                    if self._check_almost_done(ii):
                        break
            return None
        print("failure")
        return None

    def get_subset(self, i: int, j: int):
        n = self.n
        # assert max(i, j) <= (n - 1) // 2
        # assert i < (n - 1) // 2
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
        m = (n - 1) // 2
        # assert max(i, j) <= n - 1 - max(i, j)
        # assert i < n - 1 - i
        current_state_sub, goal_state_sub = self.get_subset(i, j)
        print(current_state_sub)
        if i == j:
            path = solve_greed_51_diag(current_state_sub, goal_state_sub)
            path = translate_51(path, n, i)
            print(path)
            for m in path:
                self.cube.operate(m)
                self.count_41 += 1
        else:
            path = solve_greed_61(current_state_sub, goal_state_sub)
            path = translate_61(path, n, i, j)
            print(path)
            for m in path:
                self.cube.operate(m)
                self.count_61 += 1


        print(self.cube.state)
        return None

    def print_face(self, c: int, i: int):
        n = self.n
        res = 0
        for x in range(i, n - i):
            p = n * n * c + x * n + i
            q = n * n * c + x * n + n - i
            print(self.cube.state[p:q])
        return res

    def get_sub_cubes(self):
        n = self.n
        m = (n - 1) // 2
        self.sub_cubes = [[] for _ in range(m)]
        for i in range(m):
            for j in range(m):
                if i == 0 or j == 0 or i == j:
                    current_state_sub = [f"S{x}" for x in range(24)]
                    goal_state_sub = [f"S{x}" for x in range(24)]
                else:
                    current_state_sub, goal_state_sub = self.get_subset(i, j)
                initial_state = ["X"] * (6 * 6 * 6)
                solution_state = ["X"] * (6 * 6 * 6)
                for c in range(6):
                    initial_state[6 * 6 * c + 8] = current_state_sub[4 * c + 0]
                    initial_state[6 * 6 * c + 16] = current_state_sub[4 * c + 1]
                    initial_state[6 * 6 * c + 19] = current_state_sub[4 * c + 2]
                    initial_state[6 * 6 * c + 27] = current_state_sub[4 * c + 3]
                    solution_state[6 * 6 * c + 8] = goal_state_sub[4 * c + 0]
                    solution_state[6 * 6 * c + 16] = goal_state_sub[4 * c + 1]
                    solution_state[6 * 6 * c + 19] = goal_state_sub[4 * c + 2]
                    solution_state[6 * 6 * c + 27] = goal_state_sub[4 * c + 3]
                sub_cube = Puzzle(
                    puzzle_id=self.cube.puzzle_id * 10000 + i * 100 + j, puzzle_type=f"cube_6/6/6",
                    solution_state=solution_state,
                    initial_state=initial_state,
                    num_wildcards=0
                )
                self.sub_cubes[i].append(sub_cube)
        return None

    def solve_inner_face(self):
        n = self.n
        m = (n - 1) // 2
        for i in range(1, m + 1):
            for j in range(1, m + 1):
                if i != j:
                    self.run_subset(i, j)
        for c in range(6):
            self.print_face(c, 0)
        print(self.cube.puzzle_id)
        print(len(self.cube.move_history))
        return None

    def solve(self):
        self.align_center()
        print(self.cube.move_history)
        self.solve_bone()
        self.solve_inner_face()
        return None


def translate_51(path, n, k):
    assert k < n - 1 - k
    mid = (n - 1) // 2
    res_path = []
    for m in path:
        if m[-1] == "4":
            res_path.append(m[:-1] + str(n - 1))
        elif m[-1] == "3":
            res_path.append(m[:-1] + str(n - 1 - k))
        elif m[-1] == "2":
            res_path.append(m[:-1] + str(mid))
        elif m[-1] == "1":
            res_path.append(m[:-1] + str(k))
        else:
            res_path.append(m)
    return res_path


def translate_61(path, n, i, j):
    # assert max(i, j) < n - 1 - max(i, j)
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


back = {
    "A": "F", "B": "A", "C": "B", "D": "C", "E": "D", "F": "E"
}


if __name__ == "__main__":
    puzzles_df = pd.read_csv("../input/puzzles.csv")
    _q = None
    _id_list = []
    _moves_list = []
    for _i, _row in puzzles_df.iterrows():
        if _row["puzzle_type"] == "cube_6/6/6":
            _n = 6
        elif _row["puzzle_type"] == "cube_8/8/8":
            _n = 8
        elif _row["puzzle_type"] == "cube_10/10/10":
            _n = 10
        else:
            continue
        _m = (_n - 1) // 2
        _q = RubiksCubeLarge(
            puzzle_id=_row["id"], size=_n,
            solution_state=list(_row["solution_state"].split(";")),
            initial_state=list(_row["initial_state"].split(";")),
            num_wildcards=_row["num_wildcards"]
        )
        if _q.cube.solution_state[1] != "A":
            continue

        _q.use_solver_4x4(_m)
        for j in range(_m - 1, 1, -1):
            _q.use_solver_fake_5x5_corner(j, final=False)
        _q.use_solver_fake_5x5_corner(1, final=True)

        # print(_row["id"], len(_q.cube.move_history))

        _q.solve_inner_face()
        assert _q.cube.state == _q.cube.solution_state
        print(_row["id"], len(_q.cube.move_history))
        _id_list.append(_row["id"])
        _moves_list.append(".".join(_q.cube.move_history))
        print(_q.cube.puzzle_id, _q.count_solver_5, _q.count_41, _q.count_61, _q.count_start)

    dt_now = datetime.datetime.now()
    pd.DataFrame(
        {"id": _id_list, "moves": _moves_list}
    ).to_csv(f"../output/cube_6_8_10_{dt_now.strftime('%Y-%m-%d-%H:%M')}.csv", index=False)