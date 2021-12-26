import random as rd
import numpy as np
import time


def heuristic_v2(data):

    start = time.time()

    N, K, d, t = data.N, data.K, data.d, data.t
    d_new = [0]
    d_new.extend(d)

    t_min = np.Infinity
    for i in range(N+1):
        for j in range(N+1):
            if t[i][j] < t_min and i != j:
                t_min = t[i][j]

    # number of customs for each k
    cus_for_k = [0 for k in range(K)]
    j = N
    for k in range(K):
        cus_for_k[k] = int(np.ceil(j/(K-k)))
        j = N - sum(cus_for_k)

    remaining_custumer = [i for i in range(1, N+1)]
    lst = {k: [0] for k in range(K)}
    time_consumption = [0 for k in range(K)]

    for k in range(K):
        num_cus = cus_for_k[k]
        while num_cus != 0 and len(remaining_custumer) != 0:
            if len(lst[k]) == 1:
                j = rd.choice(remaining_custumer)
                lst[k].append(j)
                remaining_custumer.remove(j)
                time_consumption[k] += t[0][j] + d[j-1]
                num_cus -= 1
            else:
                distance = []
                i = lst[k][-1]
                for j in remaining_custumer:
                    distance.append((j, t[i][j]))
                distance.sort(key=lambda item: item[1])
                j = distance[0][0]
                lst[k].append(j)
                remaining_custumer.remove(j)
                time_consumption[k] += t[i][j] + d[j-1]
                num_cus -= 1
        # lst[k].append(0)
        time_consumption[k] += t[lst[k][-1]][0]

    def fix_time(x):
        fix_time = 0
        for i in range(1, n):
            fix_time += d_new[x[i]]
        return fix_time

    print(lst)

    def BranchAndBound(x):
        nonlocal f_opt

        y[0] = 0
        visited[0] = True
        Branch(1)

        print("Total time:", f_opt + fix_time(x))
        print("Travelling time:", f_opt)

    def Branch(j):
        nonlocal f, f_opt
        if j >= n:
            if f + t[y[-1]][0] < f_opt:
                f_opt = f + t[y[-1]][0]
                print(*y, sep=" -> ", end=" ")
                print(f_opt)

        for i in x:
            if visited[i] == False:
                y[j] = i
                visited[i] = True
                f += t[y[j-1]][i]
                g = f + (n-j)*t_min
                if g < f_opt:
                    Branch(j+1)
                f = f - t[y[j-1]][i]
                visited[i] = False

    total_time = [0 for k in range(K)]
    for k in range(K):
        x = lst[k]
        n = len(x)
        f_opt = np.Infinity
        y = [0] * len(x)
        visited = {i: False for i in x}
        print(x)
        f = 0
        BranchAndBound(x)
        total_time[k] = f_opt + fix_time(x)

    '''

    print(f'Optimal cost: {max(time_consumption)}')
    for k in range(K):
        print(f'route {k + 1} :', end=' ')
        print(*lst[k], sep=' -> ', end=' | ')
        print(f'cost = {time_consumption[k]}')
    '''
    print("Total:", total_time)
    print("Optimal value:", max(total_time))
    end = time.time()
    print("Time = ", end - start)

    return max(total_time)
