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
            magic_list.append(magic51(1, 2, 6, d1, d2, flag_int, False))
            magic_list.append(magic51(1, 3, 6, d1, d2, flag_int, False))
            magic_list.append(magic51(1, 4, 6, d1, d2, flag_int, False))
            magic_list.append(magic51(2, 1, 6, d1, d2, flag_int, False))
            magic_list.append(magic51(2, 3, 6, d1, d2, flag_int, False))
            magic_list.append(magic51(2, 4, 6, d1, d2, flag_int, False))
            magic_list.append(magic51(3, 1, 6, d1, d2, flag_int, False))
            magic_list.append(magic51(3, 2, 6, d1, d2, flag_int, False))
            magic_list.append(magic51(3, 4, 6, d1, d2, flag_int, False))
            magic_list.append(magic51(4, 1, 6, d1, d2, flag_int, False))
            magic_list.append(magic51(4, 2, 6, d1, d2, flag_int, False))
            magic_list.append(magic51(4, 3, 6, d1, d2, flag_int, False))

            magic_list.append(magic51(1, 2, 6, d1, d2, flag_int, True))
            magic_list.append(magic51(1, 3, 6, d1, d2, flag_int, True))
            magic_list.append(magic51(1, 4, 6, d1, d2, flag_int, True))
            magic_list.append(magic51(2, 1, 6, d1, d2, flag_int, True))
            magic_list.append(magic51(2, 3, 6, d1, d2, flag_int, True))
            magic_list.append(magic51(2, 4, 6, d1, d2, flag_int, True))
            magic_list.append(magic51(3, 1, 6, d1, d2, flag_int, True))
            magic_list.append(magic51(3, 2, 6, d1, d2, flag_int, True))
            magic_list.append(magic51(3, 4, 6, d1, d2, flag_int, True))
            magic_list.append(magic51(4, 1, 6, d1, d2, flag_int, True))
            magic_list.append(magic51(4, 2, 6, d1, d2, flag_int, True))
            magic_list.append(magic51(4, 3, 6, d1, d2, flag_int, True))

        for flag_int in [0, 2]:
            magic_list.append(magic51(1, 2, 6, d1, d2, flag_int, False, True))
            magic_list.append(magic51(1, 3, 6, d1, d2, flag_int, True, True))
            magic_list.append(magic51(1, 4, 6, d1, d2, flag_int, False, True))
            magic_list.append(magic51(2, 1, 6, d1, d2, flag_int, True, True))
            magic_list.append(magic51(2, 3, 6, d1, d2, flag_int, False, True))
            magic_list.append(magic51(2, 4, 6, d1, d2, flag_int, True, True))
            magic_list.append(magic51(3, 1, 6, d1, d2, flag_int, False, True))
            magic_list.append(magic51(3, 2, 6, d1, d2, flag_int, True, True))
            magic_list.append(magic51(3, 4, 6, d1, d2, flag_int, False, True))
            magic_list.append(magic51(4, 1, 6, d1, d2, flag_int, True, True))
            magic_list.append(magic51(4, 2, 6, d1, d2, flag_int, False, True))
            magic_list.append(magic51(4, 3, 6, d1, d2, flag_int, True, True))

magic_list_add = []
for _add in range(1, 4):
    for d1 in ["d", "r", "f"]:
        for d2 in ["d", "r", "f"]:
            if d1 == d2:
                continue
            for flag_int in range(4):
                for b in [False, True]:
                    magic_list_add.append(magic51(1, 2, 6, d1, d2, flag_int, False, b, add=_add))
                    magic_list_add.append(magic51(1, 3, 6, d1, d2, flag_int, True, b, add=_add))
                    magic_list_add.append(magic51(1, 4, 6, d1, d2, flag_int, False, b, add=_add))
                    magic_list_add.append(magic51(2, 1, 6, d1, d2, flag_int, True, b, add=_add))
                    magic_list_add.append(magic51(2, 3, 6, d1, d2, flag_int, False, b, add=_add))
                    magic_list_add.append(magic51(2, 4, 6, d1, d2, flag_int, True, b, add=_add))
                    magic_list_add.append(magic51(3, 1, 6, d1, d2, flag_int, False, b, add=_add))
                    magic_list_add.append(magic51(3, 2, 6, d1, d2, flag_int, True, b, add=_add))
                    magic_list_add.append(magic51(3, 4, 6, d1, d2, flag_int, False, b, add=_add))
                    magic_list_add.append(magic51(4, 1, 6, d1, d2, flag_int, True, b, add=_add))
                    magic_list_add.append(magic51(4, 2, 6, d1, d2, flag_int, False, b, add=_add))
                    magic_list_add.append(magic51(4, 3, 6, d1, d2, flag_int, True, b, add=_add))

allowed_moves_arr = get_allowed_moves_24("cube_6/6/6")
# print(allowed_moves_arr)


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
            # print(key)
    # print(len(command_dict.keys()))  # 960
    del command_dict[""]
    del arr_dict[""]
    return arr_dict, command_dict


arr_dict, command_dict = compress_magic()

if __name__ == "__main__":
    print(len(arr_dict.keys()))
    for _k in arr_dict.keys():
        _n = 33
        _p33 = Puzzle(
            puzzle_id=_n * 10101, puzzle_type=f"cube_{_n}/{_n}/{_n}",
            solution_state=[str(_i) for _i in range(_n * _n * 6)], initial_state=[str(_i) for _i in range(_n * _n * 6)],
            num_wildcards=0
        )
        _path = command_dict[_k]
        _pe = Permutation(_n * _n * 33)
        for _m in _path:
            if _m[0] == "-":
                _pe = (_p33.allowed_moves[_m[1:]] ** (-1)) * _pe
            else:
                _pe = _p33.allowed_moves[_m] * _pe
        print(_pe)
        print(pick_inner_51(_pe, _n, 1))
        print(_k, len(command_dict[_k]), arr_dict[_k])
    print(list(sorted(arr_dict.keys())))

