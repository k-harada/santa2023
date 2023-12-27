import numpy as np
import pandas as pd
import json
import kociemba
from sympy.combinatorics import Permutation
from puzzle import Puzzle


action_list = ["f0", "f1", "r0", "r1", "d0", "d1", "-f0", "-f1", "-r0", "-r1", "-d0", "-d1"]


def solve_2x2_random(puzzle: Puzzle):
    score_now = sum([a == b for a, b in zip(puzzle.state, puzzle.solution_state)])
    print(score_now)
    t = 0
    h = 10.0
    while True:
        if score_now == 24:
            print("solved")
            break
        score_list = []
        for m in action_list:
            puzzle.operate(m)
            score_after = sum([a == b for a, b in zip(puzzle.state, puzzle.solution_state)])
            score_list.append(np.exp(score_after - score_now) / h)
            puzzle.undo()
        # print(score_list)
        m = np.random.choice(action_list, p=np.array(score_list) / sum(score_list))
        puzzle.operate(m)
        score_now = sum([a == b for a, b in zip(puzzle.state, puzzle.solution_state)])
        t += 1
        if t % 100 == 0:
            print(t, len(puzzle.move_history), score_now)
        if t == 10000:
            return puzzle
    return puzzle


puzzles_df = pd.read_csv("../input/puzzles.csv")
puzzles_df_2x2 = puzzles_df.iloc[:30, :]


if __name__ == "__main__":
    row = puzzles_df_2x2.iloc[2, :]
    print(row)
    _p = Puzzle(
        row["id"], row["puzzle_type"], list(row["solution_state"].split(";")),
        list(row["initial_state"].split(";")), row["num_wildcards"]
    )
    _p = solve_2x2_random(_p)
