import numpy as np
import pandas as pd
import math
from itertools import combinations
from typing import Dict, List, Optional
from puzzle import Puzzle
from sympy.combinatorics import Permutation
from collections import deque


def magic51(
        k: int, m: int, n: int = 100, d1: str = "r", d2: str = "d", flag_int: int = 0,
        rev: bool = False, diag: bool = False, add: bool = False
):
    # https://cube.uubio.com/5x5x5/
    assert 0 <= k < n
    assert 0 <= m < n
    assert k != m
    assert d1 in ["r", "f", "d"]
    assert d2 in ["r", "f", "d"]
    assert d1 != d2

    if diag:
        c = 2
    else:
        c = 1

    if rev:
        v = n - 1
    else:
        v = 0
    if flag_int == 0:
        f0 = ""
        f1 = "-"
        f2 = ""
        f3 = "-"
    elif flag_int == 1:
        f0 = "-"
        f1 = ""
        f2 = ""
        f3 = "-"
    elif flag_int == 2:
        f0 = ""
        f1 = "-"
        f2 = "-"
        f3 = ""
    else:
        f0 = "-"
        f1 = ""
        f2 = "-"
        f3 = ""
    res_path = [f"{f0}{d1}{k}"] * c + [f"{f2}{d2}{v}"] + [f"{f0}{d1}{m}"] * c + [
        f"{f3}{d2}{v}"] + [f"{f1}{d1}{k}"] * c + [f"{f2}{d2}{v}"] + [f"{f1}{d1}{m}"] * c + [f"{f3}{d2}{v}"]
    if add:
        res_path = [f"{f2}{d2}{v}"] + res_path + [f"{f3}{d2}{v}"]
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


def pick_inner_51(pe: Permutation, n: int, k: int):
    check_51 = []
    if k > n - 1 - k:
        k = n - 1 - k
    for x in pe.__str__().split(")("):
        if x[0] == "(":
            x = x[1:]
        if x[-1] == ")":
            x = x[:-1]
        perm_int = list(map(int, x.split()))
        if len(perm_int) == 1:
            continue
        print_flag = 1
        print_flag_2 = 0
        for pi in perm_int:
            qi = pi % (n * n)
            xi, yi = qi % n, qi // n
            if k < min(xi, yi) and max(xi, yi) < n - 1 - k:
                print_flag_2 = 1
            if xi in [k, n - 1 - k] and yi in [k, n - 1 - k]:
                print_flag_2 = 1
            if k > min(xi, yi) and max(xi, yi) > n - 1 - k:
                print_flag_2 = 1

        if print_flag == 1:
            check_51.append(("OK", perm_int))
        if print_flag_2 == 1:
            check_51.append(("Error", perm_int))
    return check_51


if __name__ == "__main__":
    _n = 33
    _p33 = Puzzle(
        puzzle_id=_n * 10101, puzzle_type=f"cube_{_n}/{_n}/{_n}",
        solution_state=[str(_i) for _i in range(_n * _n * 6)], initial_state=[str(_i) for _i in range(_n * _n * 6)],
        num_wildcards=0
    )
    _path = magic51(8, 11, _n)
    print(_path)
    _pe = Permutation(_n * _n * 6)
    for _m in _path:
        if _m[0] == "-":
            _pe = (_p33.allowed_moves[_m[1:]] ** (-1)) * _pe
        else:
            _pe = _p33.allowed_moves[_m] * _pe
    print(pick_inner_51(_pe, _n, 8))

    _n = 5
    _p5 = Puzzle(
        puzzle_id=_n * 10101, puzzle_type=f"cube_{_n}/{_n}/{_n}",
        solution_state=[str(_i) for _i in range(_n * _n * 6)], initial_state=[str(_i) for _i in range(_n * _n * 6)],
        num_wildcards=0
    )
    # _path = magic51(2, 3, _n, "d", "r")  # [32, 61, 36]
    # _path = magic51(2, 3, _n, "d", "r", flag_int=2)  # [32, 63, 38]
    # _path = magic51(2, 1, _n, "d", "r")  # [38, 42, 63]
    # _path = magic51(2, 1, _n, "d", "r", flag_int=2)  # [36, 42, 61]
    # _path = magic51(1, 2, _n, "d", "r", flag_int=0)  # [36, 42, 61]
    # _path = magic51(2, 1, _n, "d", "r", flag_int=0, diag=True)
    _path = ['r2', 'r2', '-d0', 'r3', 'r3', 'd0', '-r2', '-r2', '-d0', '-r3', '-r3', 'd0']


    # _path = magic51(3, 2, _n, "d", "f", flag_int=3, rev=True)
    _pe = Permutation(_n * _n * 6)
    for _m in _path:
        if _m[0] == "-":
            _pe = (_p5.allowed_moves[_m[1:]] ** (-1)) * _pe
        else:
            _pe = _p5.allowed_moves[_m] * _pe
    print(pick_inner_51(_pe, _n, 3))

    _n = 8
    _p8 = Puzzle(
        puzzle_id=_n * 10101, puzzle_type=f"cube_{_n}/{_n}/{_n}",
        solution_state=[str(_i) for _i in range(_n * _n * 6)], initial_state=[str(_i) for _i in range(_n * _n * 6)],
        num_wildcards=0
    )
    _path = magic51(2, 4, _n)
    _pe = Permutation(_n * _n * 6)
    for _m in _path:
        if _m[0] == "-":
            _pe = (_p8.allowed_moves[_m[1:]] ** (-1)) * _pe
        else:
            _pe = _p8.allowed_moves[_m] * _pe
    print(pick_inner_51(_pe, _n, 2))
