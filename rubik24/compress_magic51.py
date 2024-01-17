import numpy as np
from sympy.combinatorics import Permutation
from puzzle import Puzzle

from rubik24.allowed_moves import get_allowed_moves_24
from rubik24.magic51 import magic51, pick_inner_51


# 3点を入れ替える魔法大全

magic_list = []
for d1 in ["d", "r", "f"]:
    for d2 in ["d", "r", "f"]:
        if d1 == d2:
            continue
        for flag_int in range(4):
            magic_list.append(magic51(2, 3, 5, d1, d2, flag_int, False))
            magic_list.append(magic51(2, 3, 5, d1, d2, flag_int, True))
            magic_list.append(magic51(3, 2, 5, d1, d2, flag_int, False))
            magic_list.append(magic51(3, 2, 5, d1, d2, flag_int, True))
            magic_list.append(magic51(2, 1, 5, d1, d2, flag_int, False))
            magic_list.append(magic51(2, 1, 5, d1, d2, flag_int, True))
            magic_list.append(magic51(1, 2, 5, d1, d2, flag_int, False))
            magic_list.append(magic51(1, 2, 5, d1, d2, flag_int, True))
        for flag_int in [0, 2]:
            magic_list.append(magic51(2, 3, 5, d1, d2, flag_int, False, True))
            magic_list.append(magic51(2, 3, 5, d1, d2, flag_int, True, True))
            magic_list.append(magic51(3, 2, 5, d1, d2, flag_int, False, True))
            magic_list.append(magic51(3, 2, 5, d1, d2, flag_int, True, True))
            magic_list.append(magic51(2, 1, 5, d1, d2, flag_int, False, True))
            magic_list.append(magic51(2, 1, 5, d1, d2, flag_int, True, True))
            magic_list.append(magic51(1, 2, 5, d1, d2, flag_int, False, True))
            magic_list.append(magic51(1, 2, 5, d1, d2, flag_int, True, True))

magic_list_add = []
for d1 in ["d", "r", "f"]:
    for d2 in ["d", "r", "f"]:
        if d1 == d2:
            continue
        for flag_int in range(4):
            magic_list_add.append(magic51(2, 3, 5, d1, d2, flag_int, False, add=1))
            magic_list_add.append(magic51(2, 3, 5, d1, d2, flag_int, True, add=1))
            magic_list_add.append(magic51(3, 2, 5, d1, d2, flag_int, False, add=1))
            magic_list_add.append(magic51(3, 2, 5, d1, d2, flag_int, True, add=1))
            magic_list_add.append(magic51(2, 1, 5, d1, d2, flag_int, False, add=1))
            magic_list_add.append(magic51(2, 1, 5, d1, d2, flag_int, True, add=1))
            magic_list_add.append(magic51(1, 2, 5, d1, d2, flag_int, False, add=1))
            magic_list_add.append(magic51(1, 2, 5, d1, d2, flag_int, True, add=1))

allowed_moves_arr = get_allowed_moves_24("cube_5/5/5")


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
            print(key)  # no print is expected

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
            print(key)  # no print is expected

    for i, magic in enumerate(magic_list_add):
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
            print(key)  # no print is expected

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
            print(key)  # no print is expected
    # print(len(key_dict.keys()))  # 960
    return arr_dict, command_dict


arr_dict, command_dict = compress_magic()


if __name__ == "__main__":
    print(len(arr_dict.keys()))
    for _k in arr_dict.keys():
        _n = 5
        _p5 = Puzzle(
            puzzle_id=_n * 10101, puzzle_type=f"cube_{_n}/{_n}/{_n}",
            solution_state=[str(_i) for _i in range(_n * _n * 6)], initial_state=[str(_i) for _i in range(_n * _n * 6)],
            num_wildcards=0
        )
        _path = command_dict[_k]
        _pe = Permutation(_n * _n * 6)
        for _m in _path:
            if _m[0] == "-":
                _pe = (_p5.allowed_moves[_m[1:]] ** (-1)) * _pe
            else:
                _pe = _p5.allowed_moves[_m] * _pe
        print(pick_inner_51(_pe, _n, 3))
        print(_k, arr_dict[_k])

