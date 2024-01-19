import numpy as np
import math
from itertools import combinations
from typing import Dict, List, Optional
from puzzle import Puzzle
from sympy.combinatorics import Permutation
from collections import deque
from rubik48.allowed_moves import get_allowed_moves_48


allowed_moves_arr = get_allowed_moves_48("cube_4/4/4")


def magic44():
    # https://cube.uubio.com/4x4x4/
    res_path = [
        "r1", "r1", "-f1", "-f2",
    ] + ["-r1", "d3", "d3"] * 4 + [
        "-r1", "f1", "f2", "-r1", "-r1"
    ]
    return res_path


def magic44r():
    # https://cube.uubio.com/4x4x4/
    res_path = [
        "r1", "r1", "-f1", "-f2", "r1"
    ] + ["d3", "d3", "r1"] * 4 + [
        "f1", "f2", "-r1", "-r1"
    ]
    return res_path


def magic442():
    # https://cube.uubio.com/4x4x4/
    res_path = [
        "r1", "r1", "-f1", "-f2",
    ] + ["-r1", "d3", "d3"] * 4 + [
        "-r1"
    ] + ["-r1", "d3", "d3"] * 4 + [
        "-r1", "f1", "f2", "-r1", "-r1"
    ]
    return res_path


def magic4a():
    # https://cube.uubio.com/4x4x4/
    res_path = [
        "f3", "f3", "-d0", "-r0", "-f3"
    ]
    return res_path


def magic43():
    # https://cube.uubio.com/4x4x4/
    res_path = [
        "r2", "d3", "d3", "r1", "d3", "d3",
        "-r1", "d3", "d3", "-r2", "d3", "d3",
        "r1", "d3", "d3", "-r1", "d3", "d3",
    ]
    return res_path


def magic43r():
    # https://cube.uubio.com/4x4x4/
    res_path = [
        "r1", "d3", "d3", "r2", "d3", "d3",
        "-r2", "d3", "d3", "-r1", "d3", "d3",
        "r2", "d3", "d3", "-r2", "d3", "d3",
    ]
    return res_path


def compress_magic():
    arr_dict = dict()
    command_dict = dict()
    for i, magic in enumerate([magic44(), magic44r(), magic442(), magic43(), magic43r()]):
        repr_arr = np.arange(48)
        for m in magic:
            repr_arr = repr_arr[allowed_moves_arr[m]]
        key = str(Permutation(repr_arr))
        if key[:4] == "(47)":
            key = key[4:]
        if key not in arr_dict:
            arr_dict[key] = repr_arr
            command_dict[key] = magic
        else:
            pass
            # print(key)  # no print is expected

        repr_arr = np.arange(48)
        for m in reversed(magic):
            repr_arr = repr_arr[allowed_moves_arr[m]]
        key = str(Permutation(repr_arr))
        if key[:4] == "(47)":
            key = key[4:]
        if key not in arr_dict:
            arr_dict[key] = repr_arr
            command_dict[key] = list(reversed(magic))
        else:
            pass
            # print(key)  # no print is expected

    # print(len(command_dict.keys()))  # 960

    return arr_dict, command_dict


if __name__ == "__main__":
    _n = 4
    _p4 = Puzzle(
        puzzle_id=_n * 10101, puzzle_type=f"cube_{_n}/{_n}/{_n}",
        solution_state=[str(_i) for _i in range(_n * _n * 6)], initial_state=[str(_i) for _i in range(_n * _n * 6)],
        num_wildcards=0
    )
    # _path = magic44() + magic44r()
    # _path = magic442()
    # _path = magic43()
    _path = magic43r()
    print(_path)

    _pe = Permutation(_n * _n * 6)
    for _m in _path:
        if _m[0] == "-":
            _pe = (_p4.allowed_moves[_m[1:]] ** (-1)) * _pe
        else:
            _pe = _p4.allowed_moves[_m] * _pe
    print(_pe)
    _arr_dict, _command_dict = compress_magic()
    print(_arr_dict)
    print(_command_dict)

