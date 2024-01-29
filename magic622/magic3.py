import numpy as np
import pandas as pd
from typing import List, Optional
from puzzle import Puzzle
from sympy.combinatorics import Permutation
from magic622.allowed_moves import get_allowed_moves_48


def cut_rot(n: int, magic: List[str]):
    st = 0
    for i, mv in enumerate(magic):
        if mv[0] == "-":
            nm = int(mv[2:])
        else:
            nm = int(mv[1:])
        if nm in [0, n - 1]:
            st += 1
        else:
            break
    end = len(magic)
    for i, mv in enumerate(list(reversed(magic))):
        if mv[0] == "-":
            nm = int(mv[2:])
        else:
            nm = int(mv[1:])
        if nm in [0, n - 1]:
            end -= 1
        else:
            break
    return magic[st:end].copy()


def find_magic_number_3(n: int, magic: List[str]):
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


def find_magic_number_2(n: int, magic: List[str]):
    double_int = 0
    if magic[0] == magic[1]:
        double_int += 2
    if magic[-1] == magic[-2]:
        double_int += 1
    if double_int == 0:
        return magic[0], magic[1], None, False, double_int
    elif double_int == 1:
        return magic[0], magic[1], None, False, double_int
    elif double_int == 2:
        return magic[0], magic[2], None, False, double_int
    else:
        return magic[0], magic[2], None, False, double_int


def find_magic_number(n: int, magic: List[str]):
    magic_set = set()
    for mv in magic:
        if mv[0] == "-":
            magic_set.add(mv[1:])
        else:
            magic_set.add(mv)
    num = len(magic_set)
    if num == 3:
        return find_magic_number_3(n, magic)
    else:
        return find_magic_number_2(n, magic)

def magic2(n: int, m1: str, m2: str, reverse: bool = False, double_int: int = 0):
    if m1[0] == "-":
        m11 = m1[1:]
    else:
        m11 = "-" + m1
    if m2[0] == "-":
        m21 = m2[1:]
    else:
        m21 = "-" + m2

    if double_int == 1:
        if not reverse:
            res = [m1, m2, m2, m11, m21, m21]
        else:
            res = [m2, m2, m1, m21, m21, m11]
    elif double_int == 2:
        if not reverse:
            res = [m1, m1, m2, m11, m11, m21]
        else:
            res = [m2, m1, m1, m21, m11, m11]
    elif double_int == 3:
        if not reverse:
            res = [m1, m1, m2, m2, m11, m11, m21, m21]
        else:
            res = [m2, m2, m1, m1, m21, m21, m11, m11]
    else:
        if not reverse:
            res = [m1, m2, m11, m21]
        else:
            res = [m2, m1, m21, m11]
    return res


def magic3(n: int, m1: str, m2: str, m3: Optional[str], reverse: bool = False, double_int: int = 0):
    if m3 is None:
        return magic2(n, m1, m2, reverse, double_int)
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
    return res


class Magic3:

    def __init__(self, n: int, m1: str, m2: str, m3: Optional[str], reverse: bool = False, double_int: int = 0):
        self.n = n
        if m1[0] == "-":
            self.dim1 = m1[1]
            self.flag1 = -1
        else:
            self.dim1 = m1[0]
            self.flag1 = 1
        if m2[0] == "-":
            self.dim2 = m2[1]
            self.flag2 = -1
        else:
            self.dim2 = m2[0]
            self.flag2 = 1
        if m3 is not None:
            if m3[0] == "-":
                self.dim3 = m3[1]
                self.flag3 = -1
            else:
                self.dim3 = m3[0]
                self.flag3 = 1
        else:
            self.dim3 = "n"
            self.flag3 = 0

        res = magic3(n, m1, m2, m3, reverse=reverse, double_int=double_int)

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

allowed_moves_arr = get_allowed_moves_48("cube_6/6/6")


def check_magic(path, skip: bool=False):

    # if path == ['-r0', '-d3', 'r0', '-d1', '-r0', 'd3', 'r0', 'd1']:
    #     check_flag = True
    # else:
    #     check_flag = False

    repr_arr = np.arange(48)
    for m in path:
        repr_arr = repr_arr[allowed_moves_arr[m]]
    key = str(Permutation(repr_arr))
    if key[:4] == "(47)":
        key = key[4:]

    d = (repr_arr != np.arange(48)).sum()
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
    # check_x = np.array([1, 0, 0, 1, 1, 0, 0, 1] * 6)
    # check_y = check_x[repr_arr]
    # print(path)
    # print(repr_arr)
    # print(check_x, check_y)
    # assert np.abs(check_x - check_y).sum() == 0
    if skip:
        return key, repr_arr
    if d == dd > 0:
        return key, repr_arr
    else:
        return None, None


def get_magic_dict():

    path_dict = dict()
    arr_dict = dict()
    path_dict_rot = dict()
    arr_dict_rot = dict()

    for m1 in p6.allowed_moves:
        for m2 in p6.allowed_moves:
            if m1 == m2:
                continue
            for m3 in [None] + list(p6.allowed_moves.keys()):
                if m3 in [m1, m2]:
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
                        if m3 is not None:
                            if s & 1 > 0:
                                _m3 = "-" + m3
                            else:
                                _m3 = m3
                        else:
                            _m3 = None
                        # print(_m1, _m2, _m3)
                        _path = magic3(n, _m1, _m2, _m3, reverse=False, double_int=db)
                        mag = magic_from_command(n, _path)
                        # print(_path, mag.command_list)
                        assert mag.command_list == _path
                        _k, _arr = check_magic(_path)

                        if _k is not None:
                            if _k not in path_dict.keys():
                                path_dict[_k] = _path
                                arr_dict[_k] = _arr
                            elif len(_path) < len(path_dict[_k]):
                                path_dict[_k] = _path
                                arr_dict[_k] = _arr
                            if _k not in path_dict_rot.keys():
                                path_dict_rot[_k] = _path
                                arr_dict_rot[_k] = _arr
                            elif len(_path) < len(path_dict_rot[_k]):
                                path_dict_rot[_k] = _path
                                arr_dict_rot[_k] = _arr

                            # cut rotation
                            _path_cut = cut_rot(n, _path)
                            _k, _arr_cut = check_magic(_path_cut, skip=True)
                            if _k not in path_dict_rot.keys():
                                path_dict_rot[_k] = _path_cut
                                arr_dict_rot[_k] = _arr_cut
                            elif len(_path_cut) < len(path_dict_rot[_k]):
                                path_dict_rot[_k] = _path_cut
                                arr_dict_rot[_k] = _arr_cut

                        # reverse
                        _path = magic3(n, _m1, _m2, _m3, reverse=True, double_int=db)
                        _k, _arr = check_magic(_path)

                        if _k is not None:
                            if _k not in path_dict.keys():
                                path_dict[_k] = _path
                                arr_dict[_k] = _arr
                            elif len(_path) < len(path_dict[_k]):
                                path_dict[_k] = _path
                                arr_dict[_k] = _arr

                            if _k not in path_dict_rot.keys():
                                path_dict_rot[_k] = _path
                                arr_dict_rot[_k] = _arr
                            elif len(_path) < len(path_dict_rot[_k]):
                                path_dict_rot[_k] = _path
                                arr_dict_rot[_k] = _arr

                            # cut rotation
                            _path_cut = cut_rot(n, _path)
                            _k, _arr_cut = check_magic(_path_cut, skip=True)
                            if _k not in path_dict_rot.keys():
                                path_dict_rot[_k] = _path_cut
                                arr_dict_rot[_k] = _arr_cut
                            elif len(_path_cut) < len(path_dict_rot[_k]):
                                path_dict_rot[_k] = _path_cut
                                arr_dict_rot[_k] = _arr_cut

    # print(len(path_dict.keys()))  1345
    return arr_dict, path_dict, arr_dict_rot, path_dict_rot


if __name__ == "__main__":
    _arr_dict, _path_dict, _arr_dict_rot, _path_dict_rot = get_magic_dict()
    # for _k in _arr_dict.keys():
    #     print(_k)
    #     print(_path_dict[_k])
    print(len(_arr_dict.keys()), len(_arr_dict_rot.keys()))
