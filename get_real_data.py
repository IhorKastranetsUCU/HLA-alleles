'''
Module to process real data.
'''
import os


def get_data_from_csv(filename:str) -> list[list[str, str]]:
    '''
    Reads HLA allele data from the specified CSV file and converts it into a matrix.

    The function performs the following actions:
    1. Checks for the presence of the file at the specified path.
    2. Reads the file sequentially, ignoring empty lines.
    3. Splits each line by separator (comma) into separate alleles.
    4. Cleans each allele of extra spaces.

    Args:
    filename (str): Path to the input file (e.g., ‘recipients.csv’).

    Returns:
        list[list[str]]: A list of lists (matrix) where each inner list
                         contains  alleles for one person.
                         Returns an empty list [] if the file is not found.
    >>> with open('test_genes.csv', 'w', encoding='utf-8') as f:
    ...     _ = f.write("A*01:01, A*02:01\\n")
    ...     _ = f.write("\\n")
    ...     _ = f.write("B*07:02,B*44:03")
    >>> result = get_data_from_csv('test_genes.csv')
    >>> result
    [['A*01:01', 'A*02:01'], ['B*07:02', 'B*44:03']]
    >>> get_data_from_csv('ghost_file.csv')
    Помилка: Файл 'ghost_file.csv' не знайдено.
    []
    >>> if os.path.exists('test_genes.csv'):
    ...     os.remove('test_genes.csv')
    '''
    data_matrix = []
    if not os.path.exists(filename):
        print(f"Помилка: Файл '{filename}' не знайдено.")
        return []
    with open(filename, 'r' , encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            alleles_r = line.split(',')
            alleles = [x.strip() for x in alleles_r]
            data_matrix.append(alleles)
    return data_matrix


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
