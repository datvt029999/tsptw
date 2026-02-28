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
    t = [list(map(int, f.readline().split())) for _ in range(n + 1)]
visited = [False] * (n + 1)
previous_point = 0
total_time = 0
previous_times = [0] * (n + 1)
print(f"Problem size             : {n}" if printed else n)

if printed:
    print("Solution                 :", end=" ")

for i in range(1, n + 1):
    best_deadline = float("inf")
    best_distance = float("inf")

    for j in range(1, n + 1):
        if (
            not visited[j]
            and previous_times[i - 1] + t[previous_point][j] <= l[j]
            and (
                l[j] < best_deadline
                or (l[j] == best_deadline and t[previous_point][j] < best_distance)
            )
        ):
            best_point = j
            best_deadline = l[j]
            best_distance = t[previous_point][j]
    print(best_point, end=" ")
    visited[best_point] = True
    total_time += t[previous_point][best_point]
    previous_times[i] = (
        max(previous_times[i - 1] + t[previous_point][best_point], e[best_point])
        + d[best_point]
    )
    previous_point = best_point

if printed:
    print(
        f"\nTotal time               : {total_time + t[previous_point][0]}\nTime finishing delivering:",
        *previous_times[1:],
    )
