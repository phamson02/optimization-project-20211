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

'''
K = 4
N = 15
d = [72, 64, 16, 64, 100, 19, 27, 35, 99, 78, 59, 63, 40, 37, 87]
t = [[0, 59, 60, 58, 15, 12, 42, 13, 27, 14, 25, 29, 14, 16, 21, 30], 
     [51, 0, 39, 47, 24, 36, 32, 33, 57, 57, 50, 48, 49, 26, 11, 28], 
     [45, 43, 0, 60, 43, 19, 25, 40, 34, 37, 31, 35, 24, 23, 20, 27], 
     [15, 47, 12, 0, 11, 16, 36, 10, 21, 31, 22, 11, 35, 41, 24, 37], 
     [11, 24, 54, 52, 0, 42, 32, 23, 51, 44, 46, 27, 55, 37, 40, 59], 
     [12, 15, 50, 60, 30, 0, 51, 26, 34, 33, 40, 25, 40, 45, 49, 33], 
     [46, 23, 14, 28, 26, 60, 0, 51, 50, 52, 37, 17, 34, 47, 25, 36], 
     [21, 27, 56, 44, 40, 51, 53, 0, 42, 46, 13, 19, 17, 59, 37, 47], 
     [60, 26, 40, 20, 30, 44, 19, 32, 0, 21, 33, 40, 23, 47, 44, 53], 
     [28, 21, 48, 35, 54, 35, 21, 34, 55, 0, 43, 13, 59, 28, 36, 50], 
     [42, 23, 53, 33, 15, 44, 13, 19, 16, 58, 0, 13, 32, 28, 28, 18], 
     [27, 49, 37, 42, 37, 56, 19, 20, 43, 56, 22, 0, 24, 20, 27, 50], 
     [51, 28, 59, 43, 12, 11, 51, 57, 33, 42, 53, 54, 0, 42, 28, 16], 
     [14, 42, 32, 34, 33, 22, 41, 26, 44, 22, 14, 17, 12, 0, 28, 25], 
     [48, 31, 34, 34, 46, 26, 48, 11, 57, 57, 43, 26, 17, 29, 0, 10], 
     [42, 23, 49, 29, 37, 52, 42, 16, 13, 52, 14, 37, 53, 12, 21, 0]]
'''
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
        #print('After TSP')
    #for m in temp:
        #print(temp[m])
        #temp[u] = list(travel)
    #print('done')
    '''
    print(f'Optimal value = {max(temp_total_time)}')
    for k in range(K):
        #print(cluster[k], end=' | ')
        print(*temp[k], sep=' -> ', end=' | ')
        print(f'cost = {temp_total_time[k]}')
    print()
    '''
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
