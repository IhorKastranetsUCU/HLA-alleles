'''
Module to process real data.
'''
import os


def get_data_from_csv(filename:str):
    '''

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


