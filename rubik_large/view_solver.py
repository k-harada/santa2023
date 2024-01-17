import numpy as np
import pandas as pd
import math
from puzzle import Puzzle


puzzles_df = pd.read_csv("../input/puzzles.csv")
sub_df = pd.read_csv("../submissions/submission_404515.csv")


def run_rubik(problem_id: int, n_step: int):
    for _, row in pd.merge(puzzles_df, sub_df).iterrows():
        if row["id"] == problem_id:
            break
    else:
        raise ValueError(f"id {problem_id} is not in problems")

    assert row["puzzle_type"][:5] == "cube_"
    p = Puzzle(
        puzzle_id=row["id"], puzzle_type=row["puzzle_type"],
        solution_state=list(row["solution_state"].split(";")),
        initial_state=list(row["initial_state"].split(";")),
        num_wildcards=row["num_wildcards"]
    )
    solution_moves = list(row["moves"].split("."))
    print(solution_moves)
    print(solution_moves[:n_step])
    for i, m in enumerate(solution_moves[:n_step]):
        p.operate(m)
        if center_aligned(p, 3):
            print(i)
            print_cube(p)
            print(len(p.move_history))
            print(p.move_history)
    return p


def center_aligned(p, k):
    n = int(math.sqrt(len(p.state) // 6))
    c = (n - 1) // 2
    for x in range(6):
        color_set = set()
        for i in range(c - k, c + k + 1):
            for j in range(c - k, c + k + 1):
                color_set.add(p.state[x * n * n + i * n + j])
        if len(color_set) > 1:
            return False
    return True


def print_cube(p):
    n = int(math.sqrt(len(p.state) // 6))
    i = 0
    for _ in range(6):
        print("_" * n)
        for _1 in range(n):
            print("".join(p.state[i:i+n]))
            i += n
    print("_" * (2 * n))


if __name__ == "__main__":
    # _p = run_rubik(270, 586 + 1)
    _p = run_rubik(270, 9000)
