import pandas as pd
from puzzle import Puzzle
import datetime
from solve_1xn_center import solve_1xn
from solve_trivial import solve_trivial


if __name__ == "__main__":
    puzzles_df = pd.read_csv('../../../input/puzzles.csv')
    _y = 6
    _n = 4
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == f"globe_{_y}/{_n}"]
    dt_now = datetime.datetime.now()
    _id_list = []
    _moves_list = []

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

            seed = 0
            _sol = solve_1xn(_initial_state, _goal_state, center_list=[0, _n], seed=seed)
            while _sol is None:
                seed += 1
                _sol = solve_1xn(_initial_state, _goal_state, center_list=[0, _n], seed=seed)

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
        if _y % 2 == 0:
            _yy = _y // 2
            _mm = _yy * _n * 2
            _sol_add = solve_trivial(_initial_state_all[_mm:-_mm], _goal_state_all[_mm:-_mm])
            for _m in _sol_add:
                if _m == "r0":
                    _sol_all.append(f"r{_yy}")
                elif _m == "-r0":
                    _sol_all.append(f"-r{_yy}")

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
        f"../output/globe_{_y}x{_n}_{dt_now.strftime('%Y-%m-%d-%H:%M')}.csv", index=False
    )