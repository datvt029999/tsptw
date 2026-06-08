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
masks = 1 << n
best_total_times = [[1000000] * nodes for _ in range(masks)]
best_arrivals = [[0] * nodes for _ in range(masks)]
previous_points = [[0] * nodes for _ in range(masks)]

for i in range(1, nodes):
    arrival = max(t[0][i], e[i])

    if arrival <= l[i]:
        mask = 1 << (i - 1)
        best_total_times[mask][i] = t[0][i]
        best_arrivals[mask][i] = arrival
        previous_points[mask][i] = 0

for mask in range(masks):
    for current_point in range(1, nodes):
        if best_total_times[mask][current_point] < 1000000:
            time_finishing_delivering = (
                best_arrivals[mask][current_point] + d[current_point]
            )

            for point in range(1, nodes):
                if mask & (1 << (point - 1)):
                    continue
                arrival = max(
                    time_finishing_delivering + t[current_point][point], e[point]
                )

                if arrival > l[point]:
                    continue
                new_mask = mask | (1 << (point - 1))
                total_time = (
                    best_total_times[mask][current_point] + t[current_point][point]
                )

                if total_time < best_total_times[new_mask][point]:
                    best_total_times[new_mask][point] = total_time
                    best_arrivals[new_mask][point] = arrival
                    previous_points[new_mask][point] = current_point
                elif (
                    total_time == best_total_times[new_mask][point]
                    and arrival < best_arrivals[new_mask][point]
                ):
                    best_arrivals[new_mask][point] = arrival
                    previous_points[new_mask][point] = current_point
mask = masks - 1
best_time = 1000000

for current_point in range(1, nodes):
    if best_total_times[mask][current_point] < 1000000:
        total = best_total_times[mask][current_point] + t[current_point][0]

        if total < best_time:
            best_time = total
            last_point = current_point
s = []

while last_point > 0:
    s.append(last_point)
    prev = previous_points[mask][last_point]
    mask ^= 1 << (last_point - 1)
    last_point = prev
s.reverse()

if printed:
    print("Problem size   :", end=" ")
print(n)

if printed:
    print("Best solution  :", end=" ")
print(*s)

if printed:
    arrivals = []
    arrival = 0
    previous_point = 0

    for point in s:
        arrival = max(arrival + d[previous_point] + t[previous_point][point], e[point])
        arrivals.append(arrival)
        previous_point = point
    print(f"Best total time: {best_time}\nArrivals       :", *arrivals)
