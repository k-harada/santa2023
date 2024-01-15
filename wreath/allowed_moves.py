import numpy as np
import pandas as pd
import os
from ast import literal_eval
from typing import Dict, List, Optional
from sympy.combinatorics import Permutation

puzzle_info_df = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "../input/puzzle_info.csv"), index_col='puzzle_type'
)


def get_allowed_moves(puzzle_type: str):
    assert puzzle_type in ["wreath_6/6", "wreath_7/7", "wreath_12/12", "wreath_21/21", "wreath_33/33", "wreath_100/100"]
    allowed_moves_ = literal_eval(puzzle_info_df.loc[puzzle_type, 'allowed_moves'])
    allowed_moves: Dict[str, Permutation] = {k: Permutation(v) for k, v in allowed_moves_.items()}
    allowed_moves["-l"] = allowed_moves["l"] ** (-1)
    allowed_moves["-r"] = allowed_moves["r"] ** (-1)
    return allowed_moves


if __name__ == "__main__":
    print(get_allowed_moves("wreath_6/6"))
