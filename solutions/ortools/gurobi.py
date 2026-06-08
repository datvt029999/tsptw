import sys

from gurobipy import GRB, Model

# Set to true to read input from a file, false otherwise
read_from_file = True

# Set to true to add additional text explaining the output, false otherwise
printed = True

if read_from_file:
    sys.stdin = open(f"../../input/{sys.argv[1]}.txt")
n = int(input().strip())
nodes = n + 1
e = [0] * nodes
l = [0] * nodes
d = [0] * nodes

for i in range(1, nodes):
    e[i], l[i], d[i] = map(int, input().split())
t = [list(map(int, input().split())) for _ in range(nodes)]

if read_from_file:
    sys.stdin.close()
model = Model()

# x[i, j] = 1 if the salesman moves from city i to city j, 0 otherwise
x = model.addVars(
    ((i, j) for i in range(nodes) for j in range(nodes) if i != j), vtype=GRB.BINARY
)

# Time to visit customer i
arrivals = [model.addVar(lb=e[i], ub=l[i], vtype=GRB.CONTINUOUS) for i in range(nodes)]

for i in range(nodes):
    # Each customer is visited exactly once
    model.addConstr(sum(x[i, j] for j in range(nodes) if j != i) == 1)
    model.addConstr(sum(x[j, i] for j in range(nodes) if j != i) == 1)

    for j in range(1, nodes):
        if i != j:
            model.addGenConstrIndicator(
                x[i, j], True, arrivals[j] >= arrivals[i] + d[i] + t[i][j]
            )
model.setObjective(
    sum(t[i][j] * x[i, j] for i in range(nodes) for j in range(nodes) if i != j),
    GRB.MINIMIZE,
)
model.Params.TimeLimit = 600
model.Params.OutputFlag = 1 if printed else 0
model.update()
model.optimize()

if model.Status == GRB.OPTIMAL or model.SolCount > 0:
    if printed:
        print("Problem size       :", end=" ")
    print(n)

    if printed:
        print("Best solution      :", end=" ")
    solution = sorted([(i, arrivals[i].X) for i in range(1, nodes)], key=lambda x: x[1])

    for i in range(n):
        print(solution[i][0], end=" ")

    if printed:
        print(
            f"\nBest total time    : {round(model.getObjective().getValue())}\nArrivals           :",
            end=" ",
        )

        for i in range(n):
            print(round(solution[i][1]), end=" ")
        print(f"\nRuntime            : {model.Runtime:.3f}s", end="")
    print()
else:
    print("No solution found in the given time limit.\nBest bound:", model.ObjBound)
