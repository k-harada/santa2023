import numpy as np
import pandas as pd
import os
from ast import literal_eval
from typing import Dict, List, Optional
from sympy.combinatorics import Permutation


puzzle_info_df = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "../input/puzzle_info.csv"), index_col='puzzle_type'
)


def get_allowed_moves_72(puzzle_type: str):
    assert puzzle_type in ["cube_4/4/4", "cube_5/5/5", "cube_6/6/6"]
    if puzzle_type == "cube_5/5/5":
        n = 5
        pick_index = []
        for i in range(6):
            pick_index.append(1 + i * 25)
            pick_index.append(2 + i * 25)
            pick_index.append(3 + i * 25)
            pick_index.append(5 + i * 25)
            pick_index.append(9 + i * 25)
            pick_index.append(10 + i * 25)
            pick_index.append(14 + i * 25)
            pick_index.append(15 + i * 25)
            pick_index.append(19 + i * 25)
            pick_index.append(21 + i * 25)
            pick_index.append(22 + i * 25)
            pick_index.append(23 + i * 25)
    else:
        raise NotImplemented

    allowed_moves_ = literal_eval(puzzle_info_df.loc[puzzle_type, 'allowed_moves'])
    allowed_moves: Dict[str, Permutation] = {k: Permutation(v) for k, v in allowed_moves_.items()}
    # to numpy
    allowed_moves_arr: Dict[str, np.array] = dict()
    for k in allowed_moves.keys():
        xxx = allowed_moves[k](np.arange(n * n * 6))
        xxx_ = np.arange(n * n * 6)[xxx]
        allowed_moves_arr[k] = np.array([pick_index.index(y) for y in (xxx_[pick_index])])
        xxx = (allowed_moves[k] ** (-1))(np.arange(n * n * 6))
        xxx_ = np.arange(n * n * 6)[xxx]
        allowed_moves_arr["-" + k] = np.array([pick_index.index(y) for y in (xxx_[pick_index])])

    return allowed_moves_arr


if __name__ == "__main__":
    print(get_allowed_moves_72("cube_5/5/5"))
