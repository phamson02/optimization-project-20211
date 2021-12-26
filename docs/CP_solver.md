# A CP model for Project 9

### Variables
- $x[i][j]$: binary variable indicating whether there is a technician traverses from node $i$ to node $j$. 
- $y[i]$: the culmulative working time at node $i$. $i = \overline{1, N}$
- $z[i]$: the index of the technician assigned to node $i$. $i = \overline{1, N}$
- $w$: the maximum waiting time among technicians.

### Constraints
- For each customer $l$, there is exactly $1$ technician entering and $1$ leaving the customer's position:
$$\sum_{i \in Ai(l)} x[i][l] = \sum_{j \in Ao(l)} x[l][j] = 1, l = \overline{1, N}.$$
- Technician $k$ starts his journey at node $N+k$ and ends at node $N+K+k$:
$$\sum_{i = 1}^N x[N+k][i] = \sum_{i = 1}^N x[i][N+K+k] = 1 , k = \overline{1, K}.$$
- The culmulative working time at start nodes are 0:
$$y[N+k] = 0, k = \overline{1, K}.$$
- Technician $k$ starts his journey at node $N+k$ and ends at node $N+K+k$:
$$z[N+k] = z[N+K+k] = k, k = \overline{1, K}.$$
- If there is a technician that travels from node $i$ to node $j$, the culmulative working time at node $j$ is equal to the culmulative working time at node $i$ plus the travel time and the fixing time at $j$:
$$x[i][j] = 1 \Rightarrow y[j] = y[i] + t[i][j] + d[j], i, j \in A.$$
- If there is a technician that travels from node $i$ to node $j$, the indexes of the technician at $i$ and $j$ must match:
$$x[i][j] = 1 \Rightarrow z[i] = z[j], i, j \in A.$$
- The working time of a technician is the culmulative working time at the end node, thus the maximum working time among technicians satisfies:
$$w \geq y[N+K+k], k = \overline{1, K}.$$

### Objective
- The objective is to minimize the maximum waiting time among technicians:
$$\min_{x, y, z, w} w$$