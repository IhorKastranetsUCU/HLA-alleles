import numpy as np

def cost(r_alleles: set[str], d_alleles: set[str]) -> float:
    '''
    checks how well a given donor is suitable for a given recipient
    returns a float number from 0 to 1
    0 is the best possible
    1 is the worst
    '''
    omega = len(d_alleles)
    mismatch = 0
    # r_alleles, d_alleles = sorted(list(r_alleles), key = lambda x: x[0]), sorted(list(d_alleles), key = lambda x: x[0])
    for d in d_alleles:
        if d not in r_alleles:
            mismatch += 1
    return round(mismatch / omega, 4)

def cost_matrix(recepients: list[set], donors: list[set]) -> np.ndarray[np.ndarray]:
    '''
    makes cost matrix out of given recepients and donors
    '''
    matrix = [[1.0 for _ in range(len(donors))] for _ in range(len(recepients))]
    for row, r_alleles in enumerate(recepients):
        for column, d_alleles in enumerate(donors):
            if r_alleles == d_alleles:
                matrix[row][column] = 0.0
            else:
                matrix[row][column] = cost(r_alleles, d_alleles)
    return np.array(matrix)
