import numpy as np
from sympy.combinatorics import Permutation
from puzzle import Puzzle

from rubik72.allowed_moves import get_allowed_moves_72
from rubik48.magic42 import magic42, pick_inner_42

# 辺を整理する魔法

magic_list = []
for curl in [0, 1, -1, 2, -2]:
    for _add in [0]:  #, 3, 1, 2]:
        for d1 in ["d", "r", "f"]:
            for d2 in ["d", "r", "f"]:
                if d1 == d2:
                    continue
                for flag_int in range(4):
                    for b in [False, True]:
                        magic_list.append(magic42(1, 5, d1, d2, flag_int, False, b, add=_add, curl=curl))
                        magic_list.append(magic42(3, 5, d1, d2, flag_int, False, b, add=_add, curl=curl))
                        magic_list.append(magic42(1, 5, d1, d2, flag_int, True, b, add=_add, curl=curl))
                        magic_list.append(magic42(3, 5, d1, d2, flag_int, True, b, add=_add, curl=curl))

allowed_moves_arr = get_allowed_moves_72("cube_5/5/5")
# print(allowed_moves_arr)




def compress_magic():
    arr_dict = dict()
    command_dict = dict()
    for i, magic in enumerate(magic_list):
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

    # print(len(command_dict.keys()))  # 960

    return arr_dict, command_dict


arr_dict, command_dict = compress_magic()

if __name__ == "__main__":
    print(len(arr_dict.keys()))
    for _k in arr_dict.keys():
        _n = 5
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
        print(pick_inner_42(_pe, _n, 0))
        print(_k, arr_dict[_k])
    print(list(sorted(arr_dict.keys())))

