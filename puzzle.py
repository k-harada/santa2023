from sympy.combinatorics import Permutation
from ast import literal_eval
from typing import Dict, List
import pandas as pd


puzzle_info_df = pd.read_csv('../input/puzzle_info.csv', index_col='puzzle_type')


class Puzzle:
    """A permutation puzzle."""

    def __init__(
            self, puzzle_id: int, puzzle_type: str,
            solution_state: List[str], initial_state: List[str], num_wildcards: int,
            handmade_type: bool = False
    ):

        self.puzzle_id: int = puzzle_id
        self.puzzle_type: str = puzzle_type
        self.solution_state: List[str] = solution_state
        self.initial_state: List[str] = initial_state
        self.num_wildcards: int = num_wildcards
        self.state = initial_state.copy()
        if handmade_type:
            self.allowed_moves: Dict[str, Permutation] = dict()
        else:
            allowed_moves = literal_eval(puzzle_info_df.loc[self.puzzle_type, 'allowed_moves'])
            self.allowed_moves: Dict[str, Permutation] = {k: Permutation(v) for k, v in allowed_moves.items()}
        self.move_history = []

    def __str__(self):
        return self.state.__str__()

    def __repr__(self):
        return self.state.__repr__()

    def reset(self):
        self.state = self.initial_state.copy()
        self.move_history = []

    def operate(self, move: str):
        if move[0] == "-":
            m = move[1:]
            power = -1
        else:
            m = move
            power = 1
        p = self.allowed_moves[m]
        self.state = (p ** power)(self.state)
        self.move_history.append(move)

    def undo(self):
        assert len(self.move_history) > 0
        move = self.move_history.pop()
        if move[0] == "-":
            m = move[1:]
            power = 1
        else:
            m = move
            power = -1
        p = self.allowed_moves[m]
        self.state = (p ** power)(self.state)
