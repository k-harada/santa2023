from typing import List


def heuristic(x: List[str], y: List[str]):
    n = len(x) // 4
    res = 4 * n - 8
    exist_up = []
    exist_down = []
    for i in range(2 * n):
        exist_up.append(x[i] + x[(i + 1) % (2 * n)])
        exist_down.append(x[(i + 1) % (2 * n)] + x[i])
        exist_up.append(x[(i + 1) % (2 * n) + 2 * n] + x[i + 2 * n])
        exist_down.append(x[i + 2 * n] + x[(i + 1) % (2 * n) + 2 * n])
    for j in range(4):
        if y[j * n + 0] + y[j * n + 1] in exist_up:
            res -= 1
            for i in range(1, n - 2):
                if y[j * n + i] + y[j * n + i + 1] in exist_up:
                    res -= 1
                else:
                    break
        elif y[j * n + 0] + y[j * n + 1] in exist_down:
            res -= 1
            for i in range(1, n - 2):
                if y[j * n + i] + y[j * n + i + 1] in exist_down:
                    res -= 1
                else:
                    break

    return res
