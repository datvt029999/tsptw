import sys

from ortools.sat.python import cp_model

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
model = cp_model.CpModel()

# next_customers[i] = j if the salesman moves from customer i to customer j
next_customers = [model.NewIntVar(0, n, f"next_customers_{i}") for i in range(nodes)]

# costs[i] = t[i][next_customers[i]]
costs = [model.NewIntVar(1, max(t[i]), f"costs_{i}") for i in range(nodes)]

# Time to visit customer i
arrivals = [model.NewIntVar(e[i], l[i], f"arrivals_{i}") for i in range(nodes)]

for i in range(nodes):
    for j in range(nodes):
        is_next_city = model.NewBoolVar(f"is_next_city_{i}_{j}")
        model.Add(next_customers[i] == j).OnlyEnforceIf(is_next_city)
        model.Add(next_customers[i] != j).OnlyEnforceIf(is_next_city.Not())
        model.Add(costs[i] == t[i][j]).OnlyEnforceIf(is_next_city)

        if j > 0:
            model.Add(arrivals[j] >= arrivals[i] + d[i] + t[i][j]).OnlyEnforceIf(
                is_next_city
            )
model.AddAllDifferent(next_customers)
model.Minimize(sum(costs))
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 600
solver.parameters.log_search_progress = printed

if solver.Solve(model) in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
    if printed:
        print("Problem size   :", end=" ")
    print(n)

    if printed:
        print("Best solution  :", end=" ")
    solution = sorted(
        {i: solver.Value(arrivals[i]) for i in range(1, nodes)}.items(),
        key=lambda node: node[1],
    )

    for i in range(n):
        print(solution[i][0], end=" ")

    if printed:
        print(
            f"\nBest total time: {round(solver.ObjectiveValue())}\nArrivals       :",
            end=" ",
        )

        for i in range(n):
            print(round(solution[i][1]), end=" ")
        print(f"\nRuntime        : {solver.WallTime():.3f}s", end="")
    print()
else:
    print("No solution found in the given time limit.")
