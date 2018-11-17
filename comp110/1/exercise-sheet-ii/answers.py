

def draw_truth_table_2(expression):
    for A in [False, True]:
        for B in [False, True]:
                print(A, "\t", B, "\t|", expression(A, B))

def draw_truth_table(expression):
    for A in [False, True]:
        for B in [False, True]:
            for C in [False, True]:
                print(A, "\t", B, "\t", C, "\t|", expression(A, B, C))

print("-"*40)
print("1a")
draw_truth_table(lambda A,B,C: A and B and not C)

print("-"*40)
print("1b")
draw_truth_table(lambda A,B,C: A and not (B and not C))

print("-"*40)
print("1c")
draw_truth_table(lambda A,B,C: (A or not B) and (A or C))

print("-"*40)
print("3a")
draw_truth_table_2(lambda A,B: not (A or B))

print("-"*40)
print("3b")
draw_truth_table_2(lambda A,B: not (A and B))

print("-"*40)
print("3c")
draw_truth_table(lambda A,B,C: (A and B) or (A and C))

print("-"*40)
print("3d")
draw_truth_table(lambda A,B,C: (A or B) and (A or C))

print("-"*40)
print("adrian")
draw_truth_table(lambda A,B,C: A and not (B or not C) and (not A and B))

