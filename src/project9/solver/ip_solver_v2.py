from ortools.linear_solver import pywraplp
import numpy as np


def ip_solver_v2(data):

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
    print(np.array(t))

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
    x = [[[solver.IntVar(0, 1, f'x[{u},{i},{j}]') for j in range(
        N+2*K)] for i in range(N+2*K)] for u in range(K)]
    y = [solver.IntVar(0, total_fix_time, f'y[{k}]') for k in range(K)]
    z = [solver.IntVar(0, K, f'z[{i}]') for i in range(N+2*K)]
    u = [solver.IntVar(0, N-1, f'u[{i}]') for i in range(N)]
    w = [solver.IntVar(0, total_fix_time + total_travel_time,
                       f'w[{k}]') for k in range(K)]
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
        cstr = solver.Constraint(0, 0)
        cstr.SetCoefficient(y[k], -1)
        for i, j in A:
            cstr.SetCoefficient(x[k][i][j], d[j])

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
        cstr.SetCoefficient(w[k], -1)
        cstr.SetCoefficient(y[k], 1)
        for i, j in A:
            cstr.SetCoefficient(x[k][i][j], t[i][j])

    for k in range(K):
        cstr = solver.Constraint(0, INF)
        cstr.SetCoefficient(a, 1)
        cstr.SetCoefficient(w[k], -1)

    obj = solver.Objective()
    obj.SetCoefficient(a, 1)
    obj.SetMinimization()

    rs = solver.Solve()

    print(f'Optimal value = {obj.Value()}')

    def findNext(k, i):
        for j in Ao(i):
            if x[k][i][j].solution_value() > 0:
                return j

    def route(k):
        s = ''
        i = k + N
        while i != k + K + N:
            s = s + str(i) + ' - '
            i = findNext(k, i)
        s = s + str(k + K + N)
        return s

    def travel_time(k):
        time = 0
        i = k + N
        while i != k + K + N:
            j = findNext(k, i)
            time += t[i][j]
            i = j
        return time

    for k in range(K):
        print('route[', k, '] = ', route(k), '| fix_time =', y[k].solution_value(
        ), '| travel_time =', travel_time(k), '| total_time =', travel_time(k) + y[k].solution_value())
        for i, j in A:
            if x[k][i][j].solution_value() > 0:
                print('(', i, '-', j, ')', 't =', t[i][j])
