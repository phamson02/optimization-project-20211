from ortools.sat.python import cp_model


def cp_solver(data, time_limit=None):
    '''
    Solve the scheduling problem using the CP solver.

    Parameters
    ----------
    data : Data
        The data to be used in the problem.
    '''

    class SolutionPrinter(cp_model.CpSolverSolutionCallback):
        # print intermediate solution
        def __init__(self, variables):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self.__variables = variables
            self.__solution_count = 0

        def on_solution_callback(self):
            self.__solution_count += 1
            for v in self.__variables:
                print('%s = %i' % (v, self.Value(v)), end=' ')
            print()

        def solution_count(self):
            return self.__solution_count

    # Duplicate the source node K times
    d = data.d + [0] * data.K
    t = [data.t[i] + [data.t[i][0]] * data.K for i in range(data.N+1)]
    [t.append(t[0]) for _ in range(data.K)]
    N = data.N + data.K + 1
    K = data.K

    model = cp_model.CpModel()

    # Create the variables
    x = [[model.NewIntVar(0, 1, f'x[{i}][{j}]')
          for j in range(N)] for i in range(N)]

    total_fix_time = sum(data.d)
    total_travel_time = sum(sum(i) for i in data.t)
    # Working time = Fix time + Travel time at each node
    z = [model.NewIntVar(0, total_fix_time +
                         total_travel_time, f'z({u})') for u in range(N)]
    # The maximum working time of a technician
    w = model.NewIntVar(0, total_fix_time + total_travel_time, 'w')

    for k in range(N):
        model.Add(sum(x[i][k] for i in range(N) if i != k) == 1)
        model.Add(sum(x[k][j] for j in range(N) if j != k) == 1)

    # Source nodes constraints
    for i in range(N-K, N-1):
        model.Add(x[0][i] == 0)
        model.Add(x[i][0] == 0)
        model.Add(x[i][N-1] == 0)
        model.Add(x[N-1][i] == 0)

    model.Add(x[N-1][0] == 1)

    # Add constraints on z and w
    model.Add(z[0] == 0)

    b = [[model.NewBoolVar(f'b({i},{j})') for j in range(N)] for i in range(N)]

    for i in range(N):
        for j in range(1, N):
            if i != j:
                model.Add(x[i][j] == 1).OnlyEnforceIf(b[i][j])
                model.Add(x[i][j] == 0).OnlyEnforceIf(b[i][j].Not())
                model.Add(z[j] == z[i] + d[j] + t[i][j]).OnlyEnforceIf(b[i][j])
                model.Add(x[j][i] == 0).OnlyEnforceIf(b[i][j])

    for i in range(N-K+1, N):
        model.Add(w >= z[i] - z[i-1])
    model.Add(w >= z[N-K])

    # Create the objective function
    model.Minimize(w)

    # Solve the problem
    solver = cp_model.CpSolver()
    if time_limit:
        solver.parameters.max_time_in_seconds = time_limit
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = [[solver.Value(x[i][j]) for j in range(N)]
                    for i in range(N)]
        objective_value = solver.Value(w)

    return solution, objective_value
