import pandas as pd
from globe.solvers.solve_1xn_center import solve_1xn
from puzzle import Puzzle
from globe.solvers.trivial_center import solve_trivial
import datetime


if __name__ == "__main__":
    # 2x6を実行
    puzzles_df = pd.read_csv('../../input/puzzles.csv')
    puzzles_df_1xn = puzzles_df[puzzles_df["puzzle_type"] == "globe_2/6"]
    _id_list = []
    _moves_list = []
    dt_now = datetime.datetime.now()
    # print(dt_now.strftime('%Y-%m-%d %H:%M'))
    for _i, _row in puzzles_df_1xn.iterrows():
        _goal_state = list(_row["solution_state"].split(";"))
        _initial_state = list(_row["initial_state"].split(";"))

        _p = Puzzle(
            _row["id"], _row["puzzle_type"], list(_row["solution_state"].split(";")),
            list(_row["initial_state"].split(";")), _row["num_wildcards"]
        )
        print(_i)
        _initial_state_sub = _initial_state[:12] + _initial_state[-12:]
        _goal_state_sub = _goal_state[:12] + _goal_state[-12:]
        print(_initial_state_sub)
        print(_goal_state_sub)
        seed = 0
        _sol = solve_1xn(_initial_state_sub, _goal_state_sub, seed=seed)
        while _sol is None:
            seed += 1
            _sol = solve_1xn(_initial_state_sub, _goal_state_sub, seed=seed)
        for _m in _sol:
            if _m == "r1":
                _p.operate("r2")
            elif _m == "-r1":
                _p.operate("-r2")
            else:
                _p.operate(_m)
        _sol_add = solve_trivial(_initial_state[12:-12], _goal_state[12:-12])
        for _m in _sol_add:
            if _m == "r0":
                _p.operate("r1")
            elif _m == "-r0":
                _p.operate("-r1")
        print(_p.state)
        print(_p.move_history)
        print(len(_p.move_history))
        _id_list.append(_i)
        _moves_list.append(".".join(_p.move_history))
    pd.DataFrame({"id": _id_list, "moves": _moves_list}).to_csv(
        f"../output/globe_2x6_{dt_now.strftime('%Y-%m-%d-%H:%M')}.csv", index=False
    )
