# Size of the problem (N)
size = 5

# Version of the input data (1 - 6)
version = 1

# Set to true to add additional text explaining the output, false otherwise
printed = True

if size not in [5, 10, 100, 200, 300, 500, 600, 700, 900, 1000]:
    raise ValueError(
        "Invalid problem size. Please choose from the following: 5, 10, 100, 200, 300, 500, 600, 700, 900, 1000"
    )
elif version < 1 or version > 6:
    raise ValueError("Invalid input version. Please choose a version from 1 to 6.")

with open(f"../../input/{size}/{version}.txt", "r") as f:
    n = int(f.readline().strip())
    e = [0] * (n + 1)
    l = [0] * (n + 1)
    d = [0] * (n + 1)

    for i in range(1, n + 1):
        e[i], l[i], d[i] = map(int, f.readline().split())
    t = []

    for i in range(n + 1):
        t.append(list(map(int, f.readline().split())))
visited = [False] * (n + 1)
previous_point = 0
total_time = 0
previous_times = [0] * (n + 1)

if printed:
    print(
        f"Size   : {size}\nVersion: {version}\n    Number of customers      : ", end=""
    )
print(n)

if printed:
    print("    Solution                 :", end=" ")

for i in range(1, n + 1):
    best_point = -1
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
    print()
    print(
        f"    Time                     : {total_time}\n    Time finishing delivering:",
        end="",
    )
    for i in range(1, n + 1):
        print(f" {previous_times[i]}", end="")
print()
