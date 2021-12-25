from ortools.linear_solver import pywraplp


def ip_solver(data):

    N, K, d, time = data.N, data.K, data.d, data.t

    for i in range(2*K):
        d.append(0)

    def extend_matrix(t):
        m = []
        for i in range(1, N+2*K+1):
            row = []
            for j in range(1, N+2*K+1):
                if i <= N and j <= N:
                    row.append(t[i][j])
                elif i <= N and j > N:
                    row.append(t[i][0])
                elif i > N and j <= N:
                    row.append(t[0][j])
                else:
                    row.append(0)
            m.append(row)
        return m

    t = extend_matrix(time)

    A = []
    for i in range(N + 2*K):
        for j in range(N + 2*K):
            if (j not in range(N, N+K)) and (i not in range(N+K, N+2*K)) and (i != j):
                A.append([i, j])

    def Ao(x): return (j for i, j in A if i == x)
    def Ai(x): return (i for i, j in A if j == x)

    total_fix_time = sum(d)
    total_travel_time = sum(sum(i) for i in time)
    M = total_fix_time + max(d)

    # create solver
    solver = pywraplp.Solver.CreateSolver('CBC')
    INF = solver.infinity()

    # Variables
    x = [[[solver.IntVar(0, 1, f'x[{k},{i},{j}]') for j in range(
        N+2*K)] for i in range(N+2*K)] for k in range(K)]
    z = [solver.IntVar(0, K, f'z[{i}]') for i in range(N+2*K)]
    u = [solver.IntVar(0, N-1, f'u[{i}]') for i in range(N)]
    y = [solver.IntVar(0, total_fix_time + total_travel_time,
                       f'y[{k}]') for k in range(K)]
    a = solver.IntVar(0, total_fix_time + total_travel_time, 'a')

    # Constraints:
    for i in range(N):
        cstr = solver.Constraint(1, 1)
        for k in range(K):
            for j in Ao(i):
                cstr.SetCoefficient(x[k][i][j], 1)

    for j in range(N):
        cstr = solver.Constraint(1, 1)
        for k in range(K):
            for i in Ai(j):
                cstr.SetCoefficient(x[k][i][j], 1)

    for i in range(N):
        for k in range(K):
            cstr = solver.Constraint(0, 0)
            for j in Ao(i):
                cstr.SetCoefficient(x[k][i][j], 1)
            for j in Ai(i):
                cstr.SetCoefficient(x[k][j][i], -1)

    for k in range(K):
        cstr = solver.Constraint(1, 1)
        for j in range(N):
            cstr.SetCoefficient(x[k][k+N][j], 1)

    for k in range(K):
        cstr = solver.Constraint(1, 1)
        for j in range(N):
            cstr.SetCoefficient(x[k][j][k+K+N], 1)

    for k in range(K):
        cstr = solver.Constraint(k, k)
        cstr.SetCoefficient(z[k+N], 1)

        cstr = solver.Constraint(k, k)
        cstr.SetCoefficient(z[k+K+N], 1)

    # x[k][i][j] = 1 --> u[j] = u[i] + 1
    # M(1-x) + u[j] >= u[i] + 1
    # M(x-1) + u[j] <= u[i] + 1
    for k in range(K):
        for i in range(N):
            for j in range(N):
                cstr = solver.Constraint(-M + 1, INF)
                cstr.SetCoefficient(x[k][i][j], -M)
                cstr.SetCoefficient(u[j], 1)
                cstr.SetCoefficient(u[i], -1)

                cstr = solver.Constraint(-M - 1, INF)
                cstr.SetCoefficient(x[k][i][j], -M)
                cstr.SetCoefficient(u[j], -1)
                cstr.SetCoefficient(u[i], 1)

    for k in range(K):
        for i, j in A:
            cstr = solver.Constraint(-M, INF)
            cstr.SetCoefficient(x[k][i][j], -M)
            cstr.SetCoefficient(z[j], 1)
            cstr.SetCoefficient(z[i], -1)

            cstr = solver.Constraint(-M, INF)
            cstr.SetCoefficient(x[k][i][j], -M)
            cstr.SetCoefficient(z[j], -1)
            cstr.SetCoefficient(z[i], 1)

    for k in range(K):
        cstr = solver.Constraint(0, 0)
        cstr.SetCoefficient(y[k], -1)
        for i, j in A:
            cstr.SetCoefficient(x[k][i][j], t[i][j] + d[j])

    for k in range(K):
        cstr = solver.Constraint(0, INF)
        cstr.SetCoefficient(a, 1)
        cstr.SetCoefficient(y[k], -1)

    obj = solver.Objective()
    obj.SetCoefficient(a, 1)
    obj.SetMinimization()

    solver.Solve()

    def findNext(k, i):
        for j in Ao(i):
            if x[k][i][j].solution_value() > 0:
                return j

    def route(k):
        s = [0]
        i = k + N
        while True:
            i = findNext(k, i)
            if i == N + K + k:
                s += [0]
                break
            else:
                s += [i + 1]
        return s

    print('Solver wall time', solver.WallTime(), 'ms')
    print(f'Optimal cost: {obj.Value()}')
    for k in range(K):
        route_k = route(k)
        journey = f'Route[{k}] = ' + ' -> '.join(str(e) for e in route_k)
        fix_time = f'fix time = {sum(data.d[e-1] if e != 0 else 0 for e in route_k)}'
        travel_time = f'travel time = {sum(data.t[i][j] for i, j in zip(route_k, route_k[1:]))}'
        total_time = f' total time = {y[k].solution_value()}'
        print(f'{journey} | {fix_time} | {travel_time} | {total_time}')
        for i, j in zip(route_k, route_k[1:]):
            s1 = f'{i} -> {j}'
            s2 = f'travel time = {data.t[i][j]}'
            s3 = f'fix time = {d[j-1]}' if j != 0 else 'fix time = 0'
            print(f'{s1} | {s2} | {s3}')
