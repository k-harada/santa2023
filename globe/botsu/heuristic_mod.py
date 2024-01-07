from typing import Dict, List
from sympy.combinatorics import Permutation
from heapq import heappop, heappush


def heuristic_0(x: List[str], done_list: List[List[str]]):
    res = 4
    n = len(x) // 4
    string_upper = "_".join(["."] + x[:2 * n] + x[:2 * n] + ["."])
    string_lower = "_".join(["."] + x[2 * n:] + x[2 * n:] + ["."])
    x0 = "_" + "_".join(done_list[0]) + "_"
    x0_rev = "_" + "_".join(reversed(done_list[0])) + "_"
    x1 = "_" + "_".join(done_list[1]) + "_"
    x1_rev = "_" + "_".join(reversed(done_list[1])) + "_"
    x2 = "_" + "_".join(done_list[2]) + "_"
    x2_rev = "_" + "_".join(reversed(done_list[2])) + "_"
    x3 = "_" + "_".join(done_list[3]) + "_"
    x3_rev = "_" + "_".join(reversed(done_list[3])) + "_"
    count_upper = 0
    count_lower = 0
    if string_upper.find(x0) >= 0:
        res -= 1
        count_upper += 1
    elif string_lower.find(x0_rev) >= 0:
        res -= 1
        count_lower += 1

    if string_upper.find(x1) >= 0:
        res -= 1
        count_upper += 1
    elif string_lower.find(x1_rev) >= 0:
        res -= 1
        count_lower += 1

    if string_lower.find(x2) >= 0:
        res -= 1
        count_lower += 1
    elif string_upper.find(x2_rev) >= 0:
        res -= 1
        count_upper += 1

    if string_lower.find(x3) >= 0:
        res -= 1
        count_lower += 1
    elif string_upper.find(x3_rev) >= 0:
        res -= 1
        count_upper += 1
    if max(count_lower, count_upper) >= 3 and len(done_list[3]) >= max(n // 3, 2):
        res += 10
    return res


def calc_dist(x: int, y: int, n: int, center: int):
    return 1
    """
    if x == y:
        return 0
    if center == -1:
        if max(x, y) < 2 * n or min(x, y) >= 2 * n:
            if (x - y) % 2 == 0:
                return 2
            else:
                return 3
        else:
            if (max(x, y) + n) % (2 * n) == min(x, y):
                return 1
            elif (x - y) % 2 == 0:
                return 3
            else:
                return 4
    return 0
    """


def heuristic(
        x: List[str], y: List[str], done_list: List[List[str]],
        base_index: int = 0, add: str = "", center: int = -1
):
    h0 = heuristic_0(x, done_list)
    n = len(x) // 4
    if add == "":
        return h0
    if h0 > 0:
        return h0 * 1000
    # find index for base
    base_list = done_list[base_index]
    string_upper = "_".join(["."] + x[:2 * n] + x[:2 * n] + ["."])
    string_lower = "_".join(["."] + x[2 * n:] + x[2 * n:] + ["."])
    x_joint = "_" + "_".join(base_list) + "_"
    x_joint_add = x_joint + add + "_"

    if base_index in [0, 1]:
        if string_upper.find(x_joint_add) >= 0 or string_lower.find("".join(list(reversed(x_joint_add)))) >= 0:
            return 0
    else:
        if string_lower.find(x_joint_add) >= 0 or string_upper.find("".join(list(reversed(x_joint_add)))) >= 0:
            return 0

    if base_index in [0, 1]:
        s_up = string_upper.find(x_joint)
        if s_up >= 0:
            start_ind = string_upper[:s_up].count("_") - 1
            x_ = x.copy()
        else:
            x_ = list(reversed(x[2 * n:])) + list(reversed(x[:2 * n]))
            string_upper = "_".join(["."] + x_[:2 * n] + x_[:2 * n] + ["."])
            s_up = string_upper.find(x_joint)
            assert s_up >= 0
            start_ind = string_upper[:s_up].count("_") - 1
    else:
        s_low = string_lower.find(x_joint)
        if s_low >= 0:
            start_ind = string_lower[:s_low].count("_") - 1
            x_ = x[2 * n:] + x[:2 * n]
        else:
            x_ = list(reversed(x[:2 * n])) + list(reversed(x[2 * n:]))
            string_upper = "_".join(["."] + x_[:2 * n] + x_[:2 * n] + ["."])
            s_low = string_upper.find(x_joint)
            assert s_low >= 0
            start_ind = string_upper[:s_low].count("_") - 1

    used = [0] * (4 * n)
    if start_ind >= 2 * n:
        for i in range(start_ind, start_ind + len(base_list)):
            used[i % (2 * n)] = 1
        target_ind = (start_ind + len(base_list) - 1) % (2 * n)
    else:
        for i in range(start_ind, start_ind + len(base_list)):
            used[i % (2 * n) + 2 * n] = 1
        target_ind = (start_ind + len(base_list) - 1) % (2 * n) + 2 * n

    res = 10000000
    for i_add in range(4 * n):
        if x_[i_add] == add and used[i_add] == 0:
            res = min(res, calc_dist(i_add, target_ind, n, center))
    return res
