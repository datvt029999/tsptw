import sys

from random import shuffle
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
    return total_time + violations * 1000000


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
    best_s = []
    operators = ["Swap", "Relocate", "2-opt move"]
    operators_count = [[0] * len(operators) for _ in range(len(strategies))]

    for index, strategy in enumerate(strategies):
        starting_strategy_time = time()

        # Initialize solution
        s = sorted(
            range(1, points),
            key=lambda point: e[point] if strategy == "Earlier e" else l[point],
        )

        if printed:
            print(f"Initializing strategy:", strategy)

        # Hill climbing
        best_time, best_violations = get_statistics(s, e, l, d, t)
        best_score = get_score(best_time, best_violations)
        iterations[index] = 0

        while runtimes[index] < 1200:
            improved = False
            iterations[index] += 1
            shuffle(operators)

            # Select and evaluate a neighbour
            for operator in operators:
                if operator == "Swap":
                    indices = [(i, j) for i in range(n) for j in range(i + 1, n)]
                    shuffle(indices)

                    for i, j in indices:
                        new_s = swap(s, i, j)
                        new_time, new_violations = get_statistics(new_s, e, l, d, t)
                        new_score = get_score(new_time, new_violations)

                        if new_score < best_score:
                            s = new_s
                            best_score = new_score
                            best_time = new_time
                            best_violations = new_violations
                            improved = True
                            operators_count[index][0] += 1
                            operator_index = 0
                            break

                if improved:
                    break
                elif operator == "Relocate":
                    indices = [(i, j) for i in range(n) for j in range(n) if i != j]
                    shuffle(indices)

                    for i, j in indices:
                        new_s = relocate(s, i, j)
                        new_time, new_violations = get_statistics(new_s, e, l, d, t)
                        new_score = get_score(new_time, new_violations)

                        if new_score < best_score:
                            s = new_s
                            best_score = new_score
                            best_time = new_time
                            best_violations = new_violations
                            improved = True
                            operators_count[index][1] += 1
                            operator_index = 1
                            break

                if improved:
                    break
                elif operator == "2-opt move":
                    indices = [(i, j) for i in range(n - 2) for j in range(i + 2, n)]
                    shuffle(indices)

                    for i, j in indices:
                        new_s = two_opt_move(s, i, j)
                        new_time, new_violations = get_statistics(new_s, e, l, d, t)
                        new_score = get_score(new_time, new_violations)

                        if new_score < best_score:
                            s = new_s
                            best_score = new_score
                            best_time = new_time
                            best_violations = new_violations
                            improved = True
                            operators_count[index][2] += 1
                            operator_index = 2
                            break

            runtimes[index] = time() - starting_strategy_time

            if not improved:
                break
            elif printed:
                print(
                    f"    Iteration {iterations[index]:<4d}: {best_time}, {best_violations} violations, {runtimes[index]:.3f}s, {operators[operator_index].lower()}"
                )

        if best_score < best_overall_score:
            best_overall_score = best_score
            best_overall_time = best_time
            best_s = s[:]
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

        for index, strategy in enumerate(strategies):
            print(
                f"    {strategy:<{max(len(strategy) for strategy in strategies)}}: {iterations[index]}, {runtimes[index]:.3f}s"
            )
        print("Operators' statistics:")

        for index, strategy in enumerate(strategies):
            print(f"    {strategy:<{max(len(strategy) for strategy in strategies)}}:")

            for operator_index, operator in enumerate(operators):
                print(f"        {operator}: {operators_count[index][operator_index]}")


if __name__ == "__main__":
    main()
