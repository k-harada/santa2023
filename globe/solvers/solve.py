import pandas as pd
from puzzle import Puzzle

from solve_1xn_center import solve_1xn


if __name__ == "__main__":
    puzzles_df = pd.read_csv('../../input/puzzles.csv')
    _y = 3
    _n = 4
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == f"globe_{_y}/{_n}"]

    for _i, _row in puzzles_df_pick.iterrows():
        _goal_state_all = list(_row["solution_state"].split(";"))
        _initial_state_all = list(_row["initial_state"].split(";"))
        print(f"start _i = {_i}")
        print(_goal_state_all, _initial_state_all)
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
            print(_j, _initial_state, _goal_state)

            _sol = solve_1xn(_initial_state, _goal_state)
            for _m in _sol:
                if _m[0] == "f":
                    _q = int(_m[1:])
                    if _q == _n:
                        _sol_all.append(f"f{_n}")
                    elif _q < _n:
                        for _ in range(_n - _q):
                            _sol_all.append(f"-r{_j}")
                            _sol_all.append(f"-r{_y - _j}")
                        _sol_all.append(f"f{_n}")
                        for _ in range(_n - _q):
                            _sol_all.append(f"r{_j}")
                            _sol_all.append(f"r{_y - _j}")
                    else:
                        for _ in range(_q - _n):
                            _sol_all.append(f"r{_j}")
                            _sol_all.append(f"r{_y - _j}")
                        _sol_all.append(f"f{_n}")
                        for _ in range(_q - _n):
                            _sol_all.append(f"-r{_j}")
                            _sol_all.append(f"-r{_y - _j}")
                elif _m == "r0":
                    _sol_all.append(f"r{_j}")
                elif _m == "-r0":
                    _sol_all.append(f"-r{_j}")
                elif _m == "r1":
                    _sol_all.append(f"r{_y - _j}")
                elif _m == "-r1":
                    _sol_all.append(f"-r{_y - _j}")

            if _sol_all.count(f"f{_n}") % 2 == 1 and _j < (_y + 1) // 2 - 1:
                _sol_all.append(f"f{_n}")

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
