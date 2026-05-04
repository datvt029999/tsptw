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
t = [list(map(int, input().split())) for _ in range(nodes)]

if read_from_file:
    sys.stdin.close()
visited = [False] * nodes
previous_point = 0
total_time = 0
previous_times = [0] * nodes
print(f"Problem size             : {n}" if printed else n)

if printed:
    print("Solution                 :", end=" ")

for i in range(1, nodes):
    best_deadline = float("inf")
    best_distance = float("inf")

    for j in range(1, nodes):
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
