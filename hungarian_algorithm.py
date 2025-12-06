"""
This file includes 1 main function "hungarian_algorithm" and additional.
The function takes Numpy matrix and unsorted returns the list of tuples
where the first element is row and second is column
Example:
    >>> import numpy as np
    >>> matrix = np.array([[2, 3, 6, 2, 4],
    ...                    [5, 6, 8, 7, 5],
    ...                    [6, 2, 4, 8, 8],
    ...                    [9, 1, 3, 3, 1],
    ...                    [4, 2, 9, 3, 1]])
    >>> hungarian_algorithm(matrix)
    [(4, 4), (1, 0), (0, 3), (2, 1), (3, 2)]
"""


import numpy as np

def zero_position(matrix: np.ndarray, original_shape: tuple) -> list:
    """Find the optimal assignment from a reduced matrix of zeros.

    :param matrix: reduced cost matrix
    :param original_shape: original shape of the cost matrix
    :return: list of tuples (row_index, column_index) representing assignments
    >>> mat = np.array([[0, 1, 2, 3],
    ...                 [0, 0, 1, 2],
    ...                 [1, 0, 0, 1],
    ...                 [2, 1, 0, 0]])
    >>> zero_position(mat, (4,4))
    [(0, 0), (1, 1), (2, 2), (3, 3)]
    """
    n = matrix.shape[0]
    zeros = (matrix == 0)

    rows = set()
    cols = set()
    zero_pos = []
    while len(zero_pos) < n:
        min_alt = n + 1
        best_pos = None
        for i in range(n):
            if i in rows:
                continue
            for j in range(n):
                if j in cols:
                    continue
                if zeros[i, j]:
                    alt = np.sum(zeros[i, :]) - len([c for c in cols if zeros[i, c]])
                    if alt < min_alt:
                        min_alt = alt
                        best_pos = (i, j)
        if best_pos is None:
            break
        i, j = best_pos
        if i < original_shape[0] and j < original_shape[1]:
            zero_pos.append((i, j))
        rows.add(i)
        cols.add(j)

    return zero_pos

def min_lines(matrix: np.ndarray) -> int:
    """Find the minimum number of lines needed to cover all zeros.

    :param matrix: reduced cost matrix
    :return: integer, number of lines covering all zeros
    >>> mat = np.array([[0, 1, 2, 3],
    ...                 [0, 0, 1, 2],
    ...                 [1, 0, 0, 1],
    ...                 [2, 1, 0, 0]])
    >>> int(min_lines(mat))
    4
    """
    n = matrix.shape[0]
    zeros = (matrix == 0)
    row_zeros = np.sum(zeros, axis=1)
    col_zeros = np.sum(zeros, axis=0)
    covered_rows = np.zeros(n, dtype=bool)
    covered_cols = np.zeros(n, dtype=bool)

    while True:
        uncovered_zeros = zeros.copy()
        uncovered_zeros[covered_rows, :] = False
        uncovered_zeros[:, covered_cols] = False

        if not np.any(uncovered_zeros):
            break

        row_counts = np.sum(uncovered_zeros, axis=1)
        col_counts = np.sum(uncovered_zeros, axis=0)

        max_row = np.max(row_counts)
        max_col = np.max(col_counts)

        if max_row >= max_col:
            row_idx = np.argmax(row_counts)
            covered_rows[row_idx] = True
        else:
            col_idx = np.argmax(col_counts)
            covered_cols[col_idx] = True

    return np.sum(covered_rows) + np.sum(covered_cols)


def rows_cols(matrix):
    """
    Determine which rows and columns are covered in current zero configuration.є

    :param matrix: reduced cost matrix
    :return: tuple of two boolean arrays (rows_covered, cols_covered)
    >>> mat = np.array([[0, 1, 2, 3],
    ...                 [0, 0, 1, 2],
    ...                 [1, 0, 0, 1],
    ...                 [2, 1, 0, 0]])
    >>> rows_cols(mat)
    (array([ True,  True,  True,  True]), array([False, False, False, False]))
    """
    n = matrix.shape[0]
    zeros = (matrix == 0)
    row_zeros = np.sum(zeros, axis=1)
    col_zeros = np.sum(zeros, axis=0)
    covered_rows = np.zeros(n, dtype=bool)
    covered_cols = np.zeros(n, dtype=bool)

    while True:
        uncovered_zeros = zeros.copy()
        uncovered_zeros[covered_rows, :] = False
        uncovered_zeros[:, covered_cols] = False
        if not np.any(uncovered_zeros):
            break
        row_counts = np.sum(uncovered_zeros, axis=1)
        col_counts = np.sum(uncovered_zeros, axis=0)
        max_row = np.max(row_counts)
        max_col = np.max(col_counts)
        if max_row >= max_col:
            row_idx = np.argmax(row_counts)
            covered_rows[row_idx] = True
        else:
            col_idx = np.argmax(col_counts)
            covered_cols[col_idx] = True
    return covered_rows, covered_cols


def smallest_uncovered(matrix):
    """
    Find the smallest value in the matrix not covered by any row or column.

    :param matrix: reduced cost matrix
    :return: float, smallest uncovered element

    >>> mat = np.array([[0, 2, 3, 4],
    ...                 [1, 0, 2, 3],
    ...                 [2, 1, 1, 0],
    ...                 [3, 2, 1, 0]])
    >>> int(smallest_uncovered(mat))
    1
    """
    row, col = rows_cols(matrix)
    n = matrix.shape[0]
    smallest = np.inf
    for i in range(n):
        for j in range(n):
            if not row[i] and not col[j]:
                smallest = min(smallest, matrix[i, j])

    return smallest


def hungarian_algorithm(matrix):
    """
    Function takes a cost matrix and returns the optimal assignments that minimize the total cost.
    If multiple assignments have equal minimal cost, the function returns one valid optimal list.
    Rows represent recipients, columns represent donors.

    :param matrix: list of lists with numeric cost values (rows = recipients, columns = donors)
    :return: list of tuples (row_index, column_index) representing optimal assignments

    >>> mat = np.array([[4, 1, 3, 2],
    ...                 [2, 0, 5, 3],
    ...                 [3, 2, 2, 3],
    ...                 [4, 3, 1, 2]])
    >>> hungarian_algorithm(mat)
    [(1, 1), (0, 3), (3, 2), (2, 0)]
    """
    matrix = matrix.copy().astype(float)
    n = matrix.shape[0]
    for i in range(n):
        matrix[i] -= np.min(matrix[i])
    for j in range(n):
        matrix[:, j] -= np.min(matrix[:, j])
    while True:
        lines = min_lines(matrix)
        if lines >= n:
            break
        smallest = smallest_uncovered(matrix)
        row, col = rows_cols(matrix)
        for i in range(n):
            for j in range(n):
                if not row[i] and not col[j]:
                    matrix[i, j] -= smallest
                elif row[i] and col[j]:
                    matrix[i, j] += smallest

    zeros =  zero_position(matrix, matrix.shape)
    return zeros
