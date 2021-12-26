import numpy as np
import time


def BAB(data):
    N, K, d, t = data.N, data.K, data.d, data.t

    t_min = np.Infinity
    for i in range(N+1):
        for j in range(N+1):
            if t[i][j] < t_min and i != j:
                t_min = t[i][j]

    d_new = [0]
    d_new.extend(d)

    cus_for_k = [0 for k in range(K)]
    j = N
    for k in range(K):
        cus_for_k[k] = int(np.ceil(j/(K-k)))
        j = N - sum(cus_for_k)

    def checkVisit(visited):
        cnt = 0
        for i in visited:
            if i == False:
                cnt += 1
        return cnt

    d = np.array(d)
    print(cus_for_k)
    remaining_custumer = cus_for_k
    lst = {k: [0] for k in range(K)}
    fixtime_for_k = np.array([0 for i in range(K)])
    visited = [False for i in range(N+1)]
    visited[0] = True

    while checkVisit(visited) != 0:
        pick_k = np.argmin(fixtime_for_k)
        min = np.Infinity
        min_index = 0
        for cus in range(1, N+1):
            if d_new[cus] < min and visited[cus] == False:
                min = d_new[cus]
                min_index = cus
        if remaining_custumer[pick_k] == 0:
            fixtime_for_k[pick_k] = sum(d)
        else:
            visited[min_index] = True
            lst[pick_k].append(min_index)
            fixtime_for_k[pick_k] += min
            remaining_custumer[pick_k] -= 1

    print("Arc for k:", lst)

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

    start = time.time()
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

    print("Total:", total_time)
    print("Optimal value:", max(total_time))
    end = time.time()
    print("Time = ", end - start)
