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
l = [0] * nodes
d = [0] * nodes

for i in range(1, nodes):
    e[i], l[i], d[i] = map(int, input().split())
t = []
min_time = float("inf")

for i in range(nodes):
    row = list(map(int, input().split()))
    t.append(row)

    for j in range(nodes):
        if i != j:
            min_time = min(min_time, row[j])

if read_from_file:
    sys.stdin.close()
visited = [False] * nodes
s = [0] * nodes
best_s = [0] * nodes
times = [0] * nodes
best_times = [0] * nodes
current_time = 0
best_time = float("inf")


def generate_routes(k):
    global current_time, best_time

    for i in range(1, nodes):
        if not visited[i]:
            arrival = max(times[k - 1] + t[s[k - 1]][i], e[i])

            if arrival > l[i]:
                continue
            s[k] = i
            visited[i] = True
            current_time += t[s[k - 1]][i]
            times[k] = arrival + d[i]

            if k == n:
                total_time = current_time + t[s[k]][0]

                if total_time < best_time:
                    best_time = total_time

                    for j in range(1, nodes):
                        best_s[j] = s[j]
                        best_times[j] = times[j]
            elif current_time + (n - k) * min_time < best_time:
                generate_routes(k + 1)
            visited[i] = False
            current_time -= t[s[k - 1]][i]


s[0] = 0
times[0] = 0
generate_routes(1)

if printed:
    print("Problem size             :", end=" ")
print(n)

if printed:
    print("Best solution            :", end=" ")
print(*best_s[1:])

if printed:
    print(
        f"Best total time          : {best_time}\nTime finishing delivering:",
        *best_times[1:],
    )
