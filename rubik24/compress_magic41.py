import numpy as np
from sympy.combinatorics import Permutation
from puzzle import Puzzle

from rubik24.allowed_moves import get_allowed_moves_24
from rubik24.magic41 import magic41, pick_inner_41

# 5点を巡回させる魔法大全

magic_list = []
for curl in [0, 1, -1, 2, -2]:
    for _add in [0, 3, 1, 2]:
        for d1 in ["d", "r", "f"]:
            for d2 in ["d", "r", "f"]:
                if d1 == d2:
                    continue
                for flag_int in range(4):
                    for b in [False, True]:
                        magic_list.append(magic41(1, 4, d1, d2, flag_int, False, b, add=_add, curl=curl))
                        magic_list.append(magic41(2, 4, d1, d2, flag_int, False, b, add=_add, curl=curl))
                        magic_list.append(magic41(1, 4, d1, d2, flag_int, True, b, add=_add, curl=curl))
                        magic_list.append(magic41(2, 4, d1, d2, flag_int, True, b, add=_add, curl=curl))

#         k: int, n: int = 100, d1: str = "r", d2: str = "d", flag_int: int = 0,
#         rev: bool = False, diag: bool = False, add: int = 0
allowed_moves_arr = get_allowed_moves_24("cube_4/4/4")
# print(allowed_moves_arr)

for m in ["d1", "d2", "-d1", "-d2", "r1", "r2", "-r1", "-r2", "f1", "f2", "-f1", "-f2"]:
    magic_list.append([m])
for m in ["d0", "d3", "-d0", "-d3", "r0", "r3", "-r0", "-r3", "f0", "f3", "-f0", "-f3"]:
    magic_list.append([m])


def compress_magic():
    arr_dict = dict()
    command_dict = dict()
    for i, magic in enumerate(magic_list):
        repr_arr = np.arange(24)
        for m in magic:
            repr_arr = repr_arr[allowed_moves_arr[m]]
        key = str(Permutation(repr_arr))
        if key[:4] == "(23)":
            key = key[4:]
        if key not in arr_dict:
            arr_dict[key] = repr_arr
            command_dict[key] = magic
        else:
            pass
            # print(key)  # no print is expected

        repr_arr = np.arange(24)
        for m in reversed(magic):
            repr_arr = repr_arr[allowed_moves_arr[m]]
        key = str(Permutation(repr_arr))
        if key[:4] == "(23)":
            key = key[4:]
        if key not in arr_dict:
            arr_dict[key] = repr_arr
            command_dict[key] = list(reversed(magic))
        else:
            pass
            # print(key)  # no print is expected

    # print(len(command_dict.keys()))  # 960

    return arr_dict, command_dict


arr_dict, command_dict = compress_magic()

if __name__ == "__main__":
    print(len(arr_dict.keys()))
    for _k in arr_dict.keys():
        _n = 4
        _p4 = Puzzle(
            puzzle_id=_n * 10101, puzzle_type=f"cube_{_n}/{_n}/{_n}",
            solution_state=[str(_i) for _i in range(_n * _n * 6)], initial_state=[str(_i) for _i in range(_n * _n * 6)],
            num_wildcards=0
        )
        _path = command_dict[_k]
        _pe = Permutation(_n * _n * 6)
        for _m in _path:
            if _m[0] == "-":
                _pe = (_p4.allowed_moves[_m[1:]] ** (-1)) * _pe
            else:
                _pe = _p4.allowed_moves[_m] * _pe
        print(pick_inner_41(_pe, _n, 1))
        print(_k, arr_dict[_k])
    print(list(sorted(arr_dict.keys())))

    print(len(arr_dict.keys()))
    for _k in arr_dict.keys():
        _n = 6
        _p6 = Puzzle(
            puzzle_id=_n * 10101, puzzle_type=f"cube_{_n}/{_n}/{_n}",
            solution_state=[str(_i) for _i in range(_n * _n * 6)], initial_state=[str(_i) for _i in range(_n * _n * 6)],
            num_wildcards=0
        )
        _path = command_dict[_k]
        _pe = Permutation(_n * _n * 6)
        for _m in _path:
            if _m[-1] == "3":
                _mm = _m[:-1] + "5"
            elif _m[-1] == "2":
                _mm = _m[:-1] + "4"
            else:
                _mm = _m
            if _mm[0] == "-":
                _pe = (_p6.allowed_moves[_m[1:]] ** (-1)) * _pe
            else:
                _pe = _p6.allowed_moves[_m] * _pe
        print(pick_inner_41(_pe, _n, 1))
        print(_k, arr_dict[_k])
    print(list(sorted(arr_dict.keys())))
