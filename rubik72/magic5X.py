import numpy as np
import math
from itertools import combinations
from typing import Dict, List, Optional
from puzzle import Puzzle
from sympy.combinatorics import Permutation
from collections import deque
from rubik72.allowed_moves import get_allowed_moves_72


allowed_moves_arr = get_allowed_moves_72("cube_5/5/5")


def magic33():
    # https://cube.uubio.com/3x3x3/
    res_path = [
        "r2", "d4", "r2", "d4", "r2", "d4", "d4",
        "-r2", "d4", "-r2", "d4", "-r2", "d4", "d4",
    ]
    return res_path

def magic44():
    # https://cube.uubio.com/4x4x4/
    res_path = [
        "r1", "r1", "f0", "f4",
    ] + ["-d1", "-r0", "-r0"] * 4 + [
        "-d1", "-f0", "-f4", "-r1", "-r1"
    ]
    return res_path


def magic44r():
    # https://cube.uubio.com/4x4x4/
    res_path = [
        "r1", "r1", "f4", "f0", "d1",
    ] + ["r0", "r0", "d1"] * 4 + [
        "-f4", "-f0", "-r1", "-r1"
    ]
    return res_path


def magic442():
    # https://cube.uubio.com/4x4x4/
    res_path = [
        "r1", "r1", "f0", "f4",
    ] + ["-d1", "-r0", "-r0"] * 4 + [
        "-d1",
    ] + ["-d1", "-r0", "-r0"] * 4 + [
        "-d1", "-f0", "-f4", "-r1", "-r1"
    ]
    return res_path


def magic4a():
    # https://cube.uubio.com/4x4x4/
    res_path = [
        "f4", "f4", "-d0", "-r0", "-f4"
    ]
    return res_path


def magic43():
    # https://cube.uubio.com/4x4x4/
    res_path = [
        "r3", "d4", "d4", "r1", "d4", "d4",
        "-r1", "d4", "d4", "-r3", "d4", "d4",
        "r1", "d4", "d4", "-r1", "d4", "d4",
    ]
    return res_path


def magic43r():
    # https://cube.uubio.com/4x4x4/
    res_path = [
        "r1", "d4", "d4", "r3", "d4", "d4",
        "-r3", "d4", "d4", "-r1", "d4", "d4",
        "r3", "d4", "d4", "-r3", "d4", "d4",
    ]
    return res_path


def compress_magic():
    arr_dict = dict()
    command_dict = dict()
    for i, magic in enumerate([magic44(), magic44r(), magic442(), magic43(), magic43r()]):
        repr_arr = np.arange(72)
        for m in magic:
            repr_arr = repr_arr[allowed_moves_arr[m]]
        key = str(Permutation(repr_arr))
        if key[:4] == "(71)":
            key = key[4:]
        if key not in arr_dict:
            arr_dict[key] = repr_arr
            command_dict[key] = magic
        else:
            pass
            # print(key)  # no print is expected

        repr_arr = np.arange(72)
        for m in reversed(magic):
            repr_arr = repr_arr[allowed_moves_arr[m]]
        key = str(Permutation(repr_arr))
        if key[:4] == "(71)":
            key = key[4:]
        if key not in arr_dict:
            arr_dict[key] = repr_arr
            command_dict[key] = list(reversed(magic))
        else:
            pass
            # print(key)  # no print is expected

    # print(len(command_dict.keys()))
    # print(command_dict)

    return arr_dict, command_dict


if __name__ == "__main__":
    _n = 5
    _p5 = Puzzle(
        puzzle_id=_n * 10101, puzzle_type=f"cube_{_n}/{_n}/{_n}",
        solution_state=[str(_i) for _i in range(_n * _n * 6)], initial_state=[str(_i) for _i in range(_n * _n * 6)],
        num_wildcards=0
    )
    # _path = magic44() + magic44r()
    # _path = magic442()
    # _path = magic43()
    # _path = magic43r()
    # _path = magic44()
    _path = magic33()
    print(_path)

    _pe = Permutation(_n * _n * 6)
    for _m in _path:
        if _m[0] == "-":
            _pe = (_p5.allowed_moves[_m[1:]] ** (-1)) * _pe
        else:
            _pe = _p5.allowed_moves[_m] * _pe
    print(_pe)
    _arr_dict, _command_dict = compress_magic()
    print(_arr_dict)
    print(_command_dict)

    _n = 33
    _p33 = Puzzle(
        puzzle_id=_n * 10101, puzzle_type=f"cube_{_n}/{_n}/{_n}",
        solution_state=[str(_i) for _i in range(_n * _n * 6)], initial_state=[str(_i) for _i in range(_n * _n * 6)],
        num_wildcards=0
    )
    _path = []
    for _m in magic33():
        if _m[-1] == "4":
            _path.append(_m[:-1] + "32")
        elif _m[-1] == "3":
            _path.append(_m[:-1] + "18")
        elif _m[-1] == "2":
            _path.append(_m[:-1] + "16")
        elif _m[-1] == "1":
            _path.append(_m[:-1] + "14")
        elif _m[-1] == "0":
            _path.append(_m[:-1] + "0")
        else:
            print(_m)
    print(_path)
    _pe = Permutation(_n * _n * 6)
    for _m in _path:
        if _m[0] == "-":
            _pe = (_p33.allowed_moves[_m[1:]] ** (-1)) * _pe
        else:
            _pe = _p33.allowed_moves[_m] * _pe
    print(_pe)

