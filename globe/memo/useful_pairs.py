import numpy as np
from globe.solvers.solve_1xn_greed import GreedySolver
from puzzle import Puzzle


# [[0, 1, 2, 7], [4, 5, 6, 3]],
# 9-6-1
# 9-1-6
# to
# 9-1-6
# 9-6-1

# ['-r0', '-r0', 'f2', '-r0', 'f2', 'r0', 'f2', 'r1', 'f2', 'r0', 'f2', '-r0', 'f2', '-r1', 'r0']


# [[0, 1, 2, 3], [4, 5, 7, 6]],
# 10-1-5
# 8-1-7
# to
# 10-5-1
# 8-7-1
# ['-r0', 'f2', '-r1', 'f2', '-r0', 'f2', 'r0', 'f2', 'r0', 'r1', 'f2', 'r0', 'f2']

# [[0, 1, 3, 2], [4, 5, 7, 6]]
# ['-r0', '-r1', 'f2', 'r0', 'f2', '-r0', 'r1', 'f2', '-r1', 'f2', 'r0', 'r1']
# 上下ともにラスト２個を互換する

# [[0, 1, 2, 3], [4, 6, 7, 5]]
# ['f2', '-r0', '-r1', 'f2', 'r1', 'f2', 'r0', 'f2', '-r0', 'f2', 'r0', 'f2']
# 片方の隣接３つを巡回

# ['f4', '-r0', '-r1', 'f4', 'r1', 'f4', '-r0', '-r1', 'f4', 'r1', 'f4', 'r0'
# , 'f4', '-r0', 'f4', 'r0', 'r0', 'f4', '-r0', 'f4', 'r0', 'f4']
# ５つで巡回

# ['-r0', 'f4', '-r1', 'f4', 'r1', 'f4', 'r0', 'r1', 'f4', 'r1', 'f4', 'r1', 'r0', 'f4', 'r1', 'f4', '-r1', 'f4', '-r0', 'f4', '-r1', '-r1', 'f4']
# ３つジャンプ + 謎の置換

# "0", "1", "2", "3", "4", "5", "7", "F",
# "8", "9", "A", "B", "C", "D", "6", "E"
# ['-r0', '-r1', 'f4', '-r1', '-r1', 'f4', '-r1', 'r0', 'f4', 'r1', 'f4', 'r1', '-r0', 'f4', 'r0', 'f4', '-r0', 'r1', 'f4', 'r0', 'f4', 'r1', 'r1']
# 10 - 5 - 1

# "0", "1", "2", "3", "4", "5", "F", "E",
# "8", "9", "A", "B", "C", "D", "7", "6"
# ['r1', 'f4', '-r1', '-r1', 'f4', '-r0', 'f4', 'r0', 'f4', 'r1', '-r0', 'r1', 'f4', '-r1', 'f4', 'r0', 'f4']
# n - 2を回す

# ['-r1', '-r1', '-r1', '-r1', 'f4', 'r1', 'f4', 'r1', 'r1', 'r1', 'r1']
# 8-7-1

# "0", "1", "2", "B", "4", "5", "6", "F",
# "8", "9", "A", "3", "C", "D", "E", "7"
# ['r0', 'r0', 'r0', 'f4', 'r0', '-r1', 'f4', 'r1', 'r0', 'r0', 'r0', 'r0']
# 2か所同時上下入れ替え

# 上下２箇所を隣同士を互換
# ['f4', '-r0', 'f4', 'r0', '-r1', 'f4', 'r1', 'f4']
# ['-r0', 'f4', 'r1', 'r1', 'f4', '-r1', '-r1', 'f4', 'r0', 'f4', 'r1', 'r1', 'f4', '-r1', '-r1', '-r0', 'f4', 'r0']


# 上下同時に123-321
# "0", "1", "2", "5", "4", "3", "6", "7",
# "8", "9", "C", "B", "A", "D", "E", "F"
# ['f4', '-r0', '-r1', 'f4', 'r0', '-r1', 'f4', 'r1', 'r1', 'f4']

# 上下同時に1234-4231
# "0", "1", "2", "6", "4", "5", "3", "7",
# "8", "C", "A", "B", "9", "D", "E", "F"
# ['f4', '-r0', '-r1', '-r1', 'f4', 'r0', '-r1', 'f4', 'r1', 'r1', 'r1', 'f4']


if __name__ == "__main__":
    solver = GreedySolver(4)
    solver.initialize([
          "0", "1", "2", "3", "4", "5", "6", "7",
          "8", "9", "A", "B", "C", "D", "E", "F"
        ], [
          "0", "1", "2", "3", "4", "5", "6", "7",
          "8", "9", "A", "B", "C", "D", "E", "F"
        ], force_pair=True
    )
    solver.solve()
    print(solver.path)

    # 大きすぎて無理
    # solver = GreedySolver(6)
    # solver.initialize([
    #         "0", "1", "2", "5", "4", "3", "6", "7", "G", "H", "K", "L",
    #         "8", "9", "C", "B", "A", "D", "E", "F", "I", "J", "M", "N"
    #     ], [
    #         "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B",
    #         "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"
    #     ]
    # )
    # solver.solve()
    # print(solver.path)

    k = 0
    _sol = ['f0', '-r0'] + ['-r1'] * k + ['f1', 'r0', '-r1', 'f1'] + ['r1'] * (k + 1) + ['f0']
    # 0とkを入れ替える魔法
    # _sol = ['f0', 'r0', '-r1'] + ['-r1'] * k + ['f1', '-r0', 'r1', 'f1'] + ['r1'] * k + ['f0']
    # 0とn-kで上下を入れ替える魔法

    # _sol = ['f4'] + ['-r1'] * k + ['f4']
    # _sol = ['f0', 'r0', '-r1', 'f0', '-r0']  # 0とnで上下を入れ替える魔法
    # _sol = ['f0', 'r0', '-r1'] + ['f5', '-r0', 'r1', 'f5'] + ['f0']
    # 上下それぞれで互換する魔法

    _p = Puzzle(9999, "globe_3/33",
                [str(_i) for _i in range(66*4)],
                [str(_i) for _i in range(66*4)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f33")
        elif _m == "r1":
            _p.operate("r3")
        elif _m == "-r1":
            _p.operate("-r3")
        else:
            _p.operate(_m)
    print("f33", _p)
    print("f33", [str(_i) for _i in range(66*4)])

    _p = Puzzle(9999, "globe_1/8",
                [str(_i) for _i in range(32)],
                [str(_i) for _i in range(32)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f8")
        else:
            _p.operate(_m)
    print("f8", _p)

    _p = Puzzle(9999, "globe_1/8",
                [str(_i) for _i in range(32)],
                [str(_i) for _i in range(32)], 0
                )
    for _m in _sol:
        _p.operate(_m)
    print("asis", _p)

    _p = Puzzle(9999, "globe_1/8",
                [str(_i) for _i in range(32)],
                [str(_i) for _i in range(32)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f2")
        else:
            _p.operate(_m)
    print("f2", _p)

    _p = Puzzle(9999, "globe_1/8",
                [str(_i) for _i in range(32)],
                [str(_i) for _i in range(32)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f0")
        else:
            _p.operate(_m)
    print("f0", _p)

    _p = Puzzle(9999, "globe_1/8",
                [str(_i) for _i in range(32)],
                [str(_i) for _i in range(32)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f4")
        else:
            _p.operate(_m)
    print("f4", _p)

    _p = Puzzle(9999, "globe_1/16",
                [str(_i) for _i in range(64)],
                [str(_i) for _i in range(64)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f16")
        else:
            _p.operate(_m)
    print(_p)
    _p = Puzzle(9999, "globe_1/16",
                [str(_i) for _i in range(64)],
                [str(_i) for _i in range(64)], 0
                )
    for _m in _sol:
        if _m[0] == "f":
            _p.operate("f2")
        else:
            _p.operate(_m)
    print(_p)
