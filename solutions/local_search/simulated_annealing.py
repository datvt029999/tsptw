import random
import sys

from math import exp
from time import time

# Set to true to read input from a file, false otherwise
read_from_file = True

# Set to true to add additional text explaining the output, false otherwise
printed = True


def get_statistics(route, earliest, latests, durations, times):
    total_time = 0
    arrival = 0
    previous_point = 0
    violations = 0

    for point in route:
        arrival = (
            max(arrival, earliest[previous_point])
            + durations[previous_point]
            + times[previous_point][point]
        )
        violations += max(arrival - latests[point], 0)
        total_time += times[previous_point][point]
        previous_point = point
    return total_time + times[previous_point][0], violations


def get_score(total_time, violations):
    return total_time + violations * 10000


def swap(route, i, j):
    s = route[:]
    s[i], s[j] = s[j], s[i]
    return s


def relocate(route, i, j):
    s = route[:]
    s.insert(j, s.pop(i))
    return s


def two_opt_move(route, i, j):
    s = route[:]

    if i > j:
        i, j = j, i
    s[i : j + 1] = reversed(s[i : j + 1])
    return s


def random_neighbour(route, nodes, moves, move_index):
    if moves[move_index] == "Swap":
        i = random.randrange(nodes - 1)
        return swap(route, i, random.randrange(i + 1, nodes))
    elif moves[move_index] == "Relocate":
        i = random.randrange(nodes)
        return relocate(
            route, i, random.choice([point for point in range(nodes) if point != i])
        )
    i = random.randrange(nodes - 2)
    return two_opt_move(route, i, random.randrange(i + 2, nodes))


def main():
    if read_from_file:
        sys.stdin = open(f"../../input/{sys.argv[1]}.txt")
    n = int(input().strip())
    points = n + 1
    e = [0] * points
    l = [0] * points
    d = [0] * points

    for i in range(1, points):
        e[i], l[i], d[i] = map(int, input().split())
    t = [list(map(int, input().split())) for _ in range(points)]

    if read_from_file:
        sys.stdin.close()
    starting_time = time()
    best_overall_score = float("inf")
    best_overall_time = float("inf")
    strategies = ["Earlier e", "Earlier l"]
    iterations = [0] * len(strategies)
    runtimes = [0] * len(strategies)
    operators = ["Swap", "Relocate", "2-opt move"]
    operators_count = [[0] * len(operators) for _ in range(len(strategies))]

    # Parameters
    t_init = 10000000
    t_end = 1
    alpha = 0.99995

    if printed:
        print(
            f"Parameters           : t_init = {t_init}, t_end = {t_end}, alpha =", alpha
        )

    for index, strategy in enumerate(strategies):
        starting_strategy_time = time()
        temperature = t_init

        # Initialize solution
        s = sorted(
            range(1, points),
            key=lambda point: e[point] if strategy == "Earlier e" else l[point],
        )

        if printed:
            print(f"Initializing strategy:", strategy)

        # Simulated annealing
        best_time, best_violations = get_statistics(s, e, l, d, t)
        best_score = get_score(best_time, best_violations)
        current_s = s[:]
        current_time = best_time
        current_violations = best_violations
        current_score = best_score
        iterations[index] = 0

        while temperature > t_end:
            iterations[index] += 1
            print(f"    Iteration {iterations[index]:<6d}:")
            random.shuffle(operators)

            # Select a neighbour randomly and evaluate it
            operator_index = random.randrange(len(operators))
            new_s = random_neighbour(current_s, n, operators, operator_index)
            new_time, new_violations = get_statistics(new_s, e, l, d, t)
            new_score = get_score(new_time, new_violations)
            delta = new_score - current_score

            if delta < 0:
                print(
                    f"        delta = {delta}\n        => delta < 0\n        => Accept better solution"
                )
                current_s = new_s[:]
                current_score = new_score
                current_time = new_time
                current_violations = new_violations
                operators_count[index][operator_index] += 1
            else:
                print(
                    f"        delta                  = {delta}\n        => delta >= 0\n        temperature            =",
                    temperature,
                )
                value = -delta / temperature
                print("        -delta/temperature     =", value)
                result = exp(value)
                print("        e^(-delta/temperature) =", result)
                u = random.random()
                print("        u                      =", u)

                if result > u:
                    print(
                        "        => e^(-delta/temperature) > u\n        => Accept worse solution"
                    )
                    current_s = new_s[:]
                    current_score = new_score
                    current_time = new_time
                    current_violations = new_violations
                    operators_count[index][operator_index] += 1
                else:
                    print(
                        "        => e^(-delta/temperature) <= u\n        => Reject worse solution"
                    )

            if current_score < best_score:
                s = current_s[:]
                best_score = current_score
                best_time = current_time
                best_violations = current_violations
            temperature *= alpha
            runtimes[index] = time() - starting_strategy_time

            if printed:
                print(
                    f"        Current: {current_time}, {current_violations} violations, {operators[operator_index].lower()}\n        Best: {best_time}, {best_violations} violations, {runtimes[index]:.3f}s"
                )

        if best_score < best_overall_score:
            best_s = s[:]
            best_overall_score = best_score
            best_overall_time = best_time
    ending_time = time()

    if printed:
        print("Problem size         :", end=" ")
    print(n)

    if printed:
        print("Best solution        :", end=" ")
    print(*best_s)

    if printed:
        arrivals = []
        current_time = 0
        previous_point = 0

        for point in best_s:
            arrival = max(current_time + t[previous_point][point], e[point])
            arrivals.append(arrival)
            current_time = arrival + d[point]
            previous_point = point
        print(
            f"Best total time      : {best_overall_time}\nArrivals             :",
            *arrivals,
            f"\nRuntime              : {ending_time - starting_time:.3f}s\nIterations           :",
        )
        strategy_longest_name = max(len(strategy) for strategy in strategies)

        for index, strategy in enumerate(strategies):
            print(
                f"    {strategy:<{strategy_longest_name}}: {iterations[index]}, {runtimes[index]:.3f}s"
            )
        print("Operators' statistics:")

        for index, strategy in enumerate(strategies):
            print(f"    {strategy:<{strategy_longest_name}}:")

            for operator_index, operator in enumerate(operators):
                print(f"        {operator}:", operators_count[index][operator_index])


if __name__ == "__main__":
    main()
