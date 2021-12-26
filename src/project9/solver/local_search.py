import numpy as np
import random as rd
import copy

def create_data(filename):
    with open(filename) as f:
        N, K = [int(x) for x in f.readline().split()]
        d = [int(x) for x in f.readline().split()]
        time = [[int(x) for x in f.readline().split()] for i in range(N+1)]
    return N, K, d, time

N, K, d, t = create_data('data_test.txt')

cluster = {k:[0] for k in range(K)}
d_new = [0] + list(d)

def fix_time(x):
    fix_time = 0
    for i in range(1,len(x)):
        fix_time += d_new[x[i]]   #d_new là d thêm 0 ở đầu tiên
    return fix_time

def BranchAndBound(x):
    global f_opt, y_opt

    visited[0] = True
    Branch(1)

    return f_opt + fix_time(x), y_opt
 
def Branch(z):
    global f, f_opt, y_opt
    if z >= len(x):
        #print(y)
        if f + t[y[-1]][0] < f_opt:
            f_opt = f + t[y[-1]][0]
            y_opt = list(y) + [0]
            

    for i in x:
        if visited[i] == False:
            y[z] = i
            visited[i] = True
            f += t[y[z-1]][i]
            g = f + (len(x)-z)*t_min 
            if g < f_opt :
                Branch(z+1)
            f = f - t[y[z-1]][i]
            visited[i] = False


remain = N
while remain != 0:
    cluster[remain % K].append(remain)
    remain -= 1
print(cluster, end='\n\n')


total_time = []
for k in range(K):
    x = list(cluster[k])
    t_min = np.Infinity
    for i in x+[0]:
        for j in x+[0]:
            if t[i][j] < t_min and i != j:
                t_min = t[i][j]

    f_opt = np.Infinity #Kết quả tối ưu  #biến global
    y = [0] * len(x)  #biến global
    y_opt = []
    visited = {i:False for i in x} #biến global
    f = 0 #biến global

    working_time, travel = BranchAndBound(x)
    total_time.append(working_time)
    cluster[k] = list(travel)

print(cluster)
print(total_time)

diff = 1e8
cnt = 100000
while cnt != 0:
    max_time = max(total_time)

    Min = np.argmin(total_time)
    Max = np.argmax(total_time)
    #print(f'Min = {Min}')
    #print(f'Max = {Max}')

    temp = copy.deepcopy(cluster)
    temp_total_time = list(total_time)
    r = rd.randint(1, len(temp[Max]) - 2)
    #print(f'r = {r}')
    temp[Min].insert(1, temp[Max].pop(r))
    #print(temp[Min], temp[Max], sep = '\n')

    for u in [Min, Max]:
        #print(u, end = ' ')
        x = list(temp[u][:-1])
        t_min = np.Infinity
        for i in x+[0]:
            for j in x+[0]:
                if t[i][j] < t_min and i != j:
                    t_min = t[i][j]
        
        
        f_opt = np.Infinity #Kết quả tối ưu  #biến global
        y = [0] * len(x)  #biến global
        y_opt = []
        visited = {i:False for i in x} #biến global
        f = 0 #biến global
        temp_total_time[u], temp[u] = BranchAndBound(x)

    if max(temp_total_time) < max_time:
        cluster = copy.deepcopy(temp)
        total_time = list(temp_total_time)
        
        print(f'Optimal value = {max(total_time)}')
        for k in range(K):
            #print(cluster[k], end=' | ')
            print(*cluster[k], sep=' -> ', end=' | ')
            print(f'cost = {total_time[k]}')
        print()
        
    cnt -= 1
