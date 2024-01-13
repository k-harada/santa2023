import numpy as np
import pandas as pd
from puzzle import Puzzle
import datetime
from typing import Optional
from globe.solvers.swap_1xn import SwapSolver
from globe.solvers.trivial_center import solve_trivial
from globe.solvers.merge_flips import merge_flips


def run_swap(
        y, n, dry_run: bool = True, seed: int = 0,
        temperature: Optional[float] = None, p_cost: Optional = None
):
    puzzles_df = pd.read_csv('../../input/puzzles.csv')
    if y == 33:
        puzzles_df_pick = pd.concat([
            puzzles_df[puzzles_df["puzzle_type"] == f"globe_{y}/{n}"],
            puzzles_df[puzzles_df["puzzle_type"] == f"globe_{n}/{y}"]
        ], axis=0)
    else:
        puzzles_df_pick = puzzles_df[puzzles_df["puzzle_type"] == f"globe_{y}/{n}"]
    dt_now = datetime.datetime.now()
    id_list = []
    moves_list = []
    score_list = []

    for i, row in puzzles_df_pick.iterrows():
        goal_state_all = list(row["solution_state"].split(";"))
        initial_state_all = list(row["initial_state"].split(";"))
        print(f"start i = {i}")
        print("initial_state:", initial_state_all)
        print("goal_state:", goal_state_all)

        sol_all = [[] for _ in range((y + 2) // 2)]

        for j in range((y + 1) // 2):
            # sol = []
            if j > 0:
                left = j * (2 * n)
                right = (j + 1) * (2 * n)
                initial_state = initial_state_all[left:right] + initial_state_all[-right:-left]
                goal_state = goal_state_all[left:right] + goal_state_all[-right:-left]
            else:
                initial_state = initial_state_all[:2 * n] + initial_state_all[-2 * n:]
                goal_state = goal_state_all[:2 * n] + goal_state_all[-2 * n:]
            print("sub problem:", j)
            print("initial_state:", initial_state)
            print("goal_state:", goal_state)

            solver = SwapSolver(n)
            # seed = 0
            # res_list = []
            # for _ in range(10):
            #     np.random.seed(seed)
            #     solver.initialize(initial_state, goal_state)
            #     r = solver.align_up_down(random=True)
            #     s = len(solver.path)
            #     np.random.seed(seed)
            #     solver.initialize(initial_state, goal_state)
            #     solver.solve(random=True)
            #     res_list.append((r, s, len(solver.path)))
            #     seed += 1
            # print(res_list)
            solver.initialize(initial_state, goal_state, temperature=temperature, p_cost=p_cost)
            np.random.seed(seed)
            solver.solve(random=True)
            if solver.path is None:
                seed += 1
                while True:
                    np.random.seed(seed)
                    solver.initialize(initial_state, goal_state, temperature=temperature, p_cost=p_cost)
                    seed += 1
                    solver.solve(random=True)
                    if solver.path is not None:
                        break
            # print(seed, len(solver.path))
            sol = solver.path

            sol_add = solve_trivial(list(solver.state[:2 * n]), goal_state[:2 * n])
            for m in sol_add:
                if m == "r0":
                    sol.append("r0")
                elif m == "-r0":
                    sol.append("-r0")

            sol_add = solve_trivial(list(solver.state[2 * n:]), goal_state[2 * n:])
            for m in sol_add:
                if m == "r0":
                    sol.append("r1")
                elif m == "-r0":
                    sol.append("-r1")

            for m in sol:
                if m[0] == "f":
                    sol_all[j].append(m)
                elif m == "r0":
                    sol_all[j].append(f"r{j}")
                elif m == "-r0":
                    sol_all[j].append(f"-r{j}")
                elif m == "r1":
                    sol_all[j].append(f"r{y - j}")
                elif m == "-r1":
                    sol_all[j].append(f"-r{y - j}")

        if y % 2 == 0:
            # center
            c = n * y
            sol_add = solve_trivial(initial_state_all[c:-c], goal_state_all[c:-c])
            for m in sol_add:
                if m == "r0":
                    sol_all[y // 2].append(f"r{y // 2}")
                elif m == "-r0":
                    sol_all[y // 2].append(f"-r{y // 2}")
        if y >= 3:
            sol_all_flat = zip_path(sol_all)
        else:
            sol_all_flat = []
            for sol in sol_all:
                sol_all_flat = sol_all_flat + sol

        # check
        p = Puzzle(
            row["id"], row["puzzle_type"], list(row["solution_state"].split(";")),
            list(row["initial_state"].split(";")), row["num_wildcards"]
        )
        for m in sol_all_flat:
            p.operate(m)
        print(p.state)
        assert p.state == p.solution_state
        print(f"i = {i} Done, score = {len(p.move_history)}")
        id_list.append(i)
        moves_list.append(".".join(p.move_history))
        score_list.append((i, len(p.move_history)))
        print(p.move_history)

    res_df = pd.DataFrame({"id": id_list, "moves": moves_list})
    if not dry_run:
        res_df.to_csv(
            f"../../output/globe_swap_{y}x{n}_{dt_now.strftime('%Y-%m-%d-%H:%M')}.csv", index=False
        )
    return score_list, res_df


def zip_path(path_list):
    yy = len(path_list)
    path = path_list[0]
    for i in range(1, yy):
        r, path = merge_flips(path, path_list[i])
    return path


if __name__ == "__main__":
    # _res, _df = run_swap(1, 8, seed=78, p_cost=1.0, temperature=0.0)
    # _res, _df = run_swap(1, 16, seed=78, p_cost=1.0, temperature=0.0)
    # _res, _df = run_swap(2, 6, seed=78, p_cost=1.0, temperature=0.0)
    # _res, _df = run_swap(3, 4, seed=78, p_cost=1.0, temperature=0.0)
    # _res, _df = run_swap(3, 33, seed=78, p_cost=1.0, temperature=0.0)
    # _res, _df = run_swap(6, 4, seed=78, p_cost=1.0, temperature=0.0)
    # _res, _df = run_swap(6, 8, seed=78, p_cost=1.0, temperature=0.0)
    # _res, _df = run_swap(6, 10, seed=78, p_cost=1.0, temperature=0.0)
    _res, _df = run_swap(8, 25, seed=78, p_cost=1.0, temperature=0.0)
    _s_sum = 0
    for _i, _s in _res:
        print(_i, _s)
        _s_sum += _s
    print(_s_sum)
