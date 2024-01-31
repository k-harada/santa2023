import numpy as np
import pandas as pd
import datetime
from rubik_large.large_cube import RubiksCubeLarge


c_list = ["A", "B", "C", "D", "E", "F"]


def parse_magic(path):
    count_dict = dict()
    cnt_nonzero = 0
    parsed_path = [[]]
    for mv in path:
        if mv[0] != "-":
            mv_ = mv
            v = 1
        else:
            mv_ = mv[1:]
            v = -1

        if mv_ not in count_dict.keys():
            count_dict[mv_] = v
            cnt_nonzero += 1
        else:
            if count_dict[mv_] == 0:
                cnt_nonzero += 1
            count_dict[mv_] += v
            if count_dict[mv_] == 0:
                cnt_nonzero -= 1
        # print(mv, mv_, cnt_nonzero)
        parsed_path[-1].append(mv)
        if cnt_nonzero == 0:
            parsed_path.append([])
    return parsed_path[:-1]


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
        # pd.DataFrame(
        #     {"id": [283], "moves": [".".join(_q.cube.move_history)]}
        # ).to_csv(f"../output/large-283_bone.csv", index=False)

        # pd.DataFrame({
        #     "id": [283], "puzzle_type": ["cube_33/33/33"], "solution_state": [";".join(_q.cube.solution_state)],
        #     "initial_state": [";".join(_q.cube.state)], "num_wildcards": [_row["num_wildcards"]]
        # }).to_csv(f"../output/large-283_step2_problems.csv", index=False)

    assert _q.cube.state[:33] == _q.dummy_cube.state[:33]
    print(_q.face_rotations)
    _m = (_n - 1) // 2
    _path_list = [[] for _ in range(200)]
    for _i in range(1, _m):
        for _j in range(1, _m + 1):
            if _i != _j and _j != _m:
                continue
            _path = _q.run_subset(_i, _j, only_path=True)
            # print(_path)
            _parsed_path = parse_magic(_path)
            # print(_parsed_path)
            for _k, _path in enumerate(_parsed_path):
                _path_list[_k] = _path_list[_k] + _path

    for _path in _path_list:
        for _mv in _path:
            _q.cube.operate(_mv)
            if _mv in _q.face_rotations:
                _q.dummy_cube.operate(_mv)
    # print(_q.cube.state[:100])
    # print(_q.dummy_cube.state[:100])
    assert _q.cube.state[:33] == _q.dummy_cube.state[:33]

    _q.solve_inner_face_greed(allow_rot=False)
    print(len(_q.cube.move_history))

    _id_list = [283]
    _moves_list = [".".join(_q.cube.move_history)]
    dt_now = datetime.datetime.now()
    pd.DataFrame(
        {"id": _id_list, "moves": _moves_list}
    ).to_csv(f"../output/large-283_temp_seq_{len(_q.cube.move_history)}.csv", index=False)
    _q.print_face(0, 0)
    _q.print_face(1, 0)
    _q.print_face(2, 0)
    _q.print_face(3, 0)
    _q.print_face(4, 0)
    _q.print_face(5, 0)


    # rotate
    # solve dummy
    solution_state_dummy = []
    initial_state_dummy = []
    for _j, (_x, _y) in enumerate(zip(_q.cube.state, _q.cube.solution_state)):
        _xi = int(_x[1:])
        _yi = int(_y[1:])
        initial_state_dummy.append(c_list[_xi // (_n * _n)])
        solution_state_dummy.append(c_list[_yi // (_n * _n)])
    _p = RubiksCubeLarge(
        puzzle_id=999, size=_n,
        solution_state=solution_state_dummy,
        initial_state=initial_state_dummy,
        num_wildcards=0
    )
    _p.solve_3x3()
    for _mv in _p.cube.move_history:
        _q.cube.operate(_mv)

    _path_list = [[] for _ in range(200)]
    for _i in range(1, _m):
        for _j in range(_i + 1, _m):
            if _i == _j or _j == _m:
                continue
            _path = _q.run_subset_2(_i, _j, only_path=True)
            # print(_path)
            _parsed_path = parse_magic(_path)
            # print(_parsed_path)
            for _k, _path in enumerate(_parsed_path):
                _path_list[_k] = _path_list[_k] + _path
    for _path in _path_list:
        for _mv in _path:
            _q.cube.operate(_mv)

    _q.print_face(0, 0)
    _q.print_face(1, 0)
    _q.print_face(2, 0)
    _q.print_face(3, 0)
    _q.print_face(4, 0)
    _q.print_face(5, 0)
    print(len(_q.cube.move_history))
    print(_q.cube.puzzle_id, _p.count_solver_5, _q.count_41, _q.count_51, _q.count_61, _p.count_start)
    for _i, (_x, _y) in enumerate(zip(_q.cube.state, _q.cube.solution_state)):
        if _x != _y:
            print(_i, _x, _y)
    assert _q.cube.state == _q.cube.solution_state
    _id_list = [283]
    _moves_list = [".".join(_q.cube.move_history)]
    dt_now = datetime.datetime.now()
    pd.DataFrame(
        {"id": _id_list, "moves": _moves_list}
    ).to_csv(f"../output/large-283_seq_{len(_q.cube.move_history)}.csv", index=False)


