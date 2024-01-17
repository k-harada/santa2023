import numpy as np
import pandas as pd
import math
from itertools import combinations
from typing import Dict, List, Optional
from puzzle import Puzzle
from sympy.combinatorics import Permutation
from collections import deque


def magic41(k: int, n: int = 100, d1: str = "", d2: str = ""):
    # https://cube.uubio.com/4x4x4/
    assert 0 <= k < n
    res_path = ["-d0"] + [f"r{k}"] + ["d0"] + [f"-r{k}"]
    return res_path


def print_cube(p):
    n = int(math.sqrt(len(p.state) // 6))
    i = 0
    for _ in range(6):
        print("_" * n)
        for _1 in range(n):
            print(p.state[i:i+n])
            i += n
    print("_" * (2 * n))


def pick_inner_41(pe: Permutation, n: int, k: int):
    check_41 = []
    for x in pe.__str__().split(")("):
        if x[0] == "(":
            x = x[1:]
        if x[-1] == ")":
            x = x[:-1]
        perm_int = list(map(int, x.split()))
        if len(x) == 1:
            continue
        print_flag = 1
        print_flag_2 = 0
        for pi in perm_int:
            qi = pi % (n * n)
            xi, yi = qi % n, qi // n
            if k < min(xi, yi) and max(xi, yi) < n - 1 - k:
                print_flag_2 = 1
            if xi not in [k, n - 1 - k] or yi not in [k, n - 1 - k]:
                print_flag = 0

        if print_flag == 1:
            check_41.append(("OK", perm_int))
        if print_flag_2 == 1:
            check_41.append(("Error", perm_int))
    return check_41


if __name__ == "__main__":
    _n = 33
    _p4 = Puzzle(
        puzzle_id=_n * 10101, puzzle_type=f"cube_{_n}/{_n}/{_n}",
        solution_state=[str(_i) for _i in range(_n * _n * 6)], initial_state=[str(_i) for _i in range(_n * _n * 6)],
        num_wildcards=0
    )
    _path = magic41(8)
    _pe = Permutation(_n * _n * 6)
    for _m in _path:
        if _m[0] == "-":
            _pe = (_p4.allowed_moves[_m[1:]] ** (-1)) * _pe
        else:
            _pe = _p4.allowed_moves[_m] * _pe
    print(pick_inner_41(_pe, 33, 8))

