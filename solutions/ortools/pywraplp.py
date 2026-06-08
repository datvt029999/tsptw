import sys

from ortools.linear_solver.pywraplp import Solver

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
solver = Solver.CreateSolver("SCIP")

# x[i, j] = 1 if the salesman moves from city i to city j, 0 otherwise
x = {
    (i, j): solver.BoolVar(f"x_{i}_{j}")
    for i in range(nodes)
    for j in range(nodes)
    if i != j
}

# Time to visit customer i
arrivals = [solver.IntVar(e[i], l[i], f"arrivals_{i}") for i in range(nodes)]

for i in range(nodes):
    # Each customer is visited exactly once
    solver.Add(sum(x[i, j] for j in range(nodes) if j != i) == 1)
    solver.Add(sum(x[j, i] for j in range(nodes) if j != i) == 1)

    # Time window constraints if the salesman moves from customer i to customer j (arrivals[j] >= arrivals[i] + d[i] + t[i][j] if x[i, j] = 1)
    for j in range(1, nodes):
        if i != j:
            solver.Add(
                arrivals[j] >= arrivals[i] + d[i] + t[i][j] - 1000000 * (1 - x[i, j])
            )
solver.Minimize(
    sum(t[i][j] * x[i, j] for i in range(nodes) for j in range(nodes) if j != i)
)

if printed:
    solver.EnableOutput()
solver.SetTimeLimit(600000)

if solver.Solve() in [Solver.OPTIMAL, Solver.FEASIBLE]:
    if printed:
        print("Problem size       :", end=" ")
    print(n)

    if printed:
        print("Best solution      :", end=" ")
    solution = sorted(
        {i: arrivals[i].solution_value() for i in range(1, nodes)}.items(),
        key=lambda node: node[1],
    )

    for i in range(n):
        print(solution[i][0], end=" ")

    if printed:
        print(
            f"\nBest total time    : {round(solver.Objective().Value())}\nArrivals           :",
            end=" ",
        )

        for i in range(n):
            print(round(solution[i][1]), end=" ")
        print(f"\nRuntime            : {solver.WallTime() / 1000:.3f}s", end="")
    print()
else:
    print("No solution found in the given time limit.")
