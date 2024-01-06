import pandas as pd
from solve_1xn_center import solve_1xn
from puzzle import Puzzle


if __name__ == "__main__":
    # 1x8を実行（一応全部解ける）
    puzzles_df = pd.read_csv('../input/puzzles.csv')
    puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == "globe_1/8"]
    _id_list = []
    _moves_list = []
    for _i, _row in puzzles_df_pick.iterrows():
        _goal_state = list(_row["solution_state"].split(";"))
        _initial_state = list(_row["initial_state"].split(";"))

        _p = Puzzle(
            _row["id"], _row["puzzle_type"], list(_row["solution_state"].split(";")),
            list(_row["initial_state"].split(";")), _row["num_wildcards"]
        )
        print(_i)
        _sol = solve_1xn(_initial_state, _goal_state, True)

        for _m in _sol:
            _p.operate(_m)
        print(_p.state)
        print(_p.move_history)
        print(len(_p.move_history))
        _id_list.append(_i)
        _moves_list.append(".".join(_p.move_history))
    pd.DataFrame({"id": _id_list, "moves": _moves_list}).to_csv("../output/globe_1x8_harada0106.csv", index=False)
