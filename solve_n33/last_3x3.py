import numpy as np
import pandas as pd
from typing import List
from puzzle import Puzzle
import kociemba
from rubik24.solve41 import solve_greed_41
from rubik24.solve51 import solve_greed_51
from rubik24.solve61 import solve_greed_61

from rubik3.align_center_deges import solve_bruce_12
from rubik72.solve72 import align_pair_edges_with_center
from solve_n33.solve33N import RubiksCubeLarge


def kociemba_to_kaggle(s, n):
    base_dict = {
        "R": f"r0",
        "R2": f"r0.r0",
        "R'": f"-r0",
        "L": f"-r{n - 1}",
        "L2": f"r{n - 1}.r{n - 1}",
        "L'": f"r{n - 1}",
        "F": f"f0",
        "F2": f"f0.f0",
        "F'": f"-f0",
        "B": f"-f{n - 1}",
        "B2": f"f{n - 1}.f{n - 1}",
        "B'": f"f{n - 1}",
        "D": f"d0",
        "D2": f"d0.d0",
        "D'": f"-d0",
        "U": f"-d{n - 1}",
        "U2": f"d{n - 1}.d{n - 1}",
        "U'": f"d{n - 1}",
    }
    return base_dict[s]

v_map = {"A": "U", "B": "F", "C": "R", "D": "B", "E": "L", "F": "D"}


if __name__ == "__main__":
    _n = 33
    assert _n % 2 == 1
    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == f"cube_{_n}/{_n}/{_n}"]
    _q = None
    for _i, _row in puzzles_df_pick.iterrows():
        if _row["solution_state"].split(";")[1] != "B":
            continue
        _q = RubiksCubeLarge(
            puzzle_id=_row["id"], size=_n,
            solution_state=list(_row["solution_state"].split(";")),
            initial_state=list(_row["initial_state"].split(";")),
            num_wildcards=_row["num_wildcards"]
        )
    df = pd.read_csv(f"../output/temp_step2_{_q.cube.puzzle_id}.csv")
    move_list_step2 = list(df["moves"].values[0].split("."))
    for _m in move_list_step2:
        _q.cube.operate(_m)
    # print(_q.cube.state)
    for _i in range(_n * _n * 6):
        if _q.cube.state[_i] != _q.cube.solution_state[_i]:
            assert ((_i % (_n * _n)) // _n in [0, _n - 1]) or ((_i % _n) in [0, _n - 1])
    kociemba_list = []
    _m = (_n - 1) // 2

    kociemba_list.append(_q.cube.state[0 * _n * _n + 0 * _n + 0])
    kociemba_list.append(_q.cube.state[0 * _n * _n + 0 * _n + _m])
    kociemba_list.append(_q.cube.state[0 * _n * _n + 0 * _n + _n - 1])
    kociemba_list.append(_q.cube.state[0 * _n * _n + _m * _n + 0])
    kociemba_list.append(_q.cube.state[0 * _n * _n + _m * _n + _m])
    kociemba_list.append(_q.cube.state[0 * _n * _n + _m * _n + _n - 1])
    kociemba_list.append(_q.cube.state[0 * _n * _n + (_n - 1) * _n + 0])
    kociemba_list.append(_q.cube.state[0 * _n * _n + (_n - 1) * _n + _m])
    kociemba_list.append(_q.cube.state[0 * _n * _n + (_n - 1) * _n + _n - 1])

    kociemba_list.append(_q.cube.state[2 * _n * _n + 0 * _n + 0])
    kociemba_list.append(_q.cube.state[2 * _n * _n + 0 * _n + _m])
    kociemba_list.append(_q.cube.state[2 * _n * _n + 0 * _n + _n - 1])
    kociemba_list.append(_q.cube.state[2 * _n * _n + _m * _n + 0])
    kociemba_list.append(_q.cube.state[2 * _n * _n + _m * _n + _m])
    kociemba_list.append(_q.cube.state[2 * _n * _n + _m * _n + _n - 1])
    kociemba_list.append(_q.cube.state[2 * _n * _n + (_n - 1) * _n + 0])
    kociemba_list.append(_q.cube.state[2 * _n * _n + (_n - 1) * _n + _m])
    kociemba_list.append(_q.cube.state[2 * _n * _n + (_n - 1) * _n + _n - 1])

    kociemba_list.append(_q.cube.state[1 * _n * _n + 0 * _n + 0])
    kociemba_list.append(_q.cube.state[1 * _n * _n + 0 * _n + _m])
    kociemba_list.append(_q.cube.state[1 * _n * _n + 0 * _n + _n - 1])
    kociemba_list.append(_q.cube.state[1 * _n * _n + _m * _n + 0])
    kociemba_list.append(_q.cube.state[1 * _n * _n + _m * _n + _m])
    kociemba_list.append(_q.cube.state[1 * _n * _n + _m * _n + _n - 1])
    kociemba_list.append(_q.cube.state[1 * _n * _n + (_n - 1) * _n + 0])
    kociemba_list.append(_q.cube.state[1 * _n * _n + (_n - 1) * _n + _m])
    kociemba_list.append(_q.cube.state[1 * _n * _n + (_n - 1) * _n + _n - 1])

    kociemba_list.append(_q.cube.state[5 * _n * _n + 0 * _n + 0])
    kociemba_list.append(_q.cube.state[5 * _n * _n + 0 * _n + _m])
    kociemba_list.append(_q.cube.state[5 * _n * _n + 0 * _n + _n - 1])
    kociemba_list.append(_q.cube.state[5 * _n * _n + _m * _n + 0])
    kociemba_list.append(_q.cube.state[5 * _n * _n + _m * _n + _m])
    kociemba_list.append(_q.cube.state[5 * _n * _n + _m * _n + _n - 1])
    kociemba_list.append(_q.cube.state[5 * _n * _n + (_n - 1) * _n + 0])
    kociemba_list.append(_q.cube.state[5 * _n * _n + (_n - 1) * _n + _m])
    kociemba_list.append(_q.cube.state[5 * _n * _n + (_n - 1) * _n + _n - 1])

    kociemba_list.append(_q.cube.state[4 * _n * _n + 0 * _n + 0])
    kociemba_list.append(_q.cube.state[4 * _n * _n + 0 * _n + _m])
    kociemba_list.append(_q.cube.state[4 * _n * _n + 0 * _n + _n - 1])
    kociemba_list.append(_q.cube.state[4 * _n * _n + _m * _n + 0])
    kociemba_list.append(_q.cube.state[4 * _n * _n + _m * _n + _m])
    kociemba_list.append(_q.cube.state[4 * _n * _n + _m * _n + _n - 1])
    kociemba_list.append(_q.cube.state[4 * _n * _n + (_n - 1) * _n + 0])
    kociemba_list.append(_q.cube.state[4 * _n * _n + (_n - 1) * _n + _m])
    kociemba_list.append(_q.cube.state[4 * _n * _n + (_n - 1) * _n + _n - 1])

    kociemba_list.append(_q.cube.state[3 * _n * _n + 0 * _n + 0])
    kociemba_list.append(_q.cube.state[3 * _n * _n + 0 * _n + _m])
    kociemba_list.append(_q.cube.state[3 * _n * _n + 0 * _n + _n - 1])
    kociemba_list.append(_q.cube.state[3 * _n * _n + _m * _n + 0])
    kociemba_list.append(_q.cube.state[3 * _n * _n + _m * _n + _m])
    kociemba_list.append(_q.cube.state[3 * _n * _n + _m * _n + _n - 1])
    kociemba_list.append(_q.cube.state[3 * _n * _n + (_n - 1) * _n + 0])
    kociemba_list.append(_q.cube.state[3 * _n * _n + (_n - 1) * _n + _m])
    kociemba_list.append(_q.cube.state[3 * _n * _n + (_n - 1) * _n + _n - 1])

    kociemba_str = "".join([v_map[_x] for _x in kociemba_list])
    res_3x3 = kociemba.solve(kociemba_str)
    for _s in res_3x3.split():
        _ms = kociemba_to_kaggle(_s, _n)
        for _m in _ms.split("."):
            _q.cube.operate(_m)
    assert _q.cube.state == _q.cube.solution_state

    pd.DataFrame(
        {"id": [_q.cube.puzzle_id], "moves": [".".join(_q.cube.move_history)]}
    ).to_csv(f"../output/temp_done_{_q.cube.puzzle_id}.csv", index=False)



