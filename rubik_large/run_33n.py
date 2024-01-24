import numpy as np
import pandas as pd
import datetime
from rubik_large.large_cube import RubiksCubeLarge


c_list = ["A", "B", "C", "D", "E", "F"]


if __name__ == "__main__":
    puzzles_df = pd.read_csv("../input/puzzles.csv")
    puzzles_df_pick = puzzles_df[(puzzles_df["id"] == 283)]
    _q = None
    for _i, _row in puzzles_df_pick.iterrows():
        _n = 33
        _m = (_n - 1) // 2
        _q = RubiksCubeLarge(
            puzzle_id=_row["id"], size=_n,
            solution_state=list(_row["solution_state"].split(";")),
            initial_state=list(_row["initial_state"].split(";")),
            num_wildcards=_row["num_wildcards"]
        )

        # solve dummy
        solution_state_dummy = []
        initial_state_dummy = []
        for _j, (_x, _y) in enumerate(zip(_q.cube.state, _q.cube.solution_state)):
            _xi = int(_x[1:])
            _yi = int(_y[1:])
            initial_state_dummy.append(c_list[_xi // (_n * _n)])
            solution_state_dummy.append(c_list[_yi // (_n * _n)])
        _p = RubiksCubeLarge(
            puzzle_id=_row["id"], size=_n,
            solution_state=solution_state_dummy,
            initial_state=initial_state_dummy,
            num_wildcards=_row["num_wildcards"]
        )
        _p.align_center()
        _p.solve_bone()

        print(len(_p.cube.move_history))
        for _m in _p.cube.move_history:
            _q.cube.operate(_m)

        # _q.print_face(0, 0)
        # _q.print_face(1, 0)
        # _q.print_face(2, 0)
        # _q.print_face(3, 0)
        # _q.print_face(4, 0)
        # _q.print_face(5, 0)

    _m = (_n - 1) // 2
    for _i in range(1, _m):
        for _j in range(1, _m + 1):
            _q.run_subset(_i, _j)

    _q.print_face(0, 0)
    _q.print_face(1, 0)
    _q.print_face(2, 0)
    _q.print_face(3, 0)
    _q.print_face(4, 0)
    _q.print_face(5, 0)
    print(len(_q.cube.move_history))
    print(_q.cube.puzzle_id, _q.count_solver_5, _q.count_41, _q.count_51, _q.count_61, _q.count_start)
    for _i, (_x, _y) in enumerate(zip(_q.cube.state, _q.cube.solution_state)):
        if _x != _y:
            print(_i, _x, _y)
    assert _q.cube.state == _q.cube.solution_state
    _id_list = [283]
    _moves_list = [".".join(_q.cube.move_history)]
    dt_now = datetime.datetime.now()
    pd.DataFrame(
        {"id": _id_list, "moves": _moves_list}
    ).to_csv(f"../output/large-283_{dt_now.strftime('%Y-%m-%d-%H:%M')}.csv", index=False)


