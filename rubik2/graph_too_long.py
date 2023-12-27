from sympy.combinatorics import Permutation
from ast import literal_eval
from typing import Dict, List
from collections import deque

import numpy as np
import pandas as pd


puzzle_info_df = pd.read_csv('../input/puzzle_info.csv', index_col='puzzle_type')
puzzles_df = pd.read_csv('../input/puzzles.csv')

allowed_moves_ = literal_eval(puzzle_info_df.loc['cube_2/2/2', 'allowed_moves'])
allowed_moves: Dict[str, Permutation] = dict()
for k, v_ in allowed_moves_.items():
    v = Permutation(v_)
    allowed_moves[k] = v
    allowed_moves["-" + k] = v ** (-1)

graph: Dict[Permutation, Dict[str, Permutation]] = dict()
graph[Permutation(24)] = dict()
queue = deque([Permutation(24)])

i = 0
while len(queue):
    p = queue.popleft()
    for k, v in allowed_moves.items():
        q = v * p
        if q not in graph.keys():
            queue.append(q)
            graph[q] = dict()
        graph[p][k] = q
    print(i)
    i += 1


if __name__ == "__main__":
    p = Permutation(24)
    s = p.__str__()
    print(s)
    print(allowed_moves)
