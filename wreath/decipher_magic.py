import numpy as np
import pandas as pd
from itertools import combinations
from typing import Dict, List, Optional
from puzzle import Puzzle
from collections import deque

from wreath.allowed_moves import get_allowed_moves
from wreath.solve_greed import solve_greed

#         "A", "C", "A", "B", "A", "A", "A", "A", "A", "A", "A", "A",
#         "B", "B", "B", "B", "B", "B", "B", "B", "C", "B"
# ['l', '-r', '-l', '-r', 'l', '-r', '-r', '-l', '-r', 'l', 'r', 'r', 'r', 'r', '-l', 'r']


def triangle_up_1(p, q):
    # 3点を時計回りに循環させる魔法
    # 0 -> 100 - p -> 99 + q -> 0
    # 25 -> 25 - p -> 172 + q -> 25
    res_path = ["-l"] * p + ["r"] * q + ["l"] * p + ["-r"] * q
    return res_path


def triangle_up_2(p, q):
    # 3点を反時計回りに循環させる魔法
    # 0 -> 99 + q -> 100 - p -> 0
    # 25 -> 172 + q -> 25 - p -> 25
    res_path = ["r"] * q + ["-l"] * p + ["-r"] * q + ["l"] * p
    return res_path


def triangle_low_1(p, q):
    # 3点を時計回りに循環させる魔法
    # 0 -> p -> 198 - q -> 0
    # 25 -> 25 + p -> 173 - q -> 25
    res_path = ["l"] * p + ["-r"] * q + ["-l"] * p + ["r"] * q
    return res_path


def triangle_low_2(p, q):
    # 3点を反時計回りに循環させる魔法
    # 0 -> 198 - q -> p -> 0
    # 25 -> 173 - q -> 25 + p -> 25
    res_path = ["-r"] * q + ["l"] * p + ["r"] * q + ["-l"] * p
    return res_path


if __name__ == "__main__":
    _path = solve_greed([
        "A", "A", "A", "C", "A", "A", "A", "A", "A", "A", "A", "C",
        "B", "B", "B", "B", "B", "B", "B", "B", "B", "B"
    ], [
        "C", "A", "A", "C", "A", "A", "A", "A", "A", "A", "A", "A",
        "B", "B", "B", "B", "B", "B", "B", "B", "B", "B"
    ], "wreath_12/12")
    # print(_path)
    _path = triangle_low_1(3, 5)
    _p33 = Puzzle(
        puzzle_id=10033, puzzle_type="wreath_33/33",
        solution_state=[str(_i) for _i in range(64)], initial_state=[str(_i) for _i in range(64)],
        num_wildcards=0
    )
    for _m in _path:
        _p33.operate(_m)
    print(_p33)
    print(_p33.solution_state)
    print(_p33.state == _p33.solution_state)

    _p100 = Puzzle(
        puzzle_id=10100, puzzle_type="wreath_100/100",
        solution_state=[str(_i) for _i in range(198)], initial_state=[str(_i) for _i in range(198)],
        num_wildcards=0
    )
    for _m in _path:
        _p100.operate(_m)
    print(_p100)
    print(_p100.solution_state)
    print(_p100.state == _p100.solution_state)
