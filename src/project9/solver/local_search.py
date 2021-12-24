import random as rd
import copy

def create_data(filename):
    with open(filename) as f:
        N, K = [int(x) for x in f.readline().split()]
        d = [int(x) for x in f.readline().split()]
        time = [[int(x) for x in f.readline().split()] for i in range(N+1)]
    return N, K, d, time

N = 15
K = 2
d = [66, 67, 68, 45, 79, 83, 32, 22, 56, 94, 18, 62, 14, 33, 68]
time = [[0, 10, 56, 25, 51, 12, 33, 20, 25, 26, 31, 23, 32, 10, 34, 23], [54, 0, 48, 38, 56, 17, 16, 11, 39, 46, 12, 55, 27, 14, 10, 45], [30, 18, 0, 17, 20, 13, 33, 18, 22, 12, 39, 47, 12, 46, 38, 40], [26, 34, 53, 0, 29, 42, 47, 32, 30, 33, 45, 19, 36, 12, 16, 30], [54, 10, 19, 29, 0, 42, 15, 31, 13, 42, 42, 28, 15, 57, 17, 41], [56, 32, 11, 36, 52, 0, 47, 35, 35, 50, 58, 15, 19, 47, 33, 38], [55, 56, 40, 43, 30, 21, 0, 23, 56, 58, 41, 21, 17, 53, 52, 57], [12, 42, 50, 20, 13, 31, 43, 0, 58, 55, 17, 32, 46, 45, 54, 14], [11, 26, 54, 48, 27, 38, 33, 48, 0, 27, 39, 51, 32, 40, 15, 22], [30, 29, 59, 48, 57, 59, 50, 19, 46, 0, 20, 24, 52, 43, 44, 32], [21, 46, 39, 28, 13, 28, 39, 24, 51, 43, 0, 10, 19, 20, 17, 14], [47, 56, 11, 52, 41, 31, 22, 12, 16, 28, 29, 0, 44, 42, 24, 10], [21, 13, 16, 23, 57, 42, 11, 17, 54, 18, 12, 23, 0, 10, 27, 31], [36, 32, 22, 41, 57, 52, 17, 29, 33, 28, 18, 48, 37, 0, 54, 36], [46, 36, 48, 35, 52, 14, 49, 20, 12, 34, 20, 55, 34, 29, 0, 38], [57, 30, 38, 51, 52, 44, 58, 53, 56, 58, 43, 41, 50, 37, 33, 0]]


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
    max_value = max([sum(cluster[k]) for k in range(K)])
    staffs = [k for k in range(K)]
    i = rd.choice(staffs)
    staffs.remove(i)
    j = rd.choice(staffs)

    if len(cluster[j]) != 2:
        temp = copy.deepcopy(cluster)
        temp[i].insert(1, temp[j].pop(1))

        for k in range(K):
            lst = temp[k][1:-1]
            rd.shuffle(lst)
            del temp[k][1:]
            temp[k].extend(lst + [0])

        ratio, total_time = proportion(temp)
        if 15*ratio + max(total_time) < 15*diff + max_value:
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
