import pandas as pd
import datetime

new_list = [
    "../output/globe_swap_random_search_2024-01-14-00:43.csv",
    "../output/wreath100_random_732.csv",
    "../output/wreath_small_greed.csv",
]

sample_df = pd.read_csv("../submissions/submission_404515.csv")
length_list = [0] * sample_df.shape[0]
res = []

for i, row in sample_df.iterrows():
    length_list[i] = row["moves"].count(".") + 1
    res.append(row["moves"])

for file in new_list:
    new_df = pd.read_csv(file)
    for i, row in new_df.iterrows():
        new_len = row["moves"].count(".") + 1
        if new_len < length_list[row["id"]]:
            length_list[row["id"]] = new_len
            res[row["id"]] = row["moves"]


if __name__ == "__main__":
    print(sum(length_list))
    dt_now = datetime.datetime.now()
    pd.DataFrame({"id": sample_df["id"], "moves": res}).to_csv(
        f"../submissions/sub_harada_{dt_now.strftime('%Y-%m-%d-%H-%M')}.csv", index=False
    )
