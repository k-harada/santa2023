import pandas as pd
from puzzle import Puzzle
import datetime
from globe.solvers.solve_1xn_greed import GreedySolver


if __name__ == "__main__":
    puzzles_df = pd.read_csv('../../input/puzzles.csv')
    _y = 3
    _n = 4
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == f"globe_{_y}/{_n}"]
    dt_now = datetime.datetime.now()
    _id_list = []
    _moves_list = []

    solver = GreedySolver(_n)

    for _i, _row in puzzles_df_pick.iterrows():
        _goal_state_all = list(_row["solution_state"].split(";"))
        _initial_state_all = list(_row["initial_state"].split(";"))
        print(f"start _i = {_i}")
        print("initial_state:", _initial_state_all)
        print("goal_state:", _goal_state_all)
        _sol_all = []

        for _j in range((_y + 1) // 2):
            if _j > 0:
                _left = _j * (2 * _n)
                _right = (_j + 1) * (2 * _n)
                _initial_state = _initial_state_all[_left:_right] + _initial_state_all[-_right:-_left]
                _goal_state = _goal_state_all[_left:_right] + _goal_state_all[-_right:-_left]
            else:
                _initial_state = _initial_state_all[:2 * _n] + _initial_state_all[-2 * _n:]
                _goal_state = _goal_state_all[:2 * _n] + _goal_state_all[-2 * _n:]
            print("sub problem:", _j)
            print("initial_state:", _initial_state)
            print("goal_state:", _goal_state)

            solver.initialize(_initial_state, _goal_state, force_pair=False)
            solver.solve()
            print(solver.get_length())
            _sol = solver.get_path()

            for _m in _sol:
                if _m[0] == "f":
                    _sol_all.append(_m)
                elif _m == "r0":
                    _sol_all.append(f"r{_j}")
                elif _m == "-r0":
                    _sol_all.append(f"-r{_j}")
                elif _m == "r1":
                    _sol_all.append(f"r{_y - _j}")
                elif _m == "-r1":
                    _sol_all.append(f"-r{_y - _j}")

            for _q in [0, _n]:
                if _sol_all.count(f"f{_q}") % 2 == 1:
                    for _ in range(_n):
                        _sol_all.append(f"r{_j}")
                    _sol_all.append(f"f{_q}")
                    for _ in range(_n):
                        _sol_all.append(f"r{_j}")
                    _sol_all.append(f"f{_q}")
                    for _ in range(_n):
                        _sol_all.append(f"r{_j}")
                    _sol_all.append(f"f{_q}")

        # check
        _p = Puzzle(
            _row["id"], _row["puzzle_type"], list(_row["solution_state"].split(";")),
            list(_row["initial_state"].split(";")), _row["num_wildcards"]
        )
        for _m in _sol_all:
            _p.operate(_m)
        print(_p.state)
        print(_p.move_history)
        print(len(_p.move_history), "".join(_p.move_history).count("f"))
        print(f"_i = {_i} Done")
        _id_list.append(_i)
        _moves_list.append(".".join(_p.move_history))

    pd.DataFrame({"id": _id_list, "moves": _moves_list}).to_csv(
        f"../output/globe_3x4_{dt_now.strftime('%Y-%m-%d-%H:%M')}.csv", index=False
    )