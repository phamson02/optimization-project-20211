# A IP model with dynamic SEC for Project 9

### Variables
- $x[k][i][j]$: binary variable indicating whether the technician $k$ traverses from node $i$ to node $j$. 
- $y[k]$: the working time at the technician $k$. $k = \overline{1, K}$
- $w$: the maximum waiting time among technicians.

### Constraints
- There is exactly one technician entering and one leaving each customer's position:
$$\sum_{k = 1}^K \sum_{j=0, j \neq i}^N x[k][i][j] = \sum_{k = 1}^K \sum_{j=0, j \neq i}^N x[k][j][i] = 1, i = \overline{1,N}.$$
- The same technician $k$ enters and leaves the position of a customer $l$:
$$\sum_{i=0, i\neq l}^N x[k][i][l] = \sum_{j=0, j \neq l}^N x[k][l][j], k = \overline{1,K}; l = \overline{1,N}.$$
- Subtour elimination constraints, the set $SECS$ is built dynamically in solving time:
$$\sum_{i \in C}{\sum_{j \ne i, j \in C}}{x[k][i][j]} \leq |C|-1, C \in SECS, k = \overline{1,K}.$$
- All technicians start their journey at node $0$ and ends at node $0$:
$$\sum_{j=1}^N x[k][0][j] = \sum_{i=1}^N x[k][i][0] = 1, k = \overline{1,K}.$$
- The working time of a technician the sum of travel time and fixing time (fixing time at mode $0$ is $0$, $d[0] = 0$):
$$y[k] = \sum_{i=0}^N \sum_{j=0, j \neq i}^N x[k][i][j] \cdot (t[i][j] + d[j]), k = \overline{1,K}.$$
- The maximum working time among technicians satisfies:
$$w \geq y[k], k = \overline{1, K}.$$

### Objective
- The objective is to minimize the maximum waiting time among technicians:
$$\min_{x, y, z, w} w$$