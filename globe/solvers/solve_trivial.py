# 2/6とかの真ん中の自明なやつを解くだけのコード
# 左と右に回して短い方を吐き出す

def solve_trivial(initial_state_sub, goal_state):
    res_plus = 0
    temp = initial_state_sub.copy()
    while temp != goal_state:
        temp = temp[1:] + [temp[0]]
        res_plus += 1
    res_minus = 0
    temp = initial_state_sub.copy()
    while temp != goal_state:
        temp = [temp[-1]] + temp[:-1]
        res_minus += 1
    if res_plus <= res_minus:
        return ["r0"] * res_plus
    else:
        return ["-r0"] * res_minus


if __name__ == "__main__":
    x = [2, 3, 4, 0, 1]
    y = [0, 1, 2, 3, 4]
    print(solve_trivial(x, y))
    print(solve_trivial(y, x))
