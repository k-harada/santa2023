import numpy as np
import pandas as pd
import json
import kociemba
from sympy.combinatorics import Permutation


puzzles_df = pd.read_csv("../input/puzzles.csv")

dict_cube_333 = json.loads(puzzle_info_df["allowed_moves"][1].replace("'", '"'))
perms_cube_333 = {k: Permutation(v) for k, v in dict_cube_333.items()}
for k, v in dict_cube_333.items():
    perms_cube_333["-" + k] = Permutation(v) ** (-1)


if __name__ == "__main__":
    print(perms_cube_333["r0"])
    print(perms_cube_333["r0"] * perms_cube_333["d0"] * perms_cube_333["-r0"])
    print(perms_cube_333["r1"] * perms_cube_333["d0"] * perms_cube_333["-r1"])
    print(kociemba.solve('DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD'))
