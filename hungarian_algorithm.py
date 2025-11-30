from copy import deepcopy


def reducing(matrix: list[list]) -> list[list]:
    """
    Reduce the matrix by subtracting the row minima and then the column minima.

    :param matrix: list of lists with numeric cost values
    :return: reduced matrix
    """
    size = len(matrix)

    # Subtract row minima
    for i, row in enumerate(matrix):
        min_val = min(row)
        for j in range(len(row)):
            matrix[i][j] -= min_val

    # Subtract column minima
    for j in range(size):
        min_val = min(matrix[i][j] for i in range(size))
        for i in range(size):
            matrix[i][j] -= min_val

    return matrix

def zero_positions(matrix: list[list]) -> list:
    """

    :param matrix:
    :return:
    """
    size = len(matrix)

    row_zeros = set()
    col_zeros = set()
    visited = {"row": set(), "col": set()}

    for i, row in enumerate(matrix):
        if row.count(0) == 1:
            if i not in visited["row"] and row.index(0) not in visited["col"]:
                row_zeros.add((i, row.index(0)))
                visited["row"].add(i)
                visited["col"].add(row.index(0))

    for col in range(size):
        col_vals = [matrix[row][col] for row in range(size)]
        if col_vals.count(0) == 1:
            if col_vals.index(0) not in visited["row"] and col not in visited["col"]:
                col_zeros.add((col_vals.index(0), col))
                visited["row"].add(col_vals.index(0))
                visited["col"].add(col)

    return list(col_zeros | row_zeros)

print(zero_positions([[0, 6, 0, 3], [13, 0, 5, 4], [4, 3, 0, 0], [0, 9, 2, 13]]))


def changing(matrix):
    origin_matrix = deepcopy(matrix)
    selected_rows = []
    selected_cols = []

    while any(0 in row for row in matrix):
        row_zeros = {i: row.count(0) for i, row in enumerate(matrix)}
        col_zeros = {j: [matrix[i][j] for i in range(len(matrix))].count(0) for j in range(len(matrix[0]))}

        max_zero_row = max(row_zeros.values()) if row_zeros else 0
        max_zero_col = max(col_zeros.values()) if col_zeros else 0

        if max_zero_row >= max_zero_col:
            rows_to_remove = [i for i, count in row_zeros.items() if count == max_zero_row]
            for i in sorted(rows_to_remove, reverse=True):
                matrix.pop(i)
                selected_rows.append(i)
        else:
            cols_to_remove = [j for j, count in col_zeros.items() if count == max_zero_col]
            for j in sorted(cols_to_remove, reverse=True):
                for row in matrix:
                    row.pop(j)
                selected_cols.append(j)

    min_el = min(min(row) for row in matrix)
    for i, row in enumerate(origin_matrix):
        for j in range(len(row)):
            if i in selected_rows and j in selected_cols:
                origin_matrix[i][j] += min_el
            elif i in selected_rows or j in selected_cols:
                pass
            else:
                origin_matrix[i][j] -= min_el

    return origin_matrix


def hungarian_algorith(matrix: list[list]) -> int:
    """
    Function takes a cost matrix and returns the optimal assignments that minimize the total cost.
    If multiple assignments have equal minimal cost, the function returns one valid optimal list.
    Rows represent recipients, columns represent donors.

    :param matrix: list of lists with numeric cost values (rows = recipients, columns = donors)
    :return: list of tuples (row_index, column_index) representing optimal assignments
    """
    reduced_matric = reducing(matrix)
    size = len(matrix)
    print(zero_positions(reduced_matric))
    print(reduced_matric)
    print(changing(reduced_matric))
    print(zero_positions(changing(reduced_matric)))

hungarian_algorith([[2, 10, 9, 7], [15, 4, 14, 8], [13, 14, 16, 11], [4, 15, 13, 19]])