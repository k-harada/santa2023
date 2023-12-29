import numpy as np
import pandas as pd
import json
import kociemba
from sympy.combinatorics import Permutation
from puzzle import Puzzle


kaggle_to_kociemba = [
    0, 1, 2, 3, 4, 5, 6, 7, 8,
    18, 19, 20, 21, 22, 23, 24, 25, 26,
    9, 10, 11, 12, 13, 14, 15, 16, 17,
    45, 46, 47, 48, 49, 50, 51, 52, 53,
    36, 37, 38, 39, 40, 41, 42, 43, 44,
    27, 28, 29, 30, 31, 32, 33, 34, 35
]

kociemba_to_kaggle = {
    "R": "r0",
    "R2": "r0.r0",
    "R'": "-r0",
    "L": "-r2",
    "L2": "r2.r2",
    "L'": "r2",
    "F": "f0",
    "F2": "f0.f0",
    "F'": "-f0",
    "B": "-f2",
    "B2": "f2.f2",
    "B'": "f2",
    "D": "d0",
    "D2": "d0.d0",
    "D'": "-d0",
    "U": "-d2",
    "U2": "d2.d2",
    "U'": "d2",
}


def solve_3x3_normalize(puzzle: Puzzle):
    # greedy
    if puzzle.state[4] != puzzle.solution_state[4]:
        for m in ["f1", "-f1", "r1", "-r1"]:
            puzzle.operate(m)
            if puzzle.state[4] == puzzle.solution_state[4]:
                break
            else:
                puzzle.undo()
        else:
            puzzle.operate("f1")
            puzzle.operate("f1")
    if puzzle.state[13] != puzzle.solution_state[13]:
        for m in ["d1", "-d1"]:
            puzzle.operate(m)
            if puzzle.state[13] == puzzle.solution_state[13]:
                break
            else:
                puzzle.undo()
        else:
            puzzle.operate("d1")
            puzzle.operate("d1")
    return puzzle


def solve_3x3_kociemba(initial_state_normalized):
    char_map = dict()
    char_map_inv = dict()
    for a, b in zip([initial_state_normalized[9 * i + 4] for i in range(6)], ['U', 'F', 'R', 'B', 'L', 'D']):
        char_map[a] = b
        char_map_inv[b] = a

    initial_state_kociemba = [""] * 54
    for i, c in enumerate(initial_state_normalized):
        initial_state_kociemba[kaggle_to_kociemba[i]] = char_map[c]

    sol_kociemba = kociemba.solve("".join(initial_state_kociemba))
    sol = ".".join([kociemba_to_kaggle[m] for m in sol_kociemba.split()])
    # print(sol)
    return sol


puzzles_df = pd.read_csv("../input/puzzles.csv")
puzzles_df_3x3 = puzzles_df[puzzles_df["puzzle_type"] == "cube_3/3/3"]
sample_df = pd.read_csv("../input/sample_submission.csv", index_col='id')


if __name__ == "__main__":

    _id_list = []
    _moves_list = []

    for _i, row in puzzles_df_3x3.iterrows():
        clean_solution = ";".join(
            ["A"] * 9 + ["B"] * 9 +["C"] * 9 + ["D"] * 9 + ["E"] * 9 +["F"] * 9
        )

        # original
        _p = Puzzle(
            row["id"], row["puzzle_type"], list(row["solution_state"].split(";")),
            list(row["initial_state"].split(";")), row["num_wildcards"]
        )

        if row["solution_state"] == clean_solution:
            # print(_i)
            _p = solve_3x3_normalize(_p)
            # initial_state_normalized_ = solve_3x3_normalize(row["initial_state"])
            _sol = solve_3x3_kociemba(_p.state)
            for _m in _sol.split("."):
                _p.operate(_m)
        else:
            # reverse sample operation
            dummy_p = Puzzle(
                row["id"], row["puzzle_type"], list(row["solution_state"].split(";")),
                list(clean_solution.split(";")), row["num_wildcards"]
            )
            for move in reversed(sample_df.loc[_i, "moves"].split(".")):
                if move[0] == "-":
                    dummy_p.operate(move[1:])
                else:
                    dummy_p.operate("-" + move)

            dummy_pp = Puzzle(
                row["id"], row["puzzle_type"], list(clean_solution.split(";")),
                dummy_p.state, row["num_wildcards"]
            )
            dummy_pp = solve_3x3_normalize(dummy_pp)
            # initial_state_normalized_ = solve_3x3_normalize(row["initial_state"])
            _sol = solve_3x3_kociemba(dummy_pp.state)
            for _m in _sol.split("."):
                dummy_pp.operate(_m)
            for _m in dummy_pp.move_history:
                _p.operate(_m)

        print(_p)
        print(_p.move_history)
        print(_p.solution_state)
        assert _p.state == _p.solution_state

        _id_list.append(_i)
        _moves_list.append(".".join(_p.move_history))
    pd.DataFrame({"id": _id_list, "moves": _moves_list}).to_csv("../output/solve_3x3_kociemba_1229.csv", index=False)

