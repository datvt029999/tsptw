import sys

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
s = []
visited = [False] * nodes
previous_point = 0
total_time = 0
arrivals = [0] * nodes
feasible = True

for i in range(1, nodes):
    best_point = 0
    best_deadline = float("inf")
    best_distance = float("inf")
    arrivals[-1] = arrivals[i - 1] + d[previous_point]

    for j in range(1, nodes):
        if (
            not visited[j]
            and arrivals[-1] + t[previous_point][j] <= l[j]
            and (
                e[j] < best_deadline
                or (e[j] == best_deadline and t[previous_point][j] < best_distance)
            )
        ):
            best_point = j
            best_deadline = e[j]
            best_distance = t[previous_point][j]

    if best_point < 1:
        feasible = False
        print("The greedy heuristic based on smaller e[i] gives infeasible solution.")
        break
    s.append(best_point)
    visited[best_point] = True
    total_time += t[previous_point][best_point]
    arrivals[i] = max(arrivals[-1] + t[previous_point][best_point], e[best_point])
    previous_point = best_point

if feasible:
    if printed:
        print(f"Problem size:", end=" ")
    print(n)

    if printed:
        print("Solution    :", end=" ")
    print(*s)

    if printed:
        print(
            f"Total time  : {total_time + t[previous_point][0]}\nArrivals    :",
            *arrivals[1:],
        )
