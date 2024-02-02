import numpy as np
import pandas as pd
import os
from typing import List
from puzzle import Puzzle
import subprocess
from subprocess import PIPE
from heapq import heappop, heappush
from collections import deque
from datetime import datetime


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


m5 = move_translation(5)


def use_solver_5x5_corner(n: int, ii: int, state: List[str], final: bool = False):
    k = 5
    m = (n - 1) // 2
    assert 0 < ii < m
    pick_list = [0, ii, m, n - 1 - ii, n - 1]
    current_state_sub = []
    for z in range(6):
        for i in pick_list:
            for j in pick_list:
                current_state_sub.append(state[z * n * n + i * n + j])
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
    action_list_dot = ".".join([m5[move] for move in action_list_solver])
    action_list = list(action_list_dot.split("."))

    return action_list


if __name__ == "__main__":

    _n = 5
    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == f"cube_{_n}/{_n}/{_n}"]

    for _i, _row in puzzles_df_pick.iterrows():
        _q5 = Puzzle(
            puzzle_id=_row["id"], puzzle_type=f"cube_{_n}/{_n}/{_n}",
            solution_state=list(_row["solution_state"].split(";")),
            initial_state=list(_row["initial_state"].split(";")),
            num_wildcards=0
        )
        _initial_state = list(_row["initial_state"].split(";"))
        _goal_state = list(_row["solution_state"].split(";"))
        if _initial_state[1] != "A":
            continue

        res = use_solver_5x5_corner(5, 1, _initial_state)
        print(_i, len(res))

