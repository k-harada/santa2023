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

# ['f4', '-r0', '-r1', 'f4', 'r1', 'f4', '-r0', '-r1', 'f4', 'r1', 'f4', 'r0', 'f4', '-r0', 'f4', 'r0', 'r0', 'f4', '-r0', 'f4', 'r0', 'f4']
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

