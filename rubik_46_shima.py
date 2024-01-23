from puzzle import Puzzle

# 詠唱失敗

magic_444 = ["-d0", "-d2"] + ["-r0", "-r3"] + ["f0", "f2"] + ["r0", "r0"] + ["-f0", "-f2"] + ["r0", "r0"] + ["f0", "f2"]


if __name__ == "__main__":

    initial_4 = "A;A;A;A;A;A;A;A;A;A;A;A;A;A;A;A;B;B;B;B;B;B;B;B;B;B;B;B;B;B;B;B;C;C;C;C;C;C;C;C;C;C;C;C;C;C;C;C;D;D;D;D;D;D;D;D;D;D;D;D;D;D;D;D;E;E;E;E;E;E;E;E;E;E;E;E;E;E;E;E;F;F;F;F;F;F;F;F;F;F;F;F;F;F;F;F"
    goal_4 = "A;B;A;B;A;B;A;B;A;B;A;B;A;B;A;B;B;C;B;C;B;C;B;C;B;C;B;C;B;C;B;C;C;D;C;D;C;D;C;D;C;D;C;D;C;D;C;D;D;E;D;E;D;E;D;E;D;E;D;E;D;E;D;E;E;F;E;F;E;F;E;F;E;F;E;F;E;F;E;F;F;A;F;A;F;A;F;A;F;A;F;A;F;A;F;A"
    p4 = Puzzle(
        puzzle_id=444444, puzzle_type=f"cube_4/4/4",
        solution_state=list(goal_4.split(";")),
        initial_state=list(initial_4.split(";")),
        num_wildcards=0
    )

    for m in magic_444:
        p4.operate(m)
    print(p4)

