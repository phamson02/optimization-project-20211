from typing import Optional
import numpy as np
from numpy.core.arrayprint import format_float_positional
from numpy.lib.ufunclike import fix
def input(filename):
    with open(filename) as f:
        N, K = [int(x) for x in f.readline().split()]
        d = [int(x) for x in f.readline().split()]
        t = [[int(x) for x in f.readline().split()] for i in range(N+1)]
    return N, K, d, t

N, K, d, t = input("N6-K2.txt")
d_new = [0]
d_new.extend(d)
print(t)
print(d)
t_min = np.Infinity
for i in range(N+1):
    for j in range(N+1):
        if t[i][j] < t_min and i != j:
            t_min = t[i][j]
print("t_min =",t_min)


x = [0,2,4,6]  #Chuỗi cần tính time nhỏ nhất
n = len(x) 
f_opt = np.Infinity #Kết quả tối ưu
y = [0] * n  #
visited = {i:False for i in x}
f = 0
def BranchAndBound(x):
    global f_opt
    
    y[0] = 0
    visited[0] = True
    Branch(1)
    fix_time = 0
    for i in range(1,n):
        fix_time += d_new[x[i]]
    print( f_opt + fix_time)
    print(f_opt)
 
def Branch(k):
    global f, f_opt
    if k >= n:
        if f + t[y[-1]][0] < f_opt:
            f_opt = f + t[y[-1]][0]
            print(*y, sep=" ->")


    for i in x:
        if visited[i] == False:
            y[k] = i
            visited[i] = True
            f += t[y[k-1]][i]
            g = f + (n-k)*t_min 
            if g < f_opt :
                Branch(k+1)
                f = f - t[y[k-1]][i]
                visited[i] = False

BranchAndBound(x)



