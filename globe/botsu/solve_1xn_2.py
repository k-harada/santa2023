import pandas as pd
from typing import List, Dict
from sympy.combinatorics import Permutation
from heapq import heappop, heappush
from globe.botsu.heuristic import heuristic
from puzzle import Puzzle


def solve_1xn_2(initial_state: List[str], goal_state: List[str]):
    n = len(initial_state) // 4
    allowed_moves_mod: Dict[str, Permutation] = dict()
    allowed_moves_mod["r0"] = Permutation(list(range(1, 2 * n)) + [0] + list(range(2 * n, 4 * n)))
    allowed_moves_mod["-r0"] = allowed_moves_mod["r0"] ** (-1)
    allowed_moves_mod["r1"] = Permutation(list(range(2 * n)) + list(range(2 * n + 1, 4 * n)) + [2 * n])
    allowed_moves_mod["-r1"] = allowed_moves_mod["r1"] ** (-1)
    allowed_moves_mod["f0"] = Permutation(
        list(range(3 * n - 1, 2 * n - 1, -1)) + list(
            range(n, 2 * n)
        ) + list(range(n - 1, -1, -1)) + list(range(3 * n, 4 * n))
    )
    for i in range(1, 2 * n):
        allowed_moves_mod[f"f{i}"] = allowed_moves_mod["-r0"] * allowed_moves_mod["-r1"] * allowed_moves_mod[
            f"f{i - 1}"] * allowed_moves_mod["r0"] * allowed_moves_mod["r1"]

    assert len(initial_state) % 4 == 0
    assert len(initial_state) == len(goal_state)
    open_set = []

    heappush(open_set, (0, initial_state, []))
    closed_set = set()

    while len(open_set):
        _, current_state, path = heappop(open_set)
        h = 5 * heuristic(current_state, goal_state)
        if h == 0:
            # print(current_state, path)
            return current_state, path
        print(h, current_state)

        if current_state == goal_state:
            return current_state, path
        if tuple(current_state) in closed_set:
            continue
        closed_set.add(tuple(current_state))

        action_list = [[k] for k in allowed_moves_mod.keys() if k not in ["r1", "-r1"]]
        for action in action_list:
            new_state = current_state.copy()
            for move_name in action:
                move = allowed_moves_mod[move_name]
                new_state = move(new_state)

            if tuple(new_state) not in closed_set:
                h_new = heuristic(new_state, goal_state)
                priority = len(path) + len(action) + h_new
                heappush(open_set, (priority, new_state, path + action))


if __name__ == "__main__":
    # 1x8を実行（一応全部解ける）
    puzzles_df = pd.read_csv('../../input/puzzles.csv')
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
        _sol = solve_1xn_2(_initial_state, _goal_state)

        for _m in _sol:
            _p.operate(_m)
        print(_p.state)
        print(_p.move_history)
        print(len(_p.move_history))
        _id_list.append(_i)
        _moves_list.append(".".join(_p.move_history))
