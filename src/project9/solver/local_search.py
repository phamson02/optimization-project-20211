import numpy as np
import random as rd
import copy

def create_data(filename):
    with open(filename) as f:
        N, K = [int(x) for x in f.readline().split()]
        d = [int(x) for x in f.readline().split()]
        time = [[int(x) for x in f.readline().split()] for i in range(N+1)]
    return N, K, d, time

K = 4
N = 15
d = [72, 64, 16, 64, 100, 19, 27, 35, 99, 78, 59, 63, 40, 37, 87]
time = [[0, 59, 60, 58, 15, 12, 42, 13, 27, 14, 25, 29, 14, 16, 21, 30], [51, 0, 39, 47, 24, 36, 32, 33, 57, 57, 50, 48, 49, 26, 11, 28], [45, 43, 0, 60, 43, 19, 25, 40, 34, 37, 31, 35, 24, 23, 20, 27], [15, 47, 12, 0, 11, 16, 36, 10, 21, 31, 22, 11, 35, 41, 24, 37], [11, 24, 54, 52, 0, 42, 32, 23, 51, 44, 46, 27, 55, 37, 40, 59], [12, 15, 50, 60, 30, 0, 51, 26, 34, 33, 40, 25, 40, 45, 49, 33], [46, 23, 14, 28, 26, 60, 0, 51, 50, 52, 37, 17, 34, 47, 25, 36], [21, 27, 56, 44, 40, 51, 53, 0, 42, 46, 13, 19, 17, 59, 37, 47], [60, 26, 40, 20, 30, 44, 19, 32, 0, 21, 33, 40, 23, 47, 44, 53], [28, 21, 48, 35, 54, 35, 21, 34, 55, 0, 43, 13, 59, 28, 36, 50], [42, 23, 53, 33, 15, 44, 13, 19, 16, 58, 0, 13, 32, 28, 28, 18], [27, 49, 37, 42, 37, 56, 19, 20, 43, 56, 22, 0, 24, 20, 27, 50], [51, 28, 59, 43, 12, 11, 51, 57, 33, 42, 53, 54, 0, 42, 28, 16], [14, 42, 32, 34, 33, 22, 41, 26, 44, 22, 14, 17, 12, 0, 28, 25], [48, 31, 34, 34, 46, 26, 48, 11, 57, 57, 43, 26, 17, 29, 0, 10], [42, 23, 49, 29, 37, 52, 42, 16, 13, 52, 14, 37, 53, 12, 21, 0]]

cluster = {k:[0] for k in range(K)}

def proportion(cluster):
    total_time = []
    for k in range(K):
        temp = 0
        for x in range(len(cluster[k])-1):
            i, j = cluster[k][x], cluster[k][x+1]
            if j == 0:
                temp += time[i][j]
            else:
                temp += time[i][j] + d[j-1]
        total_time.append(temp)
    return max(total_time) - min(total_time), total_time


for i in range(N):
    cluster[0].append(i+1)
for k in range(K):
    cluster[k].append(0)
print(cluster, end='\n\n')

diff = 1e8
cnt = 300000
while cnt != 0:
    _, total_time = proportion(cluster)
    max_time = max(total_time)

    i = np.argmin(total_time)
    j = np.argmax(total_time)

    temp = copy.deepcopy(cluster)
    if len(temp[i]) == 2:
        x, y = 1, rd.randint(1, len(temp[j]) - 2)
    else:
        x, y = rd.randint(1, len(temp[i]) - 2), rd.randint(1, len(temp[j]) - 2)
    temp[i].insert(x, temp[j].pop(y))

    ratio, total_time = proportion(temp)

    if max(total_time) < max_time:
        diff = ratio
        cluster = copy.deepcopy(temp)

        print(f'Optimal value = {max(total_time)}')
        for k in range(K):
            #print(cluster[k], end=' | ')
            print(*cluster[k], sep=' -> ', end=' | ')
            print(f'cost = {total_time[k]}')
        print(f'diff = {diff}')
        print()

    cnt -= 1
