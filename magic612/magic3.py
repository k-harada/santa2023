import numpy as np
import pandas as pd
from typing import List
from puzzle import Puzzle
from sympy.combinatorics import Permutation
from rubik24.allowed_moves import get_allowed_moves_24
from rubik24.compress_magic61 import compress_magic as compress_magic_old


arr_dict_old, command_dict_old = compress_magic_old()


def find_magic_number(n: int, magic: List[str]):
    # rev of not
    if magic[0][0] == "-":
        v0 = int(magic[0][2:])
    else:
        v0 = int(magic[0][1:])
    if v0 in [0, n - 1]:
        double_int = 0
        if magic[1] == magic[2]:
            double_int += 1
        if magic[-1] == magic[-2]:
            double_int += 2
        if double_int == 0:
            return magic[0], magic[3], magic[1], False, double_int
        elif double_int == 1:
            return magic[0], magic[4], magic[1], False, double_int
        elif double_int == 2:
            return magic[0], magic[3], magic[1], False, double_int
        else:
            return magic[0], magic[4], magic[1], False, double_int
    else:
        double_int = 0
        if magic[-2] == magic[-3]:
            double_int += 1
        if magic[0] == magic[1]:
            double_int += 2
        if double_int == 0:
            return magic[1], magic[0], magic[2], True, double_int
        elif double_int == 1:
            return magic[1], magic[0], magic[2], True, double_int
        elif double_int == 2:
            return magic[2], magic[0], magic[3], True, double_int
        else:
            return magic[2], magic[0], magic[3], True, double_int


def magic3(n: int, m1: str, m2: str, m3: str, reverse: bool = False, double_int: int = 0):
    if m1[0] == "-":
        m11 = m1[1:]
    else:
        m11 = "-" + m1
    if m2[0] == "-":
        m21 = m2[1:]
    else:
        m21 = "-" + m2
    if m3[0] == "-":
        m31 = m3[1:]
    else:
        m31 = "-" + m3
    if double_int == 1:
        if not reverse:
            res = [m1, m3, m3, m11, m2, m1, m31, m31, m11, m21]
        else:
            res = [m2, m1, m3, m3, m11, m21, m1, m31, m31, m11]
    elif double_int == 2:
        if not reverse:
            res = [m1, m3, m11, m2, m2, m1, m31, m11, m21, m21]
        else:
            res = [m2, m2, m1, m3, m11, m21, m21, m1, m31, m11]
    elif double_int == 2:
        if not reverse:
            res = [m1, m3, m3, m11, m2, m2, m1, m31, m31, m11, m21, m21]
        else:
            res = [m2, m2, m1, m3, m3, m11, m21, m21, m1, m31, m31, m11]
    else:
        if not reverse:
            res = [m1, m3, m11, m2, m1, m31, m11, m21]
        else:
            res = [m2, m1, m3, m11, m21, m1, m31, m11]
    return res


class Magic3:

    def __init__(self, n: int, m1: str, m2: str, m3: str, reverse: bool = False, double_int: int = 0):
        self.n = n
        if m1[0] == "-":
            m11 = m1[1:]
            self.dim1 = m11[0]
            self.flag1 = -1
        else:
            m11 = "-" + m1
            self.dim1 = m1[0]
            self.flag1 = 1
        if m2[0] == "-":
            m21 = m2[1:]
            self.dim2 = m21[0]
            self.flag2 = -1
        else:
            m21 = "-" + m2
            self.dim2 = m2[0]
            self.flag2 = 1
        if m3[0] == "-":
            m31 = m3[1:]
            self.dim3 = m31[0]
            self.flag3 = -1
        else:
            m31 = "-" + m3
            self.dim3 = m3[0]
            self.flag3 = 1

        if double_int == 1:
            if not reverse:
                res = [m1, m3, m3, m11, m2, m1, m31, m31, m11, m21]
            else:
                res = [m2, m1, m3, m3, m11, m21, m1, m31, m31, m11]
        elif double_int == 2:
            if not reverse:
                res = [m1, m3, m11, m2, m2, m1, m31, m11, m21, m21]
            else:
                res = [m2, m2, m1, m3, m11, m21, m21, m1, m31, m11]
        elif double_int == 3:
            if not reverse:
                res = [m1, m3, m3, m11, m2, m2, m1, m31, m31, m11, m21, m21]
            else:
                res = [m2, m2, m1, m3, m3, m11, m21, m21, m1, m31, m31, m11]
        else:
            if not reverse:
                res = [m1, m3, m11, m2, m1, m31, m11, m21]
            else:
                res = [m2, m1, m3, m11, m21, m1, m31, m11]

        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.double_int = double_int
        self.rev = reverse
        self.command_list = res


def magic_from_command(n: int, magic: List[str]):
    m1, m2, m3, rev, double_int = find_magic_number(n, magic)
    return Magic3(n, m1, m2, m3, rev, double_int)


n = 6
p6 = Puzzle(
    puzzle_id=n * 10101, puzzle_type=f"cube_{n}/{n}/{n}",
    solution_state=[str(i) for i in range(n * n * 6)], initial_state=[str(i) for i in range(n * n * 6)],
    num_wildcards=0
)

allowed_moves_arr = get_allowed_moves_24("cube_6/6/6")


def check_magic(path):

    # if path == ['-r0', '-d3', 'r0', '-d1', '-r0', 'd3', 'r0', 'd1']:
    #     check_flag = True
    # else:
    #     check_flag = False

    repr_arr = np.arange(24)
    for m in path:
        repr_arr = repr_arr[allowed_moves_arr[m]]
    key = str(Permutation(repr_arr))
    if key[:4] == "(23)":
        key = key[4:]

    d = (repr_arr != np.arange(24)).sum()
    dd = 0
    for m in path:
        p6.operate(m)
    for x, y in zip(p6.state, p6.solution_state):
        if x != y:
            dd += 1
    # if d == 3 and dd != 3:
    #     print(d, dd)
    p6.reset()
    # if check_flag:
    #     print(d, dd, key, repr_arr)
    if d == dd:
        return key, repr_arr
    else:
        return None, None


def get_magic_dict():

    path_dict = dict()
    arr_dict = dict()

    for m1 in ["f0", "f5", "d0", "d5", "r0", "r5"]:
        for m2 in p6.allowed_moves:
            if m2 in ["f0", "f5", "d0", "d5", "r0", "r5"]:
                continue
            for m3 in p6.allowed_moves:
                if m3 in ["f0", "f5", "d0", "d5", "r0", "r5"]:
                    continue

                for db in range(4):

                    for s in range(8):
                        if s & 4 > 0:
                            _m1 = "-" + m1
                        else:
                            _m1 = m1
                        if s & 2 > 0:
                            _m2 = "-" + m2
                        else:
                            _m2 = m2
                        if s & 1 > 0:
                            _m3 = "-" + m3
                        else:
                            _m3 = m3
                        # print(_m1, _m2, _m3)
                        _path = magic3(n, _m1, _m2, _m3, reverse=False, double_int=db)
                        mag = magic_from_command(n, _path)
                        assert mag.command_list == _path
                        _k, _arr = check_magic(_path)

                        if _k is not None:
                            if _k not in path_dict.keys():
                                path_dict[_k] = _path
                                arr_dict[_k] = _arr
                        # reverse
                        _path = magic3(n, _m1, _m2, _m3, reverse=True, double_int=db)
                        _k, _arr = check_magic(_path)

                        if _k is not None:
                            if _k not in path_dict.keys():
                                path_dict[_k] = _path
                                arr_dict[_k] = _arr
    # print(len(path_dict.keys()))  1345

    for _k in arr_dict_old.keys():
        _path = command_dict_old[_k]
        _arr = arr_dict_old[_k]
        _kk, _arr = check_magic(_path)
        if _kk is not None:
            if _kk not in path_dict.keys():
                # print(_kk, _path)
                path_dict[_k] = _path
                arr_dict[_k] = _arr

    return arr_dict, path_dict


if __name__ == "__main__":
    _arr_dict, _path_dict = get_magic_dict()
    print(len(_arr_dict.keys()))
