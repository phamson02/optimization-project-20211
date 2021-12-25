class Data:
    '''
    Data class for the scheduling problem

    Attributes:
    -----------
        N: int
            Number of customers
        K: int
            Number of workers
        d: list
            d[i-1] is the time to fix the i-th customer
        t: list of lists
            Matrix of travel times for each customer
    '''

    def __init__(self, N, K, d, t):
        self.N = N
        self.K = K
        self.d = d
        self.t = t

    @classmethod
    def from_file(cls, filename):
        '''
        Reads data from a file in data folder
        '''
        with open(filename, 'r') as f:
            N, K = [int(x) for x in f.readline().split()]
            d = [int(x) for x in f.readline().split()[:N]]
            t = []
            for _ in range(N + 1):
                t.append([int(x) for x in f.readline().split()[:N+1]])

        return cls(N, K, d, t)

    @classmethod
    def generated_with(cls, N: int, K: int, seed: int = None, range_d: tuple = (1, 100), range_t: tuple = (1, 100)):
        '''
        Generates a random data model with N customers, K vehicles and
        the range of d and t can be specified by range_d and range_t 
        '''
        import random as rd
        rd.seed(seed)

        d = [rd.randint(*range_d) for _ in range(N)]
        t = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
        for i in range(N + 1):
            for j in range(N + 1):
                if i != j:
                    t[i][j] = rd.randint(*range_t)

        return cls(N, K, d, t)

    def __str__(self):
        l1 = f'N: {self.N}\n'
        l2 = f'K: {self.K}\n'
        l3 = f'd: {self.d}\n'
        l4 = f't:\n'
        l4 += '\n'.join(f'{i}: {self.t[i]}' for i in range(self.N+1))

        return l1 + l2 + l3 + l4

    def save_as(self, filename):
        '''
        Saves the data model to a file
        '''
        with open(filename, 'w') as f:
            f.write(f'{self.N} {self.K}\n')
            f.write(' '.join(str(x) for x in self.d[1:]))
            f.write('\n')
            for i in range(self.N+1):
                f.write(' '.join(str(x) for x in self.t[i]))
                f.write('\n')
