import numpy as np
import pandas as pd
import os
from ast import literal_eval
from typing import Dict, List, Optional
from sympy.combinatorics import Permutation


puzzle_info_df = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "../input/puzzle_info.csv"), index_col='puzzle_type'
)


def get_allowed_moves_48(puzzle_type: str):
    assert puzzle_type in ["cube_4/4/4", "cube_5/5/5", "cube_6/6/6"]
    if puzzle_type == "cube_4/4/4":
        n = 4
        pick_index = []
        for i in range(6):
            pick_index.append(1 + i * 16)
            pick_index.append(2 + i * 16)
            pick_index.append(4 + i * 16)
            pick_index.append(7 + i * 16)
            pick_index.append(8 + i * 16)
            pick_index.append(11 + i * 16)
            pick_index.append(13 + i * 16)
            pick_index.append(14 + i * 16)
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
    print(get_allowed_moves_48("cube_4/4/4"))
    # print(get_allowed_moves_32("cube_5/5/5"))
    # print(get_allowed_moves_32("cube_6/6/6"))
