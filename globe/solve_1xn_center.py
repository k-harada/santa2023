import pandas as pd
from ast import literal_eval
from typing import Dict, List
from sympy.combinatorics import Permutation
from heapq import heappop, heappush
from puzzle import Puzzle

from solve_last import solve_greed


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
    count_upper = 0
    count_lower = 0
    if string_upper.find(x0) >= 0:
        res -= 1
        count_upper += 1
    elif string_lower.find(x0_rev) >= 0:
        res -= 1
        count_lower += 1

    if string_upper.find(x1) >= 0:
        res -= 1
        count_upper += 1
    elif string_lower.find(x1_rev) >= 0:
        res -= 1
        count_lower += 1

    if string_lower.find(x2) >= 0:
        res -= 1
        count_lower += 1
    elif string_upper.find(x2_rev) >= 0:
        res -= 1
        count_upper += 1

    if string_lower.find(x3) >= 0:
        res -= 1
        count_lower += 1
    elif string_upper.find(x3_rev) >= 0:
        res -= 1
        count_upper += 1
    if max(count_lower, count_upper) >= 3 and len(done_list[3]) >= max(n // 3, 2):
        res += 10
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
    x_joint_add = x_joint + add + "_"

    if base_index in [0, 1]:
        if string_upper.find(x_joint_add) >= 0 or string_lower.find("".join(list(reversed(x_joint_add)))) >= 0:
            return 0
    else:
        if string_lower.find(x_joint_add) >= 0 or string_upper.find("".join(list(reversed(x_joint_add)))) >= 0:
            return 0

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
        initial_state: List[str], goal_state: List[str], allowed_moves,
        done_list: List[List[str]], base_index: int = 0, add: str = "",
        center: int = -1
):
    n = len(initial_state) // 4
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

        """
        action_list = []
        new_state = current_state.copy()
        new_state = allowed_moves[f"f{n}"](new_state)
        if heuristic_0(new_state, done_list) == 0:
            action_list.append([f"f{n}"])

        for i in range(1, n + 1):
            new_state = current_state.copy()
            new_state = (allowed_moves["r0"] ** i)(new_state)
            if heuristic_0(allowed_moves[f"f{n}"](new_state), done_list) == 0:
                action_list.append(["r0"] * i)
                break
        for i in range(1, n + 1):
            new_state = current_state.copy()
            new_state = (allowed_moves["r1"] ** i)(new_state)
            if heuristic_0(allowed_moves[f"f{n}"](new_state), done_list) == 0:
                action_list.append(["r1"] * i)
                break
        for i in range(1, n + 1):
            new_state = current_state.copy()
            new_state = (allowed_moves["-r0"] ** i)(new_state)
            if heuristic_0(allowed_moves[f"f{n}"](new_state), done_list) == 0:
                action_list.append(["-r0"] * i)
                break
        for i in range(1, n + 1):
            new_state = current_state.copy()
            new_state = (allowed_moves["-r1"] ** i)(new_state)
            if heuristic_0(allowed_moves[f"f{n}"](new_state), done_list) == 0:
                action_list.append(["-r1"] * i)
                break
        # print(action_list)
        # print(current_state, done_list, path)
        # print(len(open_set))
        # if len(action_list) == 0:
        #     action_list = [["r0"], ["-r0"], ["r1"], ["-r1"]]
        """
        if center != -1:
            action_list = [["r0"], ["-r0"], ["r1"], ["-r1"], [f"f{center}"]]
        else:
            action_list = [[k] for k in allowed_moves.keys()]
        for action in action_list:
            new_state = current_state.copy()
            for move_name in action:
                move = allowed_moves[move_name]
                new_state = move(new_state)

            if tuple(new_state) not in closed_set:
                h_new = heuristic(new_state, goal_state, done_list, base_index, add)
                priority = len(path) + len(action) + h_new
                heappush(open_set, (priority, new_state, path + action))


def solve_last(state: List[str], goal_state: List[str], done_list: List[List[str]]):
    x = state
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
    x4 = goal_state[n - 1]
    x5 = goal_state[2 * n - 1]
    x6 = goal_state[3 * n - 1]
    x7 = goal_state[4 * n - 2]
    print(x)
    print(done_list)
    print(x4, x5, x6, x7)

    res_up = [-1] * (2 * n)
    res_down = [-1] * (2 * n)
    s_up = string_upper.find(x0)
    if s_up >= 0:
        st = string_upper[:s_up].count("_")
        for i in range(st, st + len(done_list[0])):
            res_up[i % (2 * n)] = 0
    else:
        s_down = string_lower.find(x0_rev)
        st = string_lower[:s_down].count("_")
        for i in range(st, st + len(done_list[0])):
            res_down[i % (2 * n)] = 0

    s_up = string_upper.find(x1)
    if s_up >= 0:
        st = string_upper[:s_up].count("_")
        for i in range(st, st + len(done_list[1])):
            res_up[i % (2 * n)] = 1
    else:
        s_down = string_lower.find(x1_rev)
        st = string_lower[:s_down].count("_")
        for i in range(st, st + len(done_list[1])):
            res_down[i % (2 * n)] = 1

    s_up = string_upper.find(x2_rev)
    if s_up >= 0:
        st = string_upper[:s_up].count("_")
        for i in range(st, st + len(done_list[2])):
            res_up[i % (2 * n)] = 2
    else:
        s_down = string_lower.find(x2)
        st = string_lower[:s_down].count("_")
        for i in range(st, st + len(done_list[2])):
            res_down[i % (2 * n)] = 2

    s_up = string_upper.find(x3_rev)
    if s_up >= 0:
        st = string_upper[:s_up].count("_")
        for i in range(st, st + len(done_list[3])):
            res_up[i % (2 * n)] = 3
    else:
        s_down = string_lower.find(x3)
        st = string_lower[:s_down].count("_")
        for i in range(st, st + len(done_list[3])):
            res_down[i % (2 * n)] = 3

    for i in range(2 * n):
        if res_up[i] == -1:
            if state[i] == x4:
                res_up[i] = 4
            elif state[i] == x5:
                res_up[i] = 5
            elif state[i] == x6:
                res_up[i] = 6
            elif state[i] == x7:
                res_up[i] = 7
            else:
                res_up[i] = 8

        if res_down[i] == -1:
            if state[i + 2 * n] == x4:
                res_down[i] = 4
            elif state[i + 2 * n] == x5:
                res_down[i] = 5
            elif state[i + 2 * n] == x6:
                res_down[i] = 6
            elif state[i + 2 * n] == x7:
                res_down[i] = 7
            else:
                res_down[i] = 8
    print(res_up)
    print(res_down)
    length_list = [0] * (max(res_up + res_down) + 1)
    for c in res_up + res_down:
        length_list[c] += 1
    for i in range(4, len(length_list)):
        length_list[i] = 1
    if goal_state[4 * n - 2] == goal_state[4 * n - 1]:
        goal_state = [[0, 4, 1, 5], [2, 6, 3, 7, 7]]
        goal_state_sub = [[0, 4, 2, 6], [1, 5, 3, 7, 7]]
    else:
        goal_state = [[0, 4, 1, 5], [2, 6, 3, 7, 8]]
        goal_state_sub = [[0, 4, 2, 6], [1, 5, 3, 7, 8]]
    initial_state = [[], []]
    r_0 = 0
    if res_up[0] == res_up[-1] < 4:
        for i in range(2 * n):
            if res_up[i] != res_up[-1]:
                r_0 = i
                break
    s = -1
    for c in res_up[r_0:]:
        if c != s or c >= 4:
            s = c
            initial_state[0].append(c)

    r_1 = 0
    if res_down[0] == res_down[-1] < 4:
        for i in range(2 * n):
            if res_down[i] != res_down[-1]:
                r_1 = i
                break
    s = -1
    for c in res_down[r_1:]:
        if c != s or c >= 4:
            s = c
            initial_state[1].append(c)
    print(initial_state)
    print(goal_state)
    print(length_list)
    print(r_0, r_1)
    state, sol_add = solve_greed(initial_state, goal_state, length_list, r_0, r_1)
    return state, sol_add


def solve_1xn(initial_state: List[str], goal_state: List[str]):
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
        allowed_moves_mod[f"f{i}"] = allowed_moves_mod["-r0"] * allowed_moves_mod["-r1"] * allowed_moves_mod[f"f{i - 1}"] * allowed_moves_mod["r0"] * allowed_moves_mod["r1"]

    sol = []
    # print(allowed_moves_mod)
    for i in [n, 0, n + 1, 1, 2 * n - 1, n - 1, -1]:
        done_list = [[goal_state[0]], [goal_state[n]], [goal_state[2 * n]], [goal_state[3 * n]]]
        state = initial_state.copy()
        sol = []
        for k in range(n - 2):
            for j in range(4):
                if k >= n - 3 and j == 3:
                    break
                state, sol_add = add_one(
                    state, goal_state, allowed_moves_mod, done_list,
                    base_index=j, add=goal_state[n * j + k + 1],
                    center=i
                )
                sol = sol + sol_add
                done_list[j].append(goal_state[n * j + k + 1])
                # print(k, j, done_list)
        print(state)
        assert heuristic_0(state, done_list) == 0
        state, sol_add = solve_last(state, goal_state, done_list)
        if sol_add is not None:
            sol = sol + sol_add
            print(f"Success at center {i}")
            break
        else:
            print(f"Failed at center {i}")

    return sol


if __name__ == "__main__":
    # 1x8でテスト（一応全部解ける）
    puzzles_df = pd.read_csv('../input/puzzles.csv')
    puzzles_df_1xn = puzzles_df[puzzles_df["puzzle_type"] == "globe_1/8"]

    for _i, _row in puzzles_df_1xn.iterrows():
        _goal_state = list(_row["solution_state"].split(";"))
        _initial_state = list(_row["initial_state"].split(";"))

        _p = Puzzle(
            _row["id"], _row["puzzle_type"], list(_row["solution_state"].split(";")),
            list(_row["initial_state"].split(";")), _row["num_wildcards"]
        )
        print(_i)
        _sol = solve_1xn(_initial_state, _goal_state, False)

        for _m in _sol:
            _p.operate(_m)
        print(_p.state)
        print(_p.move_history)
        print(len(_p.move_history))
