import numpy as np
import pandas as pd
from typing import List
from puzzle import Puzzle
from heapq import heappop, heappush
from collections import deque

from magic612.magic3 import get_magic_dict
from rubik24.solve61 import solve_greed_61 as solve_greed_61_old


arr_dict, path_dict = get_magic_dict()


def solve_greed_61(initial_state: List[str], goal_state: List[str]):

    assert len(initial_state) == 24
    initial_state_arr = np.array(initial_state)
    goal_state_arr = np.array(goal_state)

    state_arr = initial_state_arr.copy()
    d_now = (state_arr != goal_state_arr).sum()

    res_path = []
    while d_now > 0:
        best = d_now
        best_path = []
        best_st = None
        for k in arr_dict.keys():
            pe = arr_dict[k]
            new_state_arr = state_arr[pe]
            d_new = (new_state_arr != goal_state_arr).sum()
            if d_new < best:
                best = d_new
                best_st = new_state_arr.copy()
                best_path = path_dict[k]
        if best_st is None:
            # print(d_now, best_path)
            # print(state_arr)
            # print(goal_state_arr)
            return res_path + solve_greed_61_old(list(state_arr), goal_state)
        res_path = res_path + best_path
        state_arr = best_st.copy()
        d_now = best
        # print(d_now)

    return res_path


if __name__ == "__main__":
    np.random.seed(3)
    _initial_state = ["U", "U", "U", "U"] + ["F"] * 4 + ["R"] * 4 + ["B"] * 4 + ["L"] * 4 + ["D", "D", "D", "D"]
    np.random.shuffle(_initial_state)
    _initial_state = list(_initial_state)
    _goal_state = ["U", "U", "U", "U"] + ["F"] * 4 + ["R"] * 4 + ["B"] * 4 + ["L"] * 4 + ["D", "D", "D", "D"]
    solve_greed_61(_initial_state, _goal_state)

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
            _initial_state_pick.append(_q6.state[_n * _n * _j + 16])
            _initial_state_pick.append(_q6.state[_n * _n * _j + 19])
            _initial_state_pick.append(_q6.state[_n * _n * _j + 27])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 8])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 16])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 19])
            _goal_state_pick.append(_goal_state[_n * _n * _j + 27])

        _path = solve_greed_61(_initial_state_pick, _goal_state_pick)
        for _m in _path:
            _q6.operate(_m)
        print(len(_path))
        print(_q6.state)
