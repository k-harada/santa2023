import pandas as pd
from ast import literal_eval
from typing import Dict, List
from sympy.combinatorics import Permutation
from heapq import heappop, heappush
from puzzle import Puzzle

from solve_1xn_center import solve_1xn


if __name__ == "__main__":
    # 1x8でテスト（一応全部解ける）
    puzzles_df = pd.read_csv('../input/puzzles.csv')
    puzzles_df_1xn = puzzles_df[puzzles_df["puzzle_type"] == "globe_3/4"]

    for _i, _row in puzzles_df_1xn.iterrows():
        _goal_state_all = list(_row["solution_state"].split(";"))
        _initial_state_all = list(_row["initial_state"].split(";"))

        print(_goal_state_all, _initial_state_all)

        for _y in [1, 0]:
            if _y == 0:
                _initial_state = _initial_state_all[:8] + _initial_state_all[-8:]
                _goal_state = _goal_state_all[:8] + _goal_state_all[-8:]
            else:
                _initial_state = _initial_state_all[8:16] + _initial_state_all[-16:-8]
                _goal_state = _goal_state_all[8:16] + _goal_state_all[-16:-8]
                print(_initial_state, _goal_state)
            _p = Puzzle(
                _row["id"], _row["puzzle_type"], list(_row["solution_state"].split(";")),
                list(_row["initial_state"].split(";")), _row["num_wildcards"]
            )
            print(_i)
            _sol = solve_1xn(_initial_state, _goal_state)

            for _m in _sol:
                _p.operate(_m)
            print(_p.state)
            print(_p.move_history)
            print(len(_p.move_history))