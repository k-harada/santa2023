import numpy as np
import pandas as pd
from itertools import combinations
from typing import Dict, List, Optional
from puzzle import Puzzle
from collections import deque

from wreath.allowed_moves import get_allowed_moves
from wreath.decipher_magic import triangle_up_1, triangle_up_2, triangle_low_1, triangle_low_2


def get_state_100():
    puzzle_df = pd.read_csv("../input/puzzles.csv")
    wreath_df = puzzle_df[puzzle_df["puzzle_type"].str.slice(0, 3) == "wre"]
    for i, row in wreath_df.iterrows():
        if row["puzzle_type"] == "wreath_100/100":
            return row
    return None


def get_lr(n):
    # lrを何回かやったときにどうなっているべきかの計算用
    row = get_state_100()
    sol_state = list(row["solution_state"].split(";"))
    p = Puzzle(
        puzzle_id=11100, puzzle_type="wreath_100/100",
        solution_state=sol_state, initial_state=sol_state,
        num_wildcards=8
    )
    for _ in range(n):
        p.operate("l")
        p.operate("r")
    return p


def run_heuristic(initial_state, goal_state, num_wildcards, seed, k):
    np.random.seed(seed)
    p = Puzzle(
        puzzle_id=10100, puzzle_type="wreath_100/100",
        solution_state=goal_state, initial_state=initial_state,
        num_wildcards=num_wildcards
    )
    for t in range(148):
        if p.state[25] != "A" and p.state[0] != "A":
            p.operate("r")
        elif p.state[25] != "B" and p.state[0] != "B":
            p.operate("-l")
        else:
            if p.state[25] == "B":
                p.operate("r")
            else:
                p.operate("-l")
        r = 0
        for x, y in zip(p.state, p.solution_state):
            if x != y:
                r += 1
        # print(t, r, len(p.move_history), p.state)
    # print(p.state[26:100])
    # print(p.state[100:173])
    for _ in range(k):
        p.operate("l")
        p.operate("r")
    # print(p.state[26:100])
    # print(p.state[100:173])
    # print(p.state[0], p.state[25])
    q = get_lr(k)
    # print(q.state[26:100])
    # print(q.state[100:173])
    # print(q.state[0], q.state[25])
    # print(p.state[1:25])
    # print(q.state[1:25])
    # print(p.state[173:198])
    # print(q.state[173:198])

    # random try
    for t in range(10000):
        res_diff = 0
        res_diff_add = 0
        for i in range(198):
            x, y = p.state[i], q.state[i]
            if x != y and i not in [0, 25]:
                res_diff += 1
            elif x != y and i in [0, 25]:
                res_diff_add += 1
        # print(res_diff, len(p.move_history))
        if res_diff + res_diff_add <= num_wildcards:
            break
        i, j = np.random.choice(range(k), 2, replace=False)
        f = np.random.choice(4)
        if f == 0:
            op = triangle_up_1(i, j)
        elif f == 1:
            op = triangle_up_2(i, j)
        elif f == 2:
            op = triangle_low_1(i, j)
        else:
            op = triangle_low_2(i, j)
        for m in op:
            p.operate(m)
        res_diff_new = 0
        for i in range(198):
            x, y = p.state[i], q.state[i]
            if x != y and i not in [0, 25]:
                res_diff_new += 1
        if res_diff_new >= res_diff:
            for _ in range(len(op)):
                p.undo()
        # print(p.state)
        # print(q.state)
    else:
        return None

    for _ in range(k):
        p.operate("-r")
        p.operate("-l")

    # undo trivial
    res_list = []
    for m in p.move_history:
        if len(res_list) == 0:
            res_list.append(m)
        else:
            lm = res_list.pop()
            if "-" + m == lm or m == "-" + lm:
                continue
            else:
                res_list.append(lm)
                res_list.append(m)
    return res_list


if __name__ == "__main__":
    np.random.seed(20240115)
    _row = get_state_100()
    _initial_state = list(_row["initial_state"].split(";"))
    _goal_state = list(_row["solution_state"].split(";"))
    _num_wildcards = int(_row["num_wildcards"])
    # print(_row)
    best_path = run_heuristic(_initial_state, _goal_state, _num_wildcards, seed=0, k=23)
    best_len = len(best_path)
    for _t in range(1000):
        seed = np.random.choice(10000)
        k = np.random.choice(range(16, 25))
        path = run_heuristic(_initial_state, _goal_state, _num_wildcards, seed=seed, k=k)
        if path is None:
            print("fail:", _t, seed, k)
            continue
        if len(path) < best_len:
            best_path = path
            best_len = len(best_path)
            print("best:", _t, k, seed, best_len)
        else:
            print("not best:", _t, k, seed, len(path))
    # check
    p = Puzzle(
        puzzle_id=11111, puzzle_type="wreath_100/100",
        solution_state=_goal_state, initial_state=_initial_state,
        num_wildcards=_num_wildcards
    )
    for _m in best_path:
        p.operate(_m)
    res_diff = 0
    for x, y in zip(p.state, p.solution_state):
        if x != y:
            res_diff += 1
    assert res_diff <= _num_wildcards
    print(len(best_path))
    res_df = pd.DataFrame({
        "id": [_row["id"]], "moves": [".".join(best_path)]
    })
    res_df.to_csv(f"../output/wreath100_random_{len(best_path)}.csv", index=False)
