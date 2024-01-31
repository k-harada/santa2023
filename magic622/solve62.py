import numpy as np
import pandas as pd
from typing import List, Optional
from puzzle import Puzzle
from heapq import heappop, heappush
from collections import deque

from rubik24.solve61 import solve_greed_61 as solve_greed_61_old
from magic622.magic3 import get_magic_dict
from sympy.combinatorics import Permutation
from magic622.allowed_moves import get_allowed_moves_48


arr_dict, path_dict, arr_dict_rot, path_dict_rot = get_magic_dict()
allowed_moves_arr = get_allowed_moves_48("cube_6/6/6")
base_perm_dict = dict()
rot_face = ["f0", "r0", "d0", "f5", "r5", "d5", "-f0", "-r0", "-d0", "-f5", "-r5", "-d5"]
for _mv in rot_face:
    base_perm_dict[_mv] = allowed_moves_arr[_mv]



def transpose_path(path):
    res_path = []
    for mv in path:
        if mv[-1] == "1":
            mv_ = mv[:-1] + "2"
        elif mv[-1] == "2":
            mv_ = mv[:-1] + "1"
        elif mv[-1] == "4":
            mv_ = mv[:-1] + "3"
        elif mv[-1] == "3":
            mv_ = mv[:-1] + "4"
        else:
            mv_ = mv
        res_path.append(mv_)
    return res_path


def solve_greed_62(
        initial_state: List[str], goal_state: List[str], allow_rot: bool = False, one_move: bool = False,
        last_actions: Optional[List[str]] = None
):

    if allow_rot:
        return solve_greed_62_rot(initial_state, goal_state, one_move, last_actions)

    assert len(initial_state) == 48
    initial_state_arr = np.array(initial_state)
    goal_state_arr = np.array(goal_state)

    state_arr = initial_state_arr.copy()
    d_now = (state_arr != goal_state_arr).sum()

    if one_move:
        if last_actions is not None:
            res_path = last_actions
        else:
            res_path = []
    else:
        res_path = []

    if d_now == 0 and one_move:
        return 0, 0, []

    while d_now > 0:
        if len(res_path) >= 4:
            rev_seq = []
            for mv in [res_path[-1], res_path[-2], res_path[-3], res_path[-4]]:
                if mv[0] == "-":
                    rev_seq.append(mv[1:])
                else:
                    rev_seq.append("-" + mv)
        else:
            rev_seq = ["", "", "", ""]
        efi_best = 0.0
        d_new_best = d_now
        best_le_minus = 0
        best_path = []
        best_st = None
        for k in arr_dict_rot.keys():
            pe = arr_dict_rot[k]
            path_add = path_dict_rot[k]
            le_minus = 0
            for iii in range(4):
                if path_add[iii] == rev_seq[iii]:
                    le_minus += 1
                else:
                    break
            new_state_arr = state_arr[pe]
            new_goal_state_arr = goal_state_arr.copy()
            for mv in path_add:
                if mv in rot_face:
                    new_goal_state_arr = new_goal_state_arr[base_perm_dict[mv]]
            d_new = (new_state_arr != new_goal_state_arr).sum()
            efi = (d_now - d_new) / max(0.1, len(path_add) - 2 * le_minus)
            if efi > efi_best:
                efi_best = efi
                best_st = new_state_arr.copy()
                best_goal = new_goal_state_arr.copy()
                best_path = path_dict_rot[k]
                best_le_minus = le_minus
                d_new_best = d_new
        if one_move:
            return d_now - d_new_best, best_le_minus, best_path

        if best_st is None:
            # print(d_now, best_path)
            # print(state_arr)
            # print(goal_state_arr)
            state_1 = []
            state_2 = []
            goal_state_1 = []
            goal_state_2 = []
            for c in range(6):
                for j in [0, 3, 4, 7]:
                    i = c * 8 + j
                    state_1.append(state_arr[i])
                    goal_state_1.append(goal_state[i])
                for j in [2, 1, 6, 5]:
                    i = c * 8 + j
                    state_2.append(state_arr[i])
                    goal_state_2.append(goal_state[i])
            # print(state_arr)
            # print(goal_state)
            # print(state_1, goal_state_1)
            res_add_1 = solve_greed_61_old(state_1, goal_state_1)
            res_add_2 = solve_greed_61_old(state_2, goal_state_2)
            return res_path + res_add_1 + transpose_path(res_add_2)
        if best_le_minus > 0:
            res_path = res_path[:-best_le_minus] + best_path[best_le_minus:]
        else:
            res_path = res_path + best_path
        state_arr = best_st.copy()
        goal_state_arr = best_goal.copy()
        d_now = (state_arr != goal_state_arr).sum()

        # print(d_now)

    return res_path


def solve_greed_62_rot(
        initial_state: List[str], goal_state: List[str], one_move: bool = False,
        last_actions: Optional[List[str]] = None
):
    # 面の回転を許容する
    assert len(initial_state) == 48
    initial_state_arr = np.array(initial_state)
    goal_state_arr = np.array(goal_state)

    state_arr = initial_state_arr.copy()
    d_now = (state_arr != goal_state_arr).sum()


    if one_move:
        if last_actions is not None:
            res_path = last_actions
        else:
            res_path = []
    else:
        res_path = []

    if d_now == 0 and one_move:
        return 0, 0, []

    while d_now > 0:
        if len(res_path) >= 4:
            rev_seq = []
            for mv in [res_path[-1], res_path[-2], res_path[-3], res_path[-4]]:
                if mv[0] == "-":
                    rev_seq.append(mv[1:])
                else:
                    rev_seq.append("-" + mv)
        else:
            rev_seq = ["", "", "", ""]
        efi_best = 0.0
        d_new_best = d_now
        best_le_minus = 0
        best_path = []
        best_st = None
        for k in arr_dict_rot.keys():
            pe = arr_dict_rot[k]
            path_add = path_dict_rot[k]
            le_minus = 0
            for iii in range(4):
                if path_add[iii] == rev_seq[iii]:
                    le_minus += 1
                else:
                    break
            new_state_arr = state_arr[pe]
            d_new = (new_state_arr != goal_state_arr).sum()
            efi = (d_now - d_new) / max(0.1, len(path_add) - 2 * le_minus)
            if efi > efi_best:
                efi_best = efi
                best_st = new_state_arr.copy()
                best_path = path_dict_rot[k]
                best_le_minus = le_minus
                d_new_best = d_new

        if one_move:
            return d_now - d_new_best, best_le_minus, best_path

        if best_st is None:
            # print(d_now, best_path)
            # print(state_arr)
            # print(goal_state_arr)
            state_1 = []
            state_2 = []
            goal_state_1 = []
            goal_state_2 = []
            for c in range(6):
                for j in [0, 3, 4, 7]:
                    i = c * 8 + j
                    state_1.append(state_arr[i])
                    goal_state_1.append(goal_state[i])
                for j in [2, 1, 6, 5]:
                    i = c * 8 + j
                    state_2.append(state_arr[i])
                    goal_state_2.append(goal_state[i])
            # print(state_arr)
            # print(goal_state)
            # print(state_1, goal_state_1)
            res_add_1 = solve_greed_61_old(state_1, goal_state_1)
            res_add_2 = solve_greed_61_old(state_2, goal_state_2)
            return res_path + res_add_1 + transpose_path(res_add_2)
        if best_le_minus > 0:
            res_path = res_path[:-best_le_minus] + best_path[best_le_minus:]
        else:
            res_path = res_path + best_path
        state_arr = best_st.copy()
        d_now = (state_arr != goal_state_arr).sum()
        # print(d_now)

    return res_path


if __name__ == "__main__":

    _n = 6
    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == f"cube_{_n}/{_n}/{_n}"]

    for _i, _row in puzzles_df_pick.iterrows():
        _q6 = Puzzle(
            puzzle_id=_row["id"], puzzle_type=f"cube_{_n}/{_n}/{_n}",
            solution_state=list(_row["solution_state"].split(";")),
            initial_state=list(_row["initial_state"].split(";")),
            num_wildcards=0
        )
        _initial_state = list(_row["initial_state"].split(";"))
        _goal_state = list(_row["solution_state"].split(";"))

        _initial_state_pick = []
        _goal_state_pick = []
        for _j in range(6):
            _initial_state_pick.append(_q6.state[_n * _n * _j + 8])
            _initial_state_pick.append(_q6.state[_n * _n * _j + 9])
            _initial_state_pick.append(_q6.state[_n * _n * _j + 13])
            _initial_state_pick.append(_q6.state[_n * _n * _j + 16])
            _initial_state_pick.append(_q6.state[_n * _n * _j + 19])
            _initial_state_pick.append(_q6.state[_n * _n * _j + 22])
            _initial_state_pick.append(_q6.state[_n * _n * _j + 26])
            _initial_state_pick.append(_q6.state[_n * _n * _j + 27])

            _goal_state_pick.append(_goal_state[_n * _n * _j + 8])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 9])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 13])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 16])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 19])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 22])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 26])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 27])
        if _goal_state[1] == "A":
            _path = solve_greed_62(_initial_state_pick, _goal_state_pick, allow_rot=True)
        else:
            _path = solve_greed_62(_initial_state_pick, _goal_state_pick, allow_rot=False)
        for _m in _path:
            _q6.operate(_m)

        _state_pick = []
        for _j in range(6):
            _state_pick.append(_q6.state[_n * _n * _j + 8])
            _state_pick.append(_q6.state[_n * _n * _j + 9])
            _state_pick.append(_q6.state[_n * _n * _j + 13])
            _state_pick.append(_q6.state[_n * _n * _j + 16])
            _state_pick.append(_q6.state[_n * _n * _j + 19])
            _state_pick.append(_q6.state[_n * _n * _j + 22])
            _state_pick.append(_q6.state[_n * _n * _j + 26])
            _state_pick.append(_q6.state[_n * _n * _j + 27])
        if _goal_state[1] == "A":
            print(_row["id"], len(_path))
            assert _state_pick == _goal_state_pick
        else:
            print(_row["id"], len(_path))
            print(_state_pick)
            print(_goal_state_pick)


