from ortools.sat.python import cp_model


def cp_solver(data, time_limit=None, return_routes=False):
    '''
    Solve the scheduling problem using the CP solver.

    Parameters
    ----------
    data : Data
        The data to be used in the problem.
    '''

    # Guest positions: [1, ..., N] -> [0, ..., N-1]
    # Start nodes: [0] -> [N, N+1, ..., N+K-1]
    # End nodes: [0] -> [N+K, ..., N+2K-1]
    N = data.N
    K = data.K
    d = data.d + [0] * (2*data.K)

    # Recreate the travel time matrix with reindexed nodes
    t = [data.t[i][1:] + [data.t[i][0]] * (2*data.K)
         for i in range(1, data.N+1)]
    [t.append(data.t[0][1:] + [0] * (2*data.K)) for _ in range(2*data.K)]

    # Create useful sets
    def A_set():  # Set of valid arcs
        for i in range(N + 2*K):
            for j in range(N + 2*K):
                # Cannot go into the start nodes, cannot go out of the end nodes, no loops
                if (j not in range(N, N+K)) and (i not in range(N + K, N + 2*K)) and (i != j):
                    yield (i, j)

    # Set of nodes that go out of node a
    def Ao(a): return (j for i, j in A_set() if i == a)
    # Set of nodes that go into node a
    def Ai(a): return (i for i, j in A_set() if j == a)

    model = cp_model.CpModel()

    # Create the variables
    # x[i][j] = 1 if arc (i, j) is there is a technician travels from i to j
    x = [[model.NewIntVar(0, 1, f'x[{i}][{j}]')
          for j in range(N + 2*K)] for i in range(N + 2*K)]

    total_fix_time = sum(data.d)
    total_travel_time = sum(sum(i) for i in data.t)

    # Culmulative working time at node i
    y = [model.NewIntVar(0, total_fix_time +
                         total_travel_time, f'y[{i}]') for i in range(N + 2*K)]

    # Index of the technician that is currently working at node i
    z = [model.NewIntVar(1, K, f'z[{i}]') for i in range(N + 2*K)]

    # The maximum working time of a technician
    w = model.NewIntVar(0, total_fix_time + total_travel_time, 'w')

    # Each guest is visited by exactly one technician
    for l in range(N):
        model.Add(sum(x[i][l] for i in Ai(l)) == 1)
        model.Add(sum(x[l][j] for j in Ao(l)) == 1)

    # Technician k starts his journey at the start node N+k
    # and ends at the end node N+K+k
    for k in range(K):
        model.Add(sum(x[N+k][i] for i in range(N)) == 1)
        model.Add(sum(x[i][N+K+k] for i in range(N)) == 1)

    # Culmulative working time at start nodes are 0
    [model.Add(y[N + k] == 0) for k in range(K)]

    # Technician k starts his journey at the start node N+k
    # and ends at the end node N+K+k
    [model.Add(z[N + k] == k+1) for k in range(K)]
    [model.Add(z[N + K + k] == k+1) for k in range(K)]

    b = [[model.NewBoolVar(f'b({i},{j})')
          for j in range(N + 2*K)] for i in range(N + 2*K)]

    for i, j in A_set():
        model.Add(x[i][j] == 1).OnlyEnforceIf(b[i][j])
        model.Add(x[i][j] == 0).OnlyEnforceIf(b[i][j].Not())
        # If there is an technician that travels from i to j,
        # the culmulative working time at j is equal to the
        # culmulative working time at i plus the travel time and the fix time at j
        model.Add(y[j] == y[i] + t[i][j] + d[j]).OnlyEnforceIf(b[i][j])
        # and the indexes of the technicians at node i and j match
        model.Add(z[j] == z[i]).OnlyEnforceIf(b[i][j])

    # The working time of a technician is the culmulative working time at the end node
    [model.Add(w >= y[N + K + k]) for k in range(K)]

    # Create the objective function
    model.Minimize(w)

    # Solve the problem
    solver = cp_model.CpSolver()
    if time_limit:
        solver.parameters.max_time_in_seconds = time_limit
    status = solver.Solve(model)

    # Functions to print the solution

    def next_of(i):
        for j in Ao(i):
            if solver.Value(x[i][j]) == 1:
                return j
        return None

    def route(k):
        s = [0]
        i = k + N
        while True:
            i = next_of(i)
            if i == N + K + k:
                s += [0]
                break
            else:
                s += [i + 1]
        return s

    def print_solution():
        print(f'Solver wall time {solver.WallTime()} s')
        print(f'Optimal cost: {solver.ObjectiveValue()}')
        for k in range(K):
            route_k = route(k)
            journey = f'Route[{k}] = ' + ' -> '.join(str(e) for e in route_k)
            fix_time = f'fix time = {sum(data.d[e-1] if e != 0 else 0 for e in route_k)}'
            travel_time = f'travel time = {sum(data.t[i][j] for i, j in zip(route_k, route_k[1:]))}'
            total_time = f' total time = {solver.Value(y[N + K + k])}'
            print(f'{journey} | {fix_time} | {travel_time} | {total_time}')
            for i, j in zip(route_k, route_k[1:]):
                s1 = f'{i} -> {j}'
                s2 = f'travel time = {data.t[i][j]}'
                s3 = f'fix time = {d[j-1]}' if j != 0 else 'fix time = 0'
                print(f'{s1} | {s2} | {s3}')

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:

        if return_routes:
            routes = {k: [] for k in range(1, K+1)}
            for k in range(K):
                routes[k+1] = route(k)
            return routes

        else:
            print_solution()

    else:
        print('No solution found')
