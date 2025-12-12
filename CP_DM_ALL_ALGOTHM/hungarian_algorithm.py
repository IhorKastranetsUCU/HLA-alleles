"""
This file includes 1 main function "hungarian_algorithm" and additional.
The function takes Numpy matrix and unsorted returns the list of tuples
where the first element is row and second is column
Example:
    >>> import numpy as np
    >>> mat = np.array([[0.7, 0.2, 0.3, 0.4],
    ...                 [0.1, 0.6, 0.2, 0.3],
    ...                 [0.2, 0.1, 0.1, 0.6],
    ...                 [0.3, 0.2, 0.1, 0.8]],)
    >>> hungarian_algorithm(mat, 0.1)
    [(3, 2), (1, 0), (0, 3), (2, 1)]
"""

import numpy as np

def reshaping(matrix, min_match):
    rows, cols = matrix.shape
    if rows > cols:
        return None

    if rows < cols:
        extra_rows = cols - rows
        new_rows = np.full((extra_rows, cols), np.inf)
        matrix = np.vstack([matrix, new_rows])
    else:
        matrix = matrix.copy()
    matrix[matrix > 1 - min_match] = np.inf

    return matrix


def zero_position(matrix: np.ndarray, original_shape: tuple) -> list:
    """Find the optimal assignment from a reduced matrix of zeros.

    :param matrix: reduced cost matrix
    :param original_shape: original shape of the cost matrix
    :return: list of tuples (row_index, column_index) representing assignments
    >>> mat = np.array([[0.0, 0.3, 0.4, 0.5],
    ...                 [0.2, 0.0, 0.4, 0.3],
    ...                 [0.3, 0.4, 0.0, 0.2],
    ...                 [0.5, 0.3, 0.2, 0.0]])
    >>> zero_position(mat, (4,4))
    [(0, 0), (1, 1), (2, 2), (3, 3)]
    """
    R, C = matrix.shape
    zeros = np.isclose(matrix, 0)
    rows_zero = np.zeros(R, dtype=bool)
    cols_zero = np.zeros(C, dtype=bool)
    zero_pos = []

    while True:
        num_new_assignments = 0

        for i in range(R):
            if not rows_zero[i]:
                unassigned_zeros_in_row = np.where(zeros[i, :] & ~cols_zero)[0]

                if len(unassigned_zeros_in_row) == 1:
                    j = unassigned_zeros_in_row[0]

                    rows_zero[i] = True
                    cols_zero[j] = True
                    zero_pos.append((i, j))
                    num_new_assignments += 1

        for j in range(C):
            if not cols_zero[j]:
                unassigned_zeros_in_col = np.where(zeros[:, j] & ~rows_zero)[0]

                if len(unassigned_zeros_in_col) == 1:
                    i = unassigned_zeros_in_col[0]

                    rows_zero[i] = True
                    cols_zero[j] = True
                    zero_pos.append((i, j))
                    num_new_assignments += 1
        if num_new_assignments == 0:
            break
    unassigned_zeros = np.argwhere(zeros & ~np.outer(rows_zero, cols_zero))
    for i, j in unassigned_zeros:
        if not rows_zero[i] and not cols_zero[j]:
            rows_zero[i] = True
            cols_zero[j] = True
            zero_pos.append((i, j))

    final_zero_pos = []
    original_R, original_C = original_shape

    for i, j in zero_pos:
        if i < original_R and j < original_C:
            final_zero_pos.append((int(i), int(j)))
    return final_zero_pos


def min_lines(matrix: np.ndarray) -> int:
    """Find the minimum number of lines needed to cover all zeros.

    :param matrix: reduced cost matrix
    :return: integer, number of lines covering all zeros
    >>> mat = np.array([[0.0, 0.2, 0.3, 0.4],
    ...                 [0.1, 0.6, 0.0, 0.3],
    ...                 [0.0, 0.1, 0.1, 0.6],
    ...                 [0.3, 0.2, 0.0, 0.0]],)
    >>> int(min_lines(mat))
    3
    """
    n = matrix.shape[0]
    zeros = (matrix == 0)
    row_zeros = np.sum(zeros, axis=1)
    col_zeros = np.sum(zeros, axis=0)
    rows = np.zeros(n, dtype=bool)
    cols = np.zeros(n, dtype=bool)

    while True:
        uncovered_zeros = zeros.copy()
        uncovered_zeros[rows, :] = False
        uncovered_zeros[:, cols] = False

        if not np.any(uncovered_zeros):
            break

        row_counts = np.sum(uncovered_zeros, axis=1)
        col_counts = np.sum(uncovered_zeros, axis=0)

        max_row = np.max(row_counts)
        max_col = np.max(col_counts)

        if max_row >= max_col:
            row_idx = np.argmax(row_counts)
            rows[row_idx] = True
        else:
            col_idx = np.argmax(col_counts)
            cols[col_idx] = True

    return np.sum(rows) + np.sum(cols)


def rows_cols(matrix):
    """
    Determine which rows and columns are covered in current zero configuration.є

    :param matrix: reduced cost matrix
    :return: tuple of two boolean arrays (rows_covered, cols_covered)
    >>> mat = np.array([[0.7, 0.2, 0.3, 0.0],
    ...                 [0.1, 0.0, 0.0, 0.3],
    ...                 [0.2, 0.1, 0.1, 0.0],
    ...                 [0.3, 0.2, 0.1, 0.8]],)
    >>> rows_cols(mat)
    (array([False,  True, False, False]), array([False, False, False,  True]))
    """
    n = matrix.shape[0]
    zeros = (matrix == 0)
    row_zeros = np.sum(zeros, axis=1)
    col_zeros = np.sum(zeros, axis=0)
    rows = np.zeros(n, dtype=bool)
    cols = np.zeros(n, dtype=bool)

    while True:
        uncovered_zeros = zeros.copy()
        uncovered_zeros[rows, :] = False
        uncovered_zeros[:, cols] = False
        if not np.any(uncovered_zeros):
            break
        row_counts = np.sum(uncovered_zeros, axis=1)
        col_counts = np.sum(uncovered_zeros, axis=0)
        max_row = np.max(row_counts)
        max_col = np.max(col_counts)
        if max_row >= max_col:
            row_idx = np.argmax(row_counts)
            rows[row_idx] = True
        else:
            col_idx = np.argmax(col_counts)
            cols[col_idx] = True
    return rows, cols


def smallest_uncovered(matrix):
    """
    Find the smallest value in the matrix not covered by any row or column.

    :param matrix: reduced cost matrix
    :return: float, smallest uncovered element

    >>> mat = np.array([[0.0, 0.2, 0.3, 0.4],
    ...                 [0.1, 0.6, 0.0, 0.3],
    ...                 [0.0, 0.1, 0.0, 0.6],
    ...                 [0.3, 0.2, 0.1, 0.8]])
    >>> float(smallest_uncovered(mat))
    0.1
    >>> mat = np.array([[0.0, 0.2, 0.3, 0.4],
    ...                 [0.1, 0.6, 0.0, 0.3],
    ...                 [0.0, 0.7, 0.0, 0.6],
    ...                 [0.3, 0.2, 0.0, 0.8]])
    >>> float(smallest_uncovered(mat))
    0.2
    """
    n = matrix.shape[0]
    rows, cols = rows_cols(matrix)

    smallests = []
    for i in range(n):
        for j in range(n):
            if not rows[i] and not cols[j] and np.isfinite(matrix[i, j]):
                smallests.append(matrix[i][j])
    return min(smallests)


def hungarian_algorithm(matrix, min_match):
    """
    Function takes a cost matrix and returns the optimal assignments that minimize the total cost.
    If multiple assignments have equal minimal cost, the function returns one valid optimal list.
    Rows represent recipients, columns represent donors.

    :param matrix: list of lists with numeric cost values (rows = recipients, columns = donors)
    :return: list of tuples (row_index, column_index) representing optimal assignments

    >>> mat = np.array([[0.7, 0.2, 0.3, 0.4],
    ...                 [0.1, 0.6, 0.2, 0.3],
    ...                 [0.2, 0.1, 0.1, 0.6],
    ...                 [0.3, 0.2, 0.1, 0.8]],)
    >>> hungarian_algorithm(mat, 0.1)
    [(3, 2), (1, 0), (0, 3), (2, 1)]
    """
    orig_shape = matrix.shape
    matrix = reshaping(matrix.copy().astype(float), min_match)
    if matrix is None:
        return None
    n = matrix.shape[0]


    for i in range(n):
        if not np.all(np.isinf(matrix[i])):
            matrix[i] -= np.nanmin(matrix[i])
    for j in range(n):
        if not np.all(np.isinf(matrix[:, j])):
            matrix[:, j] -= np.nanmin(matrix[:, j])

    max_iterations = n * 5
    it = 0
    while True:
        lines = min_lines(matrix)
        if lines >= n:
            break

        smallest = smallest_uncovered(matrix)
        if not np.isfinite(smallest) or np.isinf(smallest):
            break

        row, col = rows_cols(matrix)
        for i in range(n):
            for j in range(n):
                if np.isinf(matrix[i, j]):
                    continue
                if not row[i] and not col[j]:
                    matrix[i, j] -= smallest
                elif row[i] and col[j]:
                    matrix[i, j] += smallest

        it += 1
        if it >= max_iterations:
            break

    zeros = zero_position(matrix, orig_shape)
    return zeros
