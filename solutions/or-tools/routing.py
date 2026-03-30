"""Vehicles Routing Problem (VRP) with Time Windows."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import sys

def load_data_model():
    data = {}
    N = int(input())
    data['time_windows'] = [(0,10)]
    data['drop_off_time'] = [0]
    data['time_matrix'] = []
    for i in range(N):
        a,b,c = [int(_) for _ in input().split()]
        data['time_windows'].append((a,b))
        data["drop_off_time"].append(c)
    for i in range(N+1):
        data["time_matrix"].append([int(_) for _ in input().split()])
    data["num_vehicles"] = 1
    data["depot"] = 0
    return N, data

def print_solution(N, data, manager, routing, solution):
    """Prints solution on console.""" 
    print(N)
    time_dimension = routing.GetDimensionOrDie("Time")
    total_time = 0 
    route = []
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id) 
        index_equal_0_first_time = False
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        old_index = index
        while not routing.IsEnd(index):
            if index == 0 and not index_equal_0_first_time:
                index_equal_0_first_time = True
            elif index == 0 and index_equal_0_first_time:
                index = old_index
                continue
            time_var = time_dimension.CumulVar(index)
            plan_output += (
                f"{manager.IndexToNode(index)}"
                f" Time({solution.Min(time_var)},{solution.Max(time_var)})"
                " -> "
            )
            
            route.append(f"{manager.IndexToNode(index)}")

            old_index = index
            index = solution.Value(routing.NextVar(index)) 
        time_var = time_dimension.CumulVar(index)
        plan_output += (
            f"{manager.IndexToNode(index)}"
            f" Time({solution.Min(time_var)},{solution.Max(time_var)})\n"
        )
        plan_output += f"Time of the route: {solution.Min(time_var)}min\n" 
        print(" ".join(route[1:]))
        total_time += solution.Min(time_var) 
    print(f"Objective: {total_time}")

def main():
    """Solve the VRP with time windows.""" 
    N, data = load_data_model()  

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        N+1, data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes.""" 
        if to_index != 0:
            from_node = manager.IndexToNode(from_index) 
            to_node = manager.IndexToNode(to_index)
            return data["time_matrix"][from_node][to_node] + data['drop_off_time'][from_node]
        else:
            return data['drop_off_time'][from_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time Windows constraint.
    time = "Time"
    routing.AddDimension(
        evaluator_index=transit_callback_index,
        slack_max=100000,  # allow waiting time 
        capacity=1000000,
        fix_start_cumul_to_zero=True,  # Don't force start cumul to zero.
        name=time,
    )
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data["time_windows"]):
        if location_idx == data["depot"]:
            continue
        index = manager.NodeToIndex(location_idx)
        # print(index)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1]- data['drop_off_time'][location_idx])

    # Add time window constraints for each vehicle start node.
    depot_idx = data["depot"]
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data["time_windows"][depot_idx][0], data["time_windows"][depot_idx][1]
        )

    # Instantiate route start and end times to produce feasible times.
    for i in range(data["num_vehicles"]):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i))
        )
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    # search_parameters.local_search_metaheuristic = (
    # routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    # )
    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(N, data, manager, routing, solution) 


if __name__ == "__main__":
    main()