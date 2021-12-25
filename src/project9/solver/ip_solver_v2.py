from ortools.linear_solver import pywraplp
import numpy as np

def create_data(filename):
    with open(filename) as f:
        N, K = [int(x) for x in f.readline().split()]
        d = [int(x) for x in f.readline().split()]
        time = [[int(x) for x in f.readline().split()] for i in range(N+1)]
    return N, K, d, time

K = 2
N = 15
d = [20, 90, 43, 60, 50, 65, 36, 93, 81, 30, 12, 84, 35, 40, 88]
time = [[0, 25, 48, 58, 32, 32, 50, 28, 58, 37, 55, 52, 50, 50, 59, 50], [34, 0, 35, 11, 17, 31, 24, 10, 50, 59, 30, 54, 19, 11, 46, 23], [10, 22, 0, 32, 32, 40, 58, 36, 37, 56, 23, 46, 21, 15, 37, 50], [43, 50, 17, 0, 46, 60, 36, 41, 15, 26, 11, 52, 41, 20, 48, 23], [35, 53, 29, 37, 0, 13, 57, 32, 18, 12, 57, 37, 26, 41, 30, 58], [48, 31, 40, 18, 39, 0, 39, 15, 29, 20, 54, 42, 22, 17, 20, 29], [18, 25, 50, 50, 59, 10, 0, 42, 54, 30, 16, 14, 30, 45, 30, 46], [52, 16, 57, 35, 29, 40, 12, 0, 50, 37, 41, 26, 29, 60, 29, 35], [32, 42, 31, 48, 44, 27, 35, 47, 0, 26, 18, 20, 10, 46, 50, 40], [36, 33, 20, 29, 59, 15, 56, 39, 36, 0, 52, 38, 34, 33, 27, 51], [41, 60, 46, 30, 50, 58, 56, 23, 50, 40, 0, 48, 15, 53, 57, 32], [22, 21, 16, 26, 19, 57, 24, 43, 44, 21, 18, 0, 25, 56, 19, 23], [59, 53, 29, 44, 15, 52, 39, 11, 25, 22, 42, 18, 0, 14, 31, 44], [60, 46, 43, 33, 53, 25, 49, 27, 23, 33, 22, 24, 25, 0, 14, 47], [14, 13, 17, 20, 44, 14, 24, 41, 22, 28, 54, 52, 13, 15, 0, 56], [24, 40, 59, 23, 11, 44, 37, 54, 34, 50, 43, 13, 36, 34, 51, 0]]

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
            A.append([i,j])

Ao = lambda x: (j for i,j in A if i == x)
Ai = lambda x: (i for i,j in A if j == x)


total_fix_time = sum(d)
total_travel_time = sum(sum(i) for i in time)
M = total_fix_time + max(d)


#create solver
solver = pywraplp.Solver.CreateSolver('CBC')
INF = solver.infinity()


#Variables
x = [[[solver.IntVar(0,1, f'x[{k},{i},{j}]') for j in range(N+2*K)] for i in range(N+2*K)] for k in range(K)]
z = [solver.IntVar(0, K, f'z[{i}]') for i in range(N+2*K)]
u = [solver.IntVar(0, N-1, f'u[{i}]') for i in range(N)]
y = [solver.IntVar(0, total_fix_time + total_travel_time, f'y[{k}]') for k in range(K)]
a = solver.IntVar(0, total_fix_time + total_travel_time, 'a')


#Constraints:
for i in range(N):
    cstr = solver.Constraint(1, 1)
    for k in range(K):
        for j in Ao(i):
            cstr.SetCoefficient(x[k][i][j], 1)

for j in range(N):
    cstr = solver.Constraint(1,1)
    for k in range(K):
        for i in Ai(j):
            cstr.SetCoefficient(x[k][i][j], 1)


for i in range(N):
    for k in range(K):
        cstr = solver.Constraint(0,0)
        for j in Ao(i):
            cstr.SetCoefficient(x[k][i][j], 1)
        for j in Ai(i):
            cstr.SetCoefficient(x[k][j][i], -1)


for k in range(K):
    cstr = solver.Constraint(1,1)
    for j in range(N):
        cstr.SetCoefficient(x[k][k+N][j], 1)

for k in range(K):
    cstr = solver.Constraint(1,1)
    for j in range(N):
        cstr.SetCoefficient(x[k][j][k+K+N], 1)

for k in range(K):
    cstr = solver.Constraint(k,k)
    cstr.SetCoefficient(z[k+N], 1)

    cstr = solver.Constraint(k,k)
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
    for i,j in A:
        cstr = solver.Constraint(-M, INF)
        cstr.SetCoefficient(x[k][i][j], -M)
        cstr.SetCoefficient(z[j], 1)
        cstr.SetCoefficient(z[i], -1)

        cstr = solver.Constraint(-M, INF)
        cstr.SetCoefficient(x[k][i][j], -M)
        cstr.SetCoefficient(z[j], -1)
        cstr.SetCoefficient(z[i], 1)

for k in range(K):
    cstr = solver.Constraint(0,0)
    cstr.SetCoefficient(y[k], -1)
    for i,j in A:
        cstr.SetCoefficient(x[k][i][j], t[i][j] + d[j])


for k in range(K):
    cstr = solver.Constraint(0, INF)
    cstr.SetCoefficient(a, 1)
    cstr.SetCoefficient(y[k], -1)


obj = solver.Objective()
obj.SetCoefficient(a, 1)
obj.SetMinimization()

rs = solver.Solve()

print(f'Optimal value = {obj.Value()}')

def findNext(k,i):
    for j in Ao(i):
        if x[k][i][j].solution_value() > 0:
            return j
def route(k):
    s = ''
    i = k + N
    while i != k + K + N:
        s = s + str(i) + ' - '
        i = findNext(k,i)
    s = s + str(k + K + N)
    return s
def travel_time(k):
    time = 0
    i = k + N
    while i != k + K + N:
        j = findNext(k,i)
        time += t[i][j]
        i = j
    return time
    
for k in range(K):
    print('route[',k,'] = ',route(k), '| travel_time =', travel_time(k), '| total_time =', y[k].solution_value())
    for i,j in A:
        if x[k][i][j].solution_value() > 0:
            print('(',i,'-',j,')','t =', t[i][j])  
