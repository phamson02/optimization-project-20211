import random as rd
import time


def heuristic_v2(data):

    start_time = time.time()

    N, K, d, t = data.N, data.K, data.d, data.t

    # The number of customes assigned to each technician does not exceed (N//K + 1)
    max_cus = N // K + 1
    # List of remaining customers to be assigned
    remaining_custumer = [i for i in range(1, N+1)]
    # Dictionary of assigned customers to each technician, initially [0] for each technician
    lst = {k: [0] for k in range(K)}

    time_consumption = [0 for k in range(K)]

    for k in range(K):
        num_cus = 0
        # While the number of customers assigned to technician k does not exceed max_cus
        # and there are still customers to be assigned
        while num_cus <= max_cus and len(remaining_custumer) != 0:
            if len(lst[k]) == 1:  # If the technician is still in the depot
                # Assign a random customer to the technician
                j = rd.choice(remaining_custumer)
                lst[k].append(j)
                remaining_custumer.remove(j)
                time_consumption[k] += t[0][j] + d[j-1]
                num_cus += 1
            else:
                # Find the customer that have the shortest working time needed
                distance = []
                i = lst[k][-1]
                for j in remaining_custumer:
                    distance.append((j, t[i][j] + d[j-1]))
                distance.sort(key=lambda item: item[1])
                j = distance[0][0]
                # Assign that customer to the technician
                lst[k].append(j)
                remaining_custumer.remove(j)
                time_consumption[k] += t[i][j] + d[j-1]
                num_cus += 1

        lst[k].append(0)
        time_consumption[k] += t[lst[k][-1]][0]

    print(f'Solving time: {time.time() - start_time}')
    print(f'Optimal cost: {max(time_consumption)}')

    for k in range(data.K):
        journey = f'Route[{k}] = ' + ' -> '.join(str(e) for e in lst[k])
        fix_time = f'fix time = {sum(data.d[e-1] if e != 0 else 0 for e in lst[k])}'
        travel_time = f'travel time = {sum(data.t[i][j] for i, j in zip(lst[k], lst[k][1:]))}'
        total_time = f' total time = {time_consumption[k]}'
        print(f'{journey} | {fix_time} | {travel_time} | {total_time}')
        for i, j in zip(lst[k], lst[k][1:]):
            s1 = f'{i} -> {j}'
            s2 = f'travel time = {data.t[i][j]}'
            s3 = f'fix time = {data.d[j-1]}' if j != 0 else 'fix time = 0'
            print(f'{s1} | {s2} | {s3}')
