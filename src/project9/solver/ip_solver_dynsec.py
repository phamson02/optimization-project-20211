from ortools.linear_solver import pywraplp
import time


def ip_solver_dyn_sec(data):
    '''
    Solve the scheduling problem using the IP solver 
    with dynamic subtour elimination constraints formulation.

    Parameters
    ----------
    data : Data
        The data to be used in the problem.
    '''

    def solve_with_given_SEC(SECs):
        '''
        Solve the scheduling problem (TSP-like) using the given SEC.

        Parameters
        ----------
        SECs : list of list of int
            The SECs to be used.

        Returns
        -------
        solution: list of lists of int
            The value of binary variables
        objective_value: int
            The objective value of the solution
        '''
        solver = pywraplp.Solver.CreateSolver('CBC')

        # Create the variables
        x = [[[solver.IntVar(0, 1, f'x({u}, {i}, {j})') for j in range(
            data.N+1)] for i in range(data.N+1)] for u in range(data.K)]

        total_fix_time = sum(data.d)
        total_travel_time = sum(sum(i) for i in data.t)
        # Working time = Fix time + Travel time at each node
        y = [solver.IntVar(0, total_fix_time + total_travel_time,
                           f'y({u})') for u in range(data.K)]
        # The maximum working time of a technician
        w = solver.IntVar(0, total_fix_time + total_travel_time, 'w')

        for i in range(1, data.N+1):
            c1 = solver.Constraint(1, 1)
            for k in range(data.K):
                for j in range(data.N+1):
                    if j != i:
                        c1.SetCoefficient(x[k][i][j], 1)

        for j in range(1, data.N+1):
            c2 = solver.Constraint(1, 1)
            for k in range(data.K):
                for i in range(data.N+1):
                    if i != j:
                        c2.SetCoefficient(x[k][i][j], 1)

        for k in range(data.K):
            for l in range(data.N+1):
                c3 = solver.Constraint(0, 0)
                for i in range(data.N+1):
                    if i != l:
                        c3.SetCoefficient(x[k][i][l], 1)
                for j in range(data.N+1):
                    if j != l:
                        c3.SetCoefficient(x[k][l][j], -1)

        # Add the SEC constraints
        for C in SECs:
            for k in range(data.K):
                c4 = solver.Constraint(0, len(C)-1)
                [c4.SetCoefficient(x[k][i][j], 1)
                 for i in C for j in C if j != i]

        for k in range(data.K):
            c4 = solver.Constraint(1, 1)
            for j in range(1, data.N+1):
                c4.SetCoefficient(x[k][0][j], 1)

        for k in range(data.K):
            c5 = solver.Constraint(1, 1)
            for i in range(1, data.N+1):
                c5.SetCoefficient(x[k][i][0], 1)

        for k in range(data.K):
            c7 = solver.Constraint(0, 0)
            c7.SetCoefficient(y[k], -1)
            for i in range(data.N+1):
                for j in range(1, data.N+1):
                    if i != j:
                        c7.SetCoefficient(
                            x[k][i][j], data.t[i][j] + data.d[j-1])
                if i != 0:
                    c7.SetCoefficient(x[k][i][0], data.t[i][0])

        INF = solver.infinity()
        for k in range(data.K):
            c8 = solver.Constraint(0, INF)
            c8.SetCoefficient(y[k], -1)
            c8.SetCoefficient(w, 1)

        # Create the objective function
        obj = solver.Objective()
        obj.SetCoefficient(w, 1)
        obj.SetMinimization()

        # Solve the problem
        solver.Solve()
        solution = [[[x[u][i][j].solution_value() for j in range(data.N+1)]
                     for i in range(data.N+1)] for u in range(data.K)]
        objective_value = obj.Value()

        return solution, objective_value

    def findNext(s, u, x):
        for i in range(data.N + 1):
            if i != s and x[u][s][i] == 1:
                return i
        return -1

    def extract_subtour(s, x):
        C = []
        C.append(s)
        for k in range(data.K):
            if sum(x[k][s]) == 1:
                u = k
                break
        while True:
            i = findNext(s, u, x)
            if i == 0:
                return u, None
            if i in C:
                return u, C
            C.append(i)
            s = i

    def route(k, x):
        s = [0]
        i = 0
        while True:
            i = findNext(i, k, x)
            if i == 0:
                s += [0]
                break
            else:
                s += [i]
        return s

    def solve_TSP():
        SECs = []
        start_time = time.time()
        while True:
            solution, objective_value = solve_with_given_SEC(SECs)
            print(f'Found solution with objective value {objective_value}')
            for k in range(data.K):
                route_k = route(k, solution)
                print(f'Route[{k}] = ' + ' -> '.join(str(e) for e in route_k))

            found_subtour = False
            # Discover sub-tours of the solution
            visited = [False] * (data.N + 1)
            for i in range(1, data.N + 1):
                if visited[i]:
                    continue
                u, C = extract_subtour(i, solution)
                if C:
                    print(
                        f'Found subtour {C} in the route of technician {u}\n')
                    found_subtour = True
                    SECs.append(C)
                    for j in C:
                        visited[j] = True

            if not found_subtour:
                end_time = time.time()
                print('Found the optimal solution')
                for k in range(data.K):
                    route_k = route(k, solution)
                    fix_time = f'fix time = {sum(data.d[e-1] if e != 0 else 0 for e in route_k)}'
                    travel_time = f'travel time = {sum(data.t[i][j] for i, j in zip(route_k, route_k[1:]))}'
                    print(
                        f'Route[{k}]: {fix_time} | {travel_time}')
                print(f'\nSolving time = {end_time - start_time}')
                return None

    return solve_TSP()
