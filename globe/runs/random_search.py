import numpy as np
import pandas as pd
import datetime
from globe.runs.run_swap import run_swap


class RandomSearch:

    def __init__(self):
        self.path_dict = dict()
        self.length_dict = dict()

    def run_update(self, y, n, seed, p_cost, temperature):
        res, df = run_swap(y, n, seed=seed, p_cost=p_cost, temperature=temperature)
        for i, s in res:
            if i not in self.length_dict.keys():
                self.length_dict[i] = s
                self.path_dict[i] = df[df["id"] == i]["moves"].values[0]
            elif s < self.length_dict[i]:
                print(f"Updated problem {i}: {self.length_dict[i]} -> {s}")
                self.length_dict[i] = s
                self.path_dict[i] = df[df["id"] == i]["moves"].values[0]


if __name__ == "__main__":
    rs = RandomSearch()
    for s in range(20):
        rs.run_update(1, 8, seed=s * 10, p_cost=1.0, temperature=0.0)
        rs.run_update(1, 8, seed=s * 10, p_cost=0.1, temperature=0.0)
        rs.run_update(1, 8, seed=s * 10, p_cost=0.01, temperature=0.0)
        rs.run_update(1, 8, seed=s * 10, p_cost=1.0, temperature=0.01)
        rs.run_update(1, 8, seed=s * 10, p_cost=0.1, temperature=0.01)
        rs.run_update(1, 8, seed=s * 10, p_cost=0.01, temperature=0.01)

    for s in [0, 17, 57, 71]:
        rs.run_update(1, 16, seed=s, p_cost=1.0, temperature=0.0)
        rs.run_update(1, 16, seed=s, p_cost=0.1, temperature=0.0)
        rs.run_update(1, 16, seed=s, p_cost=0.01, temperature=0.0)
        rs.run_update(1, 16, seed=s, p_cost=1.0, temperature=0.01)
        rs.run_update(1, 16, seed=s, p_cost=0.1, temperature=0.01)
        rs.run_update(1, 16, seed=s, p_cost=0.01, temperature=0.01)

    for s in range(50):
        rs.run_update(2, 6, seed=s * 10, p_cost=1.0, temperature=0.0)
        rs.run_update(2, 6, seed=s * 10, p_cost=0.1, temperature=0.0)
        rs.run_update(2, 6, seed=s * 10, p_cost=0.01, temperature=0.0)
        rs.run_update(2, 6, seed=s * 10, p_cost=1.0, temperature=0.01)
        rs.run_update(2, 6, seed=s * 10, p_cost=0.1, temperature=0.01)
        rs.run_update(2, 6, seed=s * 10, p_cost=0.01, temperature=0.01)

    for s in range(50):
        rs.run_update(3, 4, seed=s * 10, p_cost=1.0, temperature=0.0)
        rs.run_update(3, 4, seed=s * 10, p_cost=0.1, temperature=0.0)
        rs.run_update(3, 4, seed=s * 10, p_cost=0.01, temperature=0.0)
        rs.run_update(3, 4, seed=s * 10, p_cost=1.0, temperature=0.01)
        rs.run_update(3, 4, seed=s * 10, p_cost=0.1, temperature=0.01)
        rs.run_update(3, 4, seed=s * 10, p_cost=0.01, temperature=0.01)

    for s in [0, 17, 57, 71]:
        rs.run_update(3, 33, seed=s, p_cost=1.0, temperature=0.0)
        rs.run_update(3, 33, seed=s, p_cost=0.1, temperature=0.0)
        rs.run_update(3, 33, seed=s, p_cost=0.01, temperature=0.0)
        rs.run_update(3, 33, seed=s, p_cost=1.0, temperature=0.01)
        rs.run_update(3, 33, seed=s, p_cost=0.1, temperature=0.01)
        rs.run_update(3, 33, seed=s, p_cost=0.01, temperature=0.01)

    for s in range(30):
        rs.run_update(6, 4, seed=s * 10, p_cost=1.0, temperature=0.0)
        rs.run_update(6, 4, seed=s * 10, p_cost=0.1, temperature=0.0)
        rs.run_update(6, 4, seed=s * 10, p_cost=0.01, temperature=0.0)
        rs.run_update(6, 4, seed=s * 10, p_cost=1.0, temperature=0.01)
        rs.run_update(6, 4, seed=s * 10, p_cost=0.1, temperature=0.01)
        rs.run_update(6, 4, seed=s * 10, p_cost=0.01, temperature=0.01)

    for s in range(20):
        rs.run_update(6, 8, seed=s * 10, p_cost=1.0, temperature=0.0)
        rs.run_update(6, 8, seed=s * 10, p_cost=0.1, temperature=0.0)
        rs.run_update(6, 8, seed=s * 10, p_cost=0.01, temperature=0.0)
        rs.run_update(6, 8, seed=s * 10, p_cost=1.0, temperature=0.01)
        rs.run_update(6, 8, seed=s * 10, p_cost=0.1, temperature=0.01)
        rs.run_update(6, 8, seed=s * 10, p_cost=0.01, temperature=0.01)

    for s in range(20):
        rs.run_update(6, 10, seed=s * 10, p_cost=1.0, temperature=0.0)
        rs.run_update(6, 10, seed=s * 10, p_cost=0.1, temperature=0.0)
        rs.run_update(6, 10, seed=s * 10, p_cost=0.01, temperature=0.0)
        rs.run_update(6, 10, seed=s * 10, p_cost=1.0, temperature=0.01)
        rs.run_update(6, 10, seed=s * 10, p_cost=0.1, temperature=0.01)
        rs.run_update(6, 10, seed=s * 10, p_cost=0.01, temperature=0.01)

    for s in [0, 17, 57, 71]:
        rs.run_update(8, 25, seed=s, p_cost=1.0, temperature=0.0)
        rs.run_update(8, 25, seed=s, p_cost=0.1, temperature=0.0)
        rs.run_update(8, 25, seed=s, p_cost=0.01, temperature=0.0)
        rs.run_update(8, 25, seed=s, p_cost=1.0, temperature=0.01)
        rs.run_update(8, 25, seed=s, p_cost=0.1, temperature=0.01)
        rs.run_update(8, 25, seed=s, p_cost=0.01, temperature=0.01)

    print(rs.length_dict)
    id_list = list(sorted(list(rs.length_dict.keys())))
    moves_list = []
    for i in id_list:
        moves_list.append(rs.path_dict[i])
    res_df = pd.DataFrame({"id": id_list, "moves": moves_list})
    dt_now = datetime.datetime.now()
    res_df.to_csv(
        f"../../output/globe_swap_random_search_{dt_now.strftime('%Y-%m-%d-%H:%M')}.csv", index=False
    )
