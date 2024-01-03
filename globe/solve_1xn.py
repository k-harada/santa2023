import pandas as pd
from ast import literal_eval
from typing import Dict, List
from sympy.combinatorics import Permutation
from heapq import heappop, heappush
from puzzle import Puzzle


def heuristic_0(x: List[str], done_list: List[List[str]]):
    res = 4
    n = len(x) // 4
    string_upper = "_".join(["."] + x[:2 * n] + x[:2 * n] + ["."])
    string_lower = "_".join(["."] + x[2 * n:] + x[2 * n:] + ["."])
    x0 = "_" + "_".join(done_list[0]) + "_"
    x0_rev = "_" + "_".join(reversed(done_list[0])) + "_"
    x1 = "_" + "_".join(done_list[1]) + "_"
    x1_rev = "_" + "_".join(reversed(done_list[1])) + "_"
    x2 = "_" + "_".join(done_list[2]) + "_"
    x2_rev = "_" + "_".join(reversed(done_list[2])) + "_"
    x3 = "_" + "_".join(done_list[3]) + "_"
    x3_rev = "_" + "_".join(reversed(done_list[3])) + "_"
    if string_upper.find(x0) >= 0 or string_lower.find(x0_rev) >= 0:
        res -= 1
    if string_upper.find(x1) >= 0 or string_lower.find(x1_rev) >= 0:
        res -= 1
    if string_upper.find(x2_rev) >= 0 or string_lower.find(x2) >= 0:
        res -= 1
    if string_upper.find(x3_rev) >= 0 or string_lower.find(x3) >= 0:
        res -= 1
    return res


def heuristic(x: List[str], y: List[str], done_list: List[List[str]], base_index: int = 0, add: str = ""):
    h0 = heuristic_0(x, done_list)
    n = len(x) // 4
    if add == "":
        return h0
    if h0 > 0:
        return h0 * 1000
    # find index for base
    base_list = done_list[base_index]
    string_upper = "_".join(["."] + x[:2 * n] + x[:2 * n] + ["."])
    string_lower = "_".join(["."] + x[2 * n:] + x[2 * n:] + ["."])

    x_joint = "_" + "_".join(base_list) + "_"
    if base_index in [0, 1]:
        s_up = string_upper.find(x_joint)
        if s_up >= 0:
            start_ind = string_upper[:s_up].count("_") - 1
            x_ = x.copy()
        else:
            x_ = list(reversed(x[2 * n:])) + list(reversed(x[:2 * n]))
            string_upper = "_".join(["."] + x_[:2 * n] + x_[:2 * n] + ["."])
            s_up = string_upper.find(x_joint)
            assert s_up >= 0
            start_ind = string_upper[:s_up].count("_") - 1
    else:
        s_low = string_lower.find(x_joint)
        if s_low >= 0:
            start_ind = string_lower[:s_low].count("_") - 1
            x_ = x[2 * n:] + x[:2 * n]
        else:
            x_ = list(reversed(x[:2 * n])) + list(reversed(x[2 * n:]))
            string_upper = "_".join(["."] + x_[:2 * n] + x_[:2 * n] + ["."])
            s_low = string_upper.find(x_joint)
            assert s_low >= 0
            start_ind = string_upper[:s_low].count("_") - 1
    x_joint_add = x_joint + add + "_"
    # print(x_joint_add, string_upper, string_lower)
    if string_upper.find(x_joint_add) >= 0 or string_lower.find(x_joint_add) >= 0:
        return 0

    res = 10000000
    last_ind = start_ind + len(base_list) - 1
    for i_add in range(4 * n):
        if x_[i_add] == add and (i_add < start_ind or last_ind < i_add):
            # print(start_ind, i_add)
            a = min((last_ind + 1) % n, -(last_ind + 1) % n)
            b = min(i_add % n, -i_add % n)
            res = min(res, a + b + 1)
    return res


def add_one(
        initial_state: List[str], goal_state: List[str],
        done_list: List[List[str]], base_index: int = 0, add: str = ""
):
    m = len(initial_state)
    assert len(initial_state) % 4 == 0
    assert len(initial_state) == len(goal_state)
    open_set = []

    heappush(open_set, (0, initial_state, []))
    closed_set = set()

    while len(open_set):

        _, current_state, path = heappop(open_set)
        h = heuristic(current_state, goal_state, done_list, base_index, add)
        if h == 0:
            # print(current_state, path)
            return current_state, path
        # print(h, current_state)

        if current_state == goal_state:
            return current_state, path

        closed_set.add(tuple(current_state))

        for action in action_list:
            new_state = current_state.copy()
            for move_name in action:
                move = allowed_moves[move_name]
                new_state = move(new_state)

            if tuple(new_state) not in closed_set:
                h_new = heuristic(new_state, goal_state, done_list, base_index, add)
                priority = len(path) + len(action) + h_new
                heappush(open_set, (priority, new_state, path + action))


def solve_last(initial_state: List[str], goal_state: List[str], done_list: List[List[str]]):

    open_set = []
    heappush(open_set, (0, initial_state, []))
    closed_set = set()

    while len(open_set):

        _, current_state, path = heappop(open_set)

        if current_state == goal_state:
            return current_state, path
        print(len(closed_set))
        closed_set.add(tuple(current_state))

        for action in action_list:
            new_state = current_state.copy()
            for move_name in action:
                move = allowed_moves[move_name]
                new_state = move(new_state)
            if tuple(new_state) not in closed_set:
                h0 = heuristic_0(new_state, done_list)
                if h0 == 0:
                    priority = len(path) + len(action)
                    heappush(open_set, (priority, new_state, path + action))


def solve_1xn(initial_state: List[str], goal_state: List[str]):
    n = len(initial_state) // 4
    done_list = [[goal_state[0]], [goal_state[n]], [goal_state[2 * n]], [goal_state[3 * n]]]
    state = initial_state.copy()
    sol = []
    for k in range(n - 2):
        for j in range(4):
            if k >= n - 3 and j == 3:
                break
            state, sol_add = add_one(
                state, goal_state, done_list, base_index=j, add=goal_state[n * j + k + 1]
            )
            sol = sol + sol_add
            done_list[j].append(goal_state[n * j + k + 1])
            # print(k, j)
    state, sol_add = solve_last(state, goal_state, done_list)
    sol = sol + sol_add
    return sol


if __name__ == "__main__":

    _id_list = []
    _moves_list = []
    action_list = [
        ["r0"], ["-r0"], ["r1"], ["-r1"],
        # ["f0"], ["f1"], ["f2"], ["f3"], ["f4"], ["f5"], ["f6"], ["f7"],
        ["f8"],
        # ["f9"], ["f10"], ["f11"], ["f12"], ["f13"], ["f14"], ["f15"],
        # ["f16"],
        # ["f17"], ["f18"], ["f19"], ["f20"], ["f21"], ["f22"], ["f23"], ["f24"],
        # ["f25"], ["f26"], ["f27"], ["f28"], ["f29"], ["f30"], ["f31"],
    ]
    puzzle_info_df = pd.read_csv('../input/puzzle_info.csv', index_col='puzzle_type')
    puzzles_df = pd.read_csv('../input/puzzles.csv')
    puzzles_df_1xn = puzzles_df[puzzles_df["puzzle_type"] == "globe_1/8"]

    allowed_moves_ = literal_eval(puzzle_info_df.loc['globe_1/8', 'allowed_moves'])
    allowed_moves: Dict[str, Permutation] = dict()
    for k_, v_ in allowed_moves_.items():
        v = Permutation(v_)
        allowed_moves[k_] = v
        allowed_moves["-" + k_] = v ** (-1)

    for _i, _row in puzzles_df_1xn.iterrows():

        _goal_state = list(_row["solution_state"].split(";"))
        _initial_state = list(_row["initial_state"].split(";"))

        _p = Puzzle(
            _row["id"], _row["puzzle_type"], list(_row["solution_state"].split(";")),
            list(_row["initial_state"].split(";")), _row["num_wildcards"]
        )
        print(_i)
        _sol = solve_1xn(_initial_state, _goal_state)

        for _m in _sol:
            _p.operate(_m)
        print(_p.state)
        print(_p.move_history)
        print(len(_p.move_history))
