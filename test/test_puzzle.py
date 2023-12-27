import pandas as pd
from puzzle import Puzzle


if __name__ == "__main__":
    puzzles_df = pd.read_csv('../input/puzzles.csv')

    row = puzzles_df.iloc[130]
    p = Puzzle(
        row["id"], row["puzzle_type"], list(row["solution_state"].split(";")),
        list(row["initial_state"].split(";")), row["num_wildcards"]
    )
