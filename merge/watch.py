import pandas as pd

sub_path = "../submissions/submission_172234.csv"

sub_df = pd.read_csv(sub_path)
sub_df["length"] = sub_df["moves"].map(lambda x: x.count(".") + 1)
puzzles_df = pd.read_csv("../input/puzzles.csv")
puzzles_sub_df = pd.merge(puzzles_df, sub_df[["id", "length"]])
puzzles_sub_df["solu"] = puzzles_sub_df["solution_state"].str.slice(0, 6)


if __name__ == "__main__":
    calc = puzzles_sub_df.groupby(["puzzle_type", "solu"])["length"].agg([
        "size", "sum", "mean", "min", "max"
    ])
    print(calc)
    calc = puzzles_sub_df.groupby(["puzzle_type"])["length"].agg([
        "size", "sum", "mean", "min", "max"
    ])
    print(calc)
