from copy import deepcopy

def hungarian_algorith(matrix: list[list]) -> int:
    """
    Function takes a cost matrix and returns the optimal assignments that minimize the total cost.
    If multiple assignments have equal minimal cost, the function returns one valid optimal list.
    Rows represent recipients, columns represent donors.

    :param matrix: list of lists with numeric cost values (rows = recipients, columns = donors)
    :return: list of tuples (row_index, column_index) representing optimal assignments
    """
    basic_matrix = deepcopy(matrix)
    size = len(matrix)

    for i, recipients in enumerate(matrix):
        min_donor = min(recipients)
        for j, donor in enumerate(recipients):
            matrix[i][j] = donor - min_donor

    for donor in range(size):
        min_recipient = min(matrix[row_index][donor] for row_index in range(size))
        for row_index in range(size):
            matrix[row_index][donor] -= min_recipient

    ...
