import random as rd
import copy

def create_data(filename):
    with open(filename) as f:
        N, K = [int(x) for x in f.readline().split()]
        d = [int(x) for x in f.readline().split()]
        time = [[int(x) for x in f.readline().split()] for i in range(N+1)]
    return N, K, d, time

N, K, d, time = create_data('data_test.txt')
total_fix_time = sum(d)
cluster = {k:[0] for k in range(K)}

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
cnt = 200000
while cnt != 0:
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
        if ratio < diff:
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
