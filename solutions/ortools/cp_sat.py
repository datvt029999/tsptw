from ortools.sat.python import cp_model

# Set to true to read input from a file, false otherwise
read_from_file = True

# Set to true to add additional text explaining the output, false otherwise
printed = True

if read_from_file:
    import sys

    sys.stdin = open(f"../../input/{int(sys.argv[1])}.txt")
n = int(input().strip())
nodes = n + 1
e = [0] * nodes
l = [1000000000] * nodes
d = [0] * nodes

for i in range(1, nodes):
    e[i], l[i], d[i] = map(int, input().split())
t = [list(map(int, input().split())) for _ in range(nodes)]

if read_from_file:
    sys.stdin.close()
model = cp_model.CpModel()

# x[i, j] = 1 if the salesman moves from city i to city j, 0 otherwise
x = {}

# Time to travel from city i to city j, including the service time at city i
travelling_times = {}

for i in range(nodes):
    for j in range(nodes):
        x[i, j] = model.NewBoolVar(f"x_{i}_{j}")
        travelling_times[i, j] = d[i] + t[i][j]

# Each city is visited exactly once
for i in range(nodes):
    model.Add(sum(x[i, j] for j in range(nodes) if j != i) == 1)
    model.Add(sum(x[j, i] for j in range(nodes) if j != i) == 1)

# Time to visit city i
visiting_times = [model.NewIntVar(0, 0, "visiting_times_0")] + [
    model.NewIntVar(e[i], l[i], f"visiting_times_{i}") for i in range(1, nodes)
]

# Waiting times at city i
waiting_times = [
    model.NewIntVar(0, l[i] - e[i], f"waiting_times_{i}") for i in range(nodes)
]

# Time window constraints if the salesman moves from city i to city j (x[i, j] = 1)
for i in range(nodes):
    for j in range(1, nodes):
        if i != j:
            # visiting_times[j] >= visiting_times[i] + travelling_times[i, j]
            model.Add(
                visiting_times[j] >= visiting_times[i] + travelling_times[i, j]
            ).OnlyEnforceIf(x[i, j])

            # The waiting time at city j is equal to the time to visit city j minus the time to visit city i minus the time to travel from city i to city j
            model.Add(
                waiting_times[j]
                == visiting_times[j] - visiting_times[i] - travelling_times[i, j]
            ).OnlyEnforceIf(x[i, j])

model.Minimize(
    sum(t[i][j] * x[i, j] for i in range(nodes) for j in range(nodes) if j != i)
)
solver = cp_model.CpSolver()
solver.Solve(model)

if printed:
    print("Problem size             :", end=" ")
print(n)

if printed:
    print("Best solution            :", end=" ")
solution = sorted(
    {i: solver.Value(visiting_times[i]) + d[i] for i in range(1, nodes)}.items(),
    key=lambda node: node[1],
)

for i in range(n):
    print(solution[i][0], end=" ")

if printed:
    print(
        f"\nBest total time          : {int(solver.ObjectiveValue())}\nTime finishing delivering:",
        end=" ",
    )

    for i in range(n):
        print(solution[i][1], end=" ")
print()
