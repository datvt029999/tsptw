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
min_time = float("inf")

for i in range(nodes):
    for j in range(nodes):
        if i != j:
            min_time = min(min_time, t[i][j])

if read_from_file:
    sys.stdin.close()
visited = [False] * nodes
s = [0] * nodes
best_s = [0] * nodes
arrivals = [0] * nodes
best_arrivals = [0] * nodes
current_time = 0
best_time = float("inf")


def generate_routes(k):
    global current_time, best_time
    time_finishing_delivering = arrivals[k - 1] + d[s[k - 1]]

    for i in range(1, nodes):
        if not visited[i]:
            arrivals[k] = max(time_finishing_delivering + t[s[k - 1]][i], e[i])

            if arrivals[k] > l[i]:
                continue
            s[k] = i
            visited[i] = True
            current_time += t[s[k - 1]][i]

            if k == n:
                total_time = current_time + t[s[k]][0]

                if total_time < best_time:
                    best_time = total_time

                    for j in range(1, nodes):
                        best_s[j] = s[j]
                        best_arrivals[j] = arrivals[j]
            elif current_time + (n - k + 1) * min_time < best_time:
                generate_routes(k + 1)
            visited[i] = False
            current_time -= t[s[k - 1]][i]


generate_routes(1)

if printed:
    print("Problem size   :", end=" ")
print(n)

if printed:
    print("Best solution  :", end=" ")
print(*best_s[1:])

if printed:
    print(f"Best total time: {best_time}\nArrivals       :", *best_arrivals[1:], end="")
print()
