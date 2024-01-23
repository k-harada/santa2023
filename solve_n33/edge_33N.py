import numpy as np
import pandas as pd
from typing import List
from puzzle import Puzzle

from rubik24.solve41 import solve_greed_41
from rubik24.solve51 import solve_greed_51
from rubik24.solve61 import solve_greed_61

from rubik3.align_center_deges import solve_bruce_12
from rubik72.solve72 import align_pair_edges_with_center
from solve_n33.solve33N import RubiksCubeLarge


if __name__ == "__main__":
    _n = 33
    assert _n % 2 == 1
    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == f"cube_{_n}/{_n}/{_n}"]
    _q = None
    for _i, _row in puzzles_df_pick.iterrows():
        if _row["solution_state"].split(";")[1] != "N1":
            continue
        _q = RubiksCubeLarge(
            puzzle_id=_row["id"], size=_n,
            solution_state=list(_row["solution_state"].split(";")),
            initial_state=list(_row["initial_state"].split(";")),
            num_wildcards=_row["num_wildcards"]
        )
    df = pd.read_csv(f"../output/temp_{_q.cube.puzzle_id}.csv")
    move_list_center = list(df["moves"].values[0].split("."))
    for _m in move_list_center:
        _q.cube.operate(_m)
    print(_q.cube.state)
    _initial_state = ["O"] * 54
    _goal_state = ["O"] * 54
    for _j in range(6):
        _initial_state[9 * _j + 1] = _q.cube.state[_n * _n * _j + 16]
        _initial_state[9 * _j + 3] = _q.cube.state[_n * _n * _j + 33 * 16]
        _initial_state[9 * _j + 5] = _q.cube.state[_n * _n * _j + 33 * 16 + 32]
        _initial_state[9 * _j + 7] = _q.cube.state[_n * _n * _j + 33 * 32 + 16]
        _goal_state[9 * _j + 1] = _q.cube.solution_state[_n * _n * _j + 16]
        _goal_state[9 * _j + 3] = _q.cube.solution_state[_n * _n * _j + 33 * 16]
        _goal_state[9 * _j + 5] = _q.cube.solution_state[_n * _n * _j + 33 * 16 + 32]
        _goal_state[9 * _j + 7] = _q.cube.solution_state[_n * _n * _j + 33 * 32 + 16]
    if _q.cube.puzzle_id == 282:
        _move_edge = ['-r0', 'f0', '-r2', '-f2', '-d0', 'r2', 'f2', '-d2', '-d0', 'f0', '-d2', 'f2', '-d0', 'r0']
    elif _q.cube.puzzle_id == 283:
        _move_edge = ['-r0', 'f2', 'd0', 'd2', 'd2', 'f0', '-r0', 'd2', 'f0', 'd2', 'r0', '-d0']
    else:
        _move_edge = solve_bruce_12(_initial_state, _goal_state)
    for _m in _move_edge:
        if _m[-1] == "2":
            _q.cube.operate(_m[:-1] + "32")
        elif _m[-1] == "0":
            _q.cube.operate(_m)
        else:
            print(_m)
    print(_move_edge)
    print(_q.cube.state)
    named = False
    if _q.cube.puzzle_id == 283:
        named = True

    for j in range(15, 0, -1):
        _initial_state, _goal_state = _q.get_subset_edge(0, j, with_center=True)
        print(_initial_state)
        print(_goal_state)
        _path = align_pair_edges_with_center(_initial_state, _goal_state, named=named)
        for _m in _path:
            if _m[-1] == "4":
                _q.cube.operate(_m[:-1] + "32")
            elif _m[-1] == "3":
                _q.cube.operate(_m[:-1] + str(32 - j))
            elif _m[-1] == "2":
                _q.cube.operate(_m[:-1] + str(16))
                print(_m)
            elif _m[-1] == "1":
                _q.cube.operate(_m[:-1] + str(j))
            elif _m[-1] == "0":
                _q.cube.operate(_m)
            else:
                print(_m)
    print(len(_q.cube.move_history))
    print(_q.cube.state)
    pd.DataFrame(
        {"id": [_q.cube.puzzle_id], "moves": [".".join(_q.cube.move_history)]}
    ).to_csv(f"../output/temp_step2_{_q.cube.puzzle_id}.csv", index=False)

