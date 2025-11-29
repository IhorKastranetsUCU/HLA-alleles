def compatibility_rating(recepients: list[set], donors: list[set]) -> list[list]:
    matrix = [[0 for _ in range(len(donors))] for _ in range(len(recepients))]
    # len(donors) must be taken everywhere for n x n matrix
    for row, r_alleles in enumerate(recepients):
        for column, d_alleles in enumerate(donors):
            if r_alleles == d_alleles:
               matrix[row][column] = 2
            else:
                for allele in d_alleles:
                    if allele in r_alleles:
                        matrix[row][column] = 1
                        break
    return matrix

'''
As an example
print(compatibility_rating(
    [
        {"A*03:01", "B*15:01", "C*04:01"},
        {"A*24:02", "B*18:01", "C*12:03"},
        {"A*02:05", "B*44:02", "C*05:01"}
    ],
    [
        {"A*03:01", "B*15:02", "C*04:01"},
        {"A*24:02", "B*40:01", "C*12:02"},
        {"A*01:01", "B*44:02", "C*05:09"},
        {"A*02:05", "B*44:02", "C*05:01"}
    ]
))

Output will be -> [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 2]]


'''
