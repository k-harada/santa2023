import pandas as pd
import datetime

new_list = [
    "../output/globe_2x6_2024-01-08-01:35.csv",
    "../output/globe_3x4_2024-01-08-01:47.csv",
    "../output/globe_6x4_2024-01-08-01:59.csv",
    "../output/globe_6x8_2024-01-08-02:03.csv",
    "../output/globe_6x10_2024-01-08-02:18.csv",
    "../output/globe_1x16_2024-01-10-02:54.csv",
    "../output/globe_1x16_2024-01-11-16:55.csv",
    "../output/globe_3x33_2024-01-10-02:48.csv",
    "../output/globe_3x33_2024-01-11-16:58.csv",
    "../output/globe_3x33_2024-01-11-18:34.csv",
    "../output/globe_8x25_2024-01-10-02:57.csv",
    "../output/globe_8x25_2024-01-11-16:51.csv",
]

sample_df = pd.read_csv("../output/submission_719501.csv")
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
        f"../submissions/sub_harada_{dt_now.strftime('%Y-%m-%d-%H:%M')}.csv", index=False
    )
