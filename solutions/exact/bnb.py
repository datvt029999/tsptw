from sys import argv

# Set to true to add additional text explaining the output, false otherwise
printed = True

with open(f"../../input/{int(argv[1])}.txt", "r") as f:
    n = int(f.readline().strip())
    e = [0] * (n + 1)
    l = [0] * (n + 1)
    d = [0] * (n + 1)

    for i in range(1, n + 1):
        e[i], l[i], d[i] = map(int, f.readline().split())
    t = []
    min_time = float("inf")

    for i in range(n + 1):
        row = list(map(int, f.readline().split()))
        t.append(row)

        for j in range(n + 1):
            if i != j:
                min_time = min(min_time, row[j])
visited = [False] * (n + 1)
s = [0] * (n + 1)
best_s = [0] * (n + 1)
times = [0] * (n + 1)
best_times = [0] * (n + 1)
current_time = 0
best_time = float("inf")


def generate_routes(k):
    global current_time, best_time

    for i in range(1, n + 1):
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

                    for j in range(1, n + 1):
                        best_s[j] = s[j]
                        best_times[j] = times[j]
            elif current_time + (n - k) * min_time < best_time:
                generate_routes(k + 1)
            visited[i] = False
            current_time -= t[s[k - 1]][i]


s[0] = 0
times[0] = 0
generate_routes(1)
print(f"Problem size             : {n}" if printed else n)

if printed:
    print("Best solution            :", end=" ")
print(*best_s[1:])

if printed:
    print(
        f"Best total time          : {best_time}\nTime finishing delivering:",
        *best_times[1:],
    )
