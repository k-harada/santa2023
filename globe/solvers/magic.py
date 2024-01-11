import numpy as np
from puzzle import Puzzle


def magic_swap1(c, k, n):
    # index c（0-base）を中心に上下ともに距離kを置換する魔法（cは動かない）
    assert 0 < k < n
    c_ = (c + 1) % (2 * n)
    k_ = -(k - c - 1) % (2 * n)
    sol = ["-r0"] + [f"f{c_}"] + ["r0", "-r1"] + [f"f{k_}", "-r0", "r1", f"f{k_}"] + [f"f{c_}"] + ["r0"]
    return sol


def magic_swap2(c, k, n):
    # index c（0-base）を右、その前を左とする中心線で距離kを上下とも置換する魔法（cは動かない）
    assert 0 <= k < n
    c_ = (c + n) % (2 * n)
    k_ = (k + c + 1) % (2 * n)
    sol = [f"f{c_}", "-r0"] + [f"f{k_}", "r0", "-r1", f"f{k_}"] + ["r1"] + [f"f{c_}"]
    return sol


def magic_updown1(c, k, n):
    # 下段からc番目を上に上げて上段のc- 1番目を下に落とす魔法
    # 長さ3, 連続したら追加は1
    c_ = (c + n) % (2 * n)
    sol = [f"f{c_}"] + ["r1"] + [f"f{c_}"]
    return sol


def magic_updown2(c, k, n):
    # cとc+nで上下を入れ替える魔法
    # 4点が180度回転する
    # 長さ6
    c_ = (c + 1) % n
    sol = ["-r0", f"f{c_}", "r0", "-r1", f"f{c_}", "r1"]
    return sol


def magic_updown3(c, k, n):
    assert 0 < k <= n
    # cとc-kで上下を入れ替える魔法
    # 長い
    c_ = (c - n) % (2 * n)
    k_ = (n - k) % (2 * n)
    sol = ["-r1"] * (k - 1) + \
          [f"f{c_}"] + ["-r1"] * k_ + ['r0', '-r1'] + [f"f{c_}", '-r0', 'r1', f"f{c_}"] + ["r1"] * k_ + [f"f{c_}"] + \
          ["r1"] * (k - 1)
    return sol


if __name__ == "__main__":
    _n = 8

    _c = 4
    _k = 2
    _p = Puzzle(9999, "globe_1/8",
                [str(100 + _i)[1:] for _i in range(32)],
                [str(100 + _i)[1:] for _i in range(32)], 0
                )
    _sol = magic_swap1(_c, _k, _n)
    for _m in _sol:
        _p.operate(_m)
    print(_c, _k)
    print(_p.state[:2 * _n])
    print(_p.state[2 * _n:])

    _c = 3
    _k = 1
    _p = Puzzle(9999, "globe_1/8",
                [str(100 + _i)[1:] for _i in range(32)],
                [str(100 + _i)[1:] for _i in range(32)], 0
                )
    _sol = magic_swap2(_c, _k, _n)
    for _m in _sol:
        _p.operate(_m)
    print(_c, _k)
    print(_p.state[:2 * _n])
    print(_p.state[2 * _n:])

    for _c in range(2 * _n):

        _p = Puzzle(9999, "globe_1/8",
                    [str(100 + _i)[1:] for _i in range(32)],
                    [str(100 + _i)[1:] for _i in range(32)], 0
                    )
        _sol = magic_updown1(_c, _k, _n)
        for _m in _sol:
            _p.operate(_m)
        print(_c)
        print(_p.state[:2 * _n])
        print(_p.state[2 * _n:])

    _c = 5
    _p = Puzzle(9999, "globe_1/8",
                [str(100 + _i)[1:] for _i in range(32)],
                [str(100 + _i)[1:] for _i in range(32)], 0
                )
    _sol = magic_updown2(_c, 0, _n)
    for _m in _sol:
        _p.operate(_m)
    print(_c)
    print(_p.state[:2 * _n])
    print(_p.state[2 * _n:])

    _c = 6
    _k = 2

    _p = Puzzle(9999, "globe_1/8",
                [str(100 + _i)[1:] for _i in range(32)],
                [str(100 + _i)[1:] for _i in range(32)], 0
                )
    _sol = magic_updown3(_c, _k, _n)
    for _m in _sol:
        _p.operate(_m)
    print(_c, _k)
    print(_p.state[:2 * _n])
    print(_p.state[2 * _n:])
