from ortools.linear_solver import pywraplp
import numpy as np
import random as rd

def create_data(filename):
    with open(filename) as f:
        N, K = [int(x) for x in f.readline().split()]
        d = [int(x) for x in f.readline().split()]
        time = [[int(x) for x in f.readline().split()] for i in range(N+1)]
    return N, K, d, time

N, K, d, time = create_data('data_test.txt')
print(f'N = {N}, K = {K}')
print(f'd = {d}')
print(*time, sep='\n', end='\n\n')


cus_for_k = round(N/K)
remaining_custumer = [i for i in range(1, N+1)]
lst = {k:[0] for k in range(K)}
time_consumption = [0 for k in range(K)]

for k in range(K):
    num_cus = cus_for_k
    while num_cus != 0 and len(remaining_custumer) != 0:
        if len(lst[k]) == 1:
            j = rd.choice(remaining_custumer)
            lst[k].append(j)
            remaining_custumer.remove(j)
            time_consumption[k] += time[0][j] + d[j-1]
            num_cus -= 1
        else:
            distance = []
            i = lst[k][-1]
            for j in remaining_custumer:
                distance.append((j, time[i][j]))
            distance.sort(key=lambda item: item[1])
            j = distance[0][0]
            lst[k].append(j)
            remaining_custumer.remove(j)
            time_consumption[k] += time[i][j] + d[j-1]
            num_cus -= 1
    lst[k].append(0)
    time_consumption[k] += time[lst[k][-1]][0]

print(f'Optimal cost: {max(time_consumption)}')
for k in range(K):
    print(f'route {k + 1} :', end=' ')
    print(*lst[k], sep=' -> ', end=' | ')
    print(f'cost = {time_consumption[k]}')