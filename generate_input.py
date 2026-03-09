import sys

from random import randint, shuffle

sys.stdout = open(f"input/{int(sys.argv[2])}.txt", "w")

# Size of the problem
n = int(sys.argv[1])

# Create a feasible route (random permutation of customers)
route = list(range(1, n + 1))
shuffle(route)

# Travel times
t = [[0] * (n + 1) for _ in range(n + 1)]

for i in range(n + 1):
    for j in range(n + 1):
        if i != j:
            t[i][j] = randint(5, 100)

# Delivery times
d = {i: randint(5, 20) for i in range(1, n + 1)}

# Calculate arrival times
arrival = {route[0]: t[0][route[0]]}
total_time = t[0][route[0]] + d[route[0]]

for i, customer in enumerate(route[1:]):
    total_time += t[route[i]][customer]
    arrival[customer] = total_time
    total_time += d[customer]

# Create time windows around arrival times
e = {}
l = {}

for i in range(1, n + 1):
    e[i] = max(0, arrival[i] - randint(0, 20))
    l[i] = arrival[i] + randint(30, 80)

# Write the data to the input file
print(n)

for i in range(1, n + 1):
    print(e[i], l[i], d[i])

for i in range(n + 1):
    print(*t[i])
