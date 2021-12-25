import numpy as np
import time


def heuristic_greedy(data):
    '''
    Solve the problem using a greedy heuristic.
    Heuristic: Assign the job with the smallest travel time + fix time 
    to the technician with the smallest number of jobs.

    Parameters
    ----------
    data : Data
        The data to be used in the problem.
    '''
    start_time = time.time()

    # Initialize the solution
    x = np.array([0 for k in range(data.K)])  # working time of staff k
    y = {k: [0] for k in range(data.K)}  # customers that staff k serves

    customers = [n for n in range(1, data.N+1)]
    while len(customers) != 0:
        # Find the technician with the smallest number of jobs
        staff = np.argmin(x)

        # Find the last customer that the technician served
        i = y[staff][-1]

        # Find the next customer with the smallest travel time + fix time
        knowledge = []
        for l in customers:
            knowledge.append((l, data.t[i][l] + data.d[l-1]))
        knowledge.sort(key=lambda item: item[1])

        # Assign that customer to the technician and update the solution
        j = knowledge[0][0]
        y[staff].append(j)
        x[staff] += knowledge[0][1]

        # Remove the customer from the list of customers
        customers.remove(j)

    for k in range(data.K):
        x[k] += data.t[y[k][-1]][0]
        y[k].append(0)

    print(f'Solving time: {time.time() - start_time}')
    print(f'Optimal cost: {np.max(x)}')

    for k in range(data.K):
        journey = f'Route[{k}] = ' + ' -> '.join(str(e) for e in y[k])
        fix_time = f'fix time = {sum(data.d[e-1] if e != 0 else 0 for e in y[k])}'
        travel_time = f'travel time = {sum(data.t[i][j] for i, j in zip(y[k], y[k][1:]))}'
        total_time = f' total time = {x[k]}'
        print(f'{journey} | {fix_time} | {travel_time} | {total_time}')
        for i, j in zip(y[k], y[k][1:]):
            s1 = f'{i} -> {j}'
            s2 = f'travel time = {data.t[i][j]}'
            s3 = f'fix time = {data.d[j-1]}' if j != 0 else 'fix time = 0'
            print(f'{s1} | {s2} | {s3}')
