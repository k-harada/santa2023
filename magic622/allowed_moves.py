import numpy as np
import pandas as pd
import os
from ast import literal_eval
from typing import Dict, List, Optional
from sympy.combinatorics import Permutation

puzzle_info_df = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "../input/puzzle_info.csv"), index_col='puzzle_type'
)


def get_allowed_moves_48(puzzle_type: str, diag: bool = False):
    assert puzzle_type in ["cube_6/6/6"]
    if puzzle_type == "cube_6/6/6":
        n = 6
        pick_index = []
        for i in range(6):
            pick_index.append(8 + i * 36)
            pick_index.append(9 + i * 36)
            pick_index.append(13 + i * 36)
            pick_index.append(16 + i * 36)
            pick_index.append(19 + i * 36)
            pick_index.append(22 + i * 36)
            pick_index.append(26 + i * 36)
            pick_index.append(27 + i * 36)
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
    print(get_allowed_moves_48("cube_6/6/6"))
