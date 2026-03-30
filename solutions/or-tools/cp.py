from ortools.sat.python import cp_model
import time 

def load_data_model():
    data = {}
    N = int(input())
    data['time_windows'] = []
    data['drop_off_time'] = []
    data['time_matrix'] = []
    for i in range(N):
        a,b,c = [int(_) for _ in input().split()]
        data['time_windows'].append((a,b))
        data["drop_off_time"].append(c)
    for i in range(N+1):
        data["time_matrix"].append([int(_) for _ in input().split()])
        data["max_edge"] = max([_ for _s in data['time_matrix'] for _ in _s])
    data["num_vehicles"] = 1
    return N, data

N, data = load_data_model()

print(N)

class VarArrayAndObjectiveSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions (objective, variable values, time)."""
    def __init__(self, x , y = None, z = None, t=None):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__x = x
        self.__y = y
        self.__z = z
        self.__t = t
        self.__solution_count = 0
        self.__start_time = time.time()

    def on_solution_callback(self):
        """Called on each new solution."""
        current_time = time.time()
        obj = self.ObjectiveValue()
        print('Solution %i, time = %0.2f s, objective = %i' %
              (self.__solution_count, current_time - self.__start_time, obj))
        for i in range(len(self.__x)): 
            print(self.Value(self.__x[i]), end = ' ')  
        print()
        if self.__y is not None:
            print()
            for i in range(len(self.__y)):
                for j in range(len(self.__y)):
                    print(self.Value(self.__y[i][j]), end = ' ') 
                print()
            print()
        if self.__z is not None:
            for i in range(len(self.__z)):
                for j in range(len(self.__z)):
                    print(self.Value(self.__z[i][j]), end = ' ') 
                print()
            print()
        if self.__t is not None:
            for i in range(len(self.__t)):
                for j in range(len(self.__t)):
                    for k in range(len(self.__t)):
                        print(self.Value(self.__t[i][j][k]), end = ' ')
                    print() 
                print()
            print()
        self.__solution_count += 1

    def solution_count(self):
        """Returns the number of solutions found."""
        return self.__solution_count
    
model = cp_model.CpModel()
x = [model.new_int_var(1, N, f"x_{i}") for i in range(N)]

model.add_all_different(x)

y = [[model.new_bool_var('y[%i][%i]' % (i,j)) for j in range(N+1)] for i in range(N+1)] 
z = [[model.new_bool_var('z[%i][%i]' % (i,j)) for j in range(N)] for i in range(N)]
t = [[[model.new_bool_var('t[%i][%i][%i]' % (i,j,k)) for k in range(N+1)] for j in range(N+1)] for i in range(N+1)] 

for i in range(N):
    for j in range(N+1):
        if i == 0:
            model.add(x[i] == j).only_enforce_if(y[0][j])
            model.add(x[i] != j).only_enforce_if(y[0][j].Not())

            model.add(x[i] == j).only_enforce_if(t[0][0][j])
            model.add(x[i] != j).only_enforce_if(t[0][0][j].Not())

            for k in range(1,N+1):
                model.add(t[0][k][j] == 0)

        if i > 0 and j > 0:
            model.add(x[i-1] == j).only_enforce_if(z[j-1][i-1])
            model.add(x[i-1] != j).only_enforce_if(z[j-1][i-1].Not())

        if i == N-1 and j > 0:
                model.add(x[i] == j).only_enforce_if(z[j-1][N-1])
                model.add(x[i] != j).only_enforce_if(z[j-1][N-1].Not())

                model.add(x[i] == j).only_enforce_if(y[j][0])
                model.add(x[i] != j).only_enforce_if(y[j][0].Not())

for j in range(1,N+1): 
    for k in range(1,N+1): 
        for l in range(1, N):
            if l == 1:
                for i in range(l, N):
                    model.add_bool_and(y[j][k]).only_enforce_if(z[j-1][i-1], z[k-1][i])
            else:
                for i in range(l, N):
                    model.add_bool_and(y[j][k].Not()).only_enforce_if(z[j-1][i-l], z[k-1][i])


for i in range(1, N+1):
    model.add_exactly_one([element for elements in t[i] for element in elements])
    for j in range(N+1):
        if j == 0:
            for k in range(N+1):
                model.add(t[i][0][k] == 0)
        else:
            for k in range(N+1):
                model.add_bool_and(t[i][j][k]).only_enforce_if(z[j-1][i-1], y[j][k])
func = 0

a = [model.new_int_var(0, 2*N*data['max_edge'], 'a[%i]' % i) for i in range(N)]

for i in range(N+1):
    for j in range(N+1):
        for k in range(N+1):
            func += data['time_matrix'][j][k] * t[i][j][k]
    if i < N:
        lower_bounds, upper_bounds = [_[0] for _ in data['time_windows']], [_[1] for _ in data['time_windows']]
        model.add_max_equality(a[i], [func, sum([lower_bounds[j] * z[j][i] for j in range(N)])])
        func = a[i]
        for j in range(N):
            func += data['drop_off_time'][j] * z[j][i]
        model.add(func <= sum([upper_bounds[j] * z[j][i] for j in range(N)]))

model.minimize(func)

solver = cp_model.CpSolver()
solution_printer = VarArrayAndObjectiveSolutionPrinter(x) 
status = solver.solve(model, solution_printer)

result = list()

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f'Minimum of objective function: {solver.ObjectiveValue()}\n')

else:
    print('No solution found.')

print('\nStatistic')
print(f'  status : {solver.StatusName(status)}')
print(f'  conflicts: {solver.NumConflicts()}')
print(f'  branches : {solver.NumBranches()}')
print(f'  wall time: {solver.WallTime()} s')
print(f'  Reasonable cost using OR-Tools: {solver.ObjectiveValue()}')
print()