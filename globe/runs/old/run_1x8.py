import pandas as pd
from globe.solvers.old.solve_1xn_center import solve_1xn
from puzzle import Puzzle
import datetime


if __name__ == "__main__":
    # 1x8を実行（一応全部解ける）
    puzzles_df = pd.read_csv('../input/puzzles.csv')
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == "globe_1/8"]
    _id_list = []
    _moves_list = []
    dt_now = datetime.datetime.now()
    for _i, _row in puzzles_df_pick.iterrows():
        _goal_state = list(_row["solution_state"].split(";"))
        _initial_state = list(_row["initial_state"].split(";"))

        _p = Puzzle(
            _row["id"], _row["puzzle_type"], list(_row["solution_state"].split(";")),
            list(_row["initial_state"].split(";")), _row["num_wildcards"]
        )
        print(_i)
        seed = 71
        _sol = solve_1xn(_initial_state, _goal_state, seed=seed)
        while _sol is None:
            seed += 1
            _sol = solve_1xn(_initial_state, _goal_state, seed=seed)
            if seed == 75:
                break
        while _sol is None:
            seed += 1
            _sol = solve_1xn(_initial_state, _goal_state, center_list=[0, 4], seed=seed)
            if seed == 80:
                break

        for _m in _sol:
            _p.operate(_m)
        print(_p.state)
        print(_p.move_history)
        print(len(_p.move_history))
        _id_list.append(_i)
        _moves_list.append(".".join(_p.move_history))
    pd.DataFrame({"id": _id_list, "moves": _moves_list}).to_csv(
        f"../../output/globe_1x8__{dt_now.strftime('%Y-%m-%d-%H:%M')}.csv", index=False
    )
