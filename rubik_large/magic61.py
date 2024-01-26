import numpy as np
import pandas as pd
import math
from itertools import combinations
from typing import Dict, List, Optional
from puzzle import Puzzle
from sympy.combinatorics import Permutation
from collections import deque


def magic61(
        k_list: List[int], m: int, n: int, d1: str = "r", d2: str = "d", flag_int: int = 0,
        rev: bool = False, diag: bool = False, add: int = 0, rev_i: bool = False
):
    # https://cube.uubio.com/5x5x5/
    assert min([abs(k) for k in k_list]) > 0
    assert max([abs(k) for k in k_list]) < n - 1
    assert 0 <= m < n
    assert m not in k_list
    assert -m not in k_list
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

    if not rev_i:
        res_path = [f"{f0}{d1}{k}" if k > 0 else f"{f1}{d1}{-k}" for k in k_list] * c + [f"{f2}{d2}{v}"] + [f"{f0}{d1}{m}"] * c + [
            f"{f3}{d2}{v}"] + [f"{f1}{d1}{k}" if k > 0 else f"{f0}{d1}{-k}"for k in k_list] * c + [f"{f2}{d2}{v}"] + [f"{f1}{d1}{m}"] * c + [
            f"{f3}{d2}{v}"]
    else:
        res_path = [f"{f1}{d1}{k}" if k > 0 else f"{f0}{d1}{-k}" for k in k_list] * c + [f"{f2}{d2}{v}"] + [f"{f0}{d1}{m}"] * c + [
            f"{f3}{d2}{v}"] + [f"{f0}{d1}{k}" if k > 0 else f"{f1}{d1}{-k}" for k in k_list] * c + [f"{f2}{d2}{v}"] + [f"{f1}{d1}{m}"] * c + [
            f"{f3}{d2}{v}"]
    if add > 0:
        res_path = [f"{f2}{d2}{v}"] * add + res_path + [f"{f3}{d2}{v}"] * add
    return res_path


if __name__ == "__main__":

    _n = 6
    _p6 = Puzzle(
        puzzle_id=_n * 10101, puzzle_type=f"cube_{_n}/{_n}/{_n}",
        solution_state=[str(_i) for _i in range(_n * _n * 6)], initial_state=[str(_i) for _i in range(_n * _n * 6)],
        num_wildcards=0
    )
    # _path = magic612([2], 3, _n, "d", "r")  # (50 92 56)
    # _path = magic612([1], 3, _n, "d", "r")  # (49 98 62)
    _path = magic61([1, 2], 3, _n, "d", "r")  # (49 98 62)(50 92 56)
    # _path = magic612([4], 3, _n, "d", "r")  # (44 52 80)
    # _path = magic612([-4], 3, _n, "d", "r")  # (52 80 116)
    # _path = magic612([-1], 3, _n, "d", "r")  # (49 98 134)
    # _path = magic612([-2], 3, _n, "d", "r")  # (50 92 128)
    # _path = magic612([1, -2, 4], 3, _n, "d", "r")  # (50 92 128)

    print(_path)

    _pe = Permutation(_n * _n * 6)
    for _m in _path:
        if _m[0] == "-":
            _pe = (_p6.allowed_moves[_m[1:]] ** (-1)) * _pe
        else:
            _pe = _p6.allowed_moves[_m] * _pe
    print(_pe)
