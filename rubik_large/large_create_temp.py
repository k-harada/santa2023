import numpy as np
import pandas as pd
import datetime
from rubik_large.large_cube import RubiksCubeLarge


c_list = ["A", "B", "C", "D", "E", "F"]
back = {
    "A": "F", "B": "A", "C": "B", "D": "C", "E": "D", "F": "E"
}


if __name__ == "__main__":

    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[(puzzles_df["id"] >= 267) & (puzzles_df["id"] < 283)]
    _q = None
    _id_list = []
    _moves_list = []
    _puzzle_type_list = []
    _solution_state_list = []
    _initial_state_list = []
    _num_wildcards_list = []

    for _i, _row in puzzles_df_pick.iterrows():
        if _row["id"] < 272:
            _n = 9
        elif _row["id"] < 277:
            _n = 10
            continue
        elif _row["id"] < 281:
            _n = 19
        else:
            _n = 33
        _m = (_n - 1) // 2
        _puzzle_type_list.append(_row["puzzle_type"])
        _num_wildcards_list.append(_row["num_wildcards"])
        if _row["id"] != 282:
            _q = RubiksCubeLarge(
                puzzle_id=_row["id"], size=_n,
                solution_state=list(_row["solution_state"].split(";")),
                initial_state=list(_row["initial_state"].split(";")),
                num_wildcards=_row["num_wildcards"]
            )
        else:
            _initial_state = []
            _solution_state = []
            for _ijk, (_x, _y) in enumerate(zip(
                    list(_row["initial_state"].split(";")),
                    list(_row["solution_state"].split(";"))
            )):
                _uv, _w = _ijk % (_n * _n), _ijk // (_n * _n)
                _u, _v = _uv // _n, _uv % _n
                if (_u + _v) % 2 == 0:
                    _initial_state.append(_x)
                    _solution_state.append(_y)
                else:
                    _initial_state.append(back[_x])
                    _solution_state.append(back[_y])
            _q = RubiksCubeLarge(
                puzzle_id=_row["id"], size=_n,
                solution_state=_solution_state,
                initial_state=_initial_state,
                num_wildcards=_row["num_wildcards"]
            )
        _q.align_center()
        _q.solve_bone()
        _id_list.append(_row["id"])
        _moves_list.append(".".join(_q.cube.move_history))
        print(_q.cube.puzzle_id, len(_q.cube.move_history))

        _solution_state_list.append(";".join(_q.cube.solution_state))
        _initial_state_list.append(";".join(_q.cube.state))

    pd.DataFrame(
        {"id": _id_list, "moves": _moves_list}
    ).to_csv(f"../output/large-267-282_bone.csv", index=False)

    pd.DataFrame({
        "id": _id_list, "puzzle_type": _puzzle_type_list, "solution_state": _solution_state_list,
        "initial_state": _initial_state_list, "num_wildcards": _num_wildcards_list
    }).to_csv(f"../output/large-267-282_step2_problems.csv", index=False)
