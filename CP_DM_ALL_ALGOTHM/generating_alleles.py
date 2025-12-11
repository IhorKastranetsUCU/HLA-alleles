import random

LOCUS_LIST = ["A", "B", "DR"]
homozygosity_rate=0.15

A_ALLELE_WEIGHTS = {
    "02": 350, 
    "01": 180,
    "03": 150,
    "24": 130,
    "11": 90,
    "26": 60,
    "68": 50,
    "29": 40,
    "30": 35,
    "31": 35,
    "32": 35,
    "33": 25,
    "23": 20,
    "25": 20
}

B_ALLELE_WEIGHTS = {
    "07": 160,
    "44": 150,
    "35": 140,
    "08": 130,
    "15": 120,
    "18": 100,
    "51": 80,
    "27": 70,
    "40": 60,
    "57": 50,
    "13": 45,
    "38": 35,
    "39": 35,
    "14": 30,
    "49": 25,
    "50": 25,
    "52": 20,
    "53": 20,
    "55": 20,
    "58": 20,
    "37": 15,
    "41": 15
}

DR_ALLELE_WEIGHTS = {
    "04": 200,
    "15": 190,
    "11": 140,
    "13": 130,
    "07": 120,
    "03": 120,
    "01": 110,
    "08": 60,
    "14": 50,
    "12": 50,
    "16": 30
}

def get_realistic_subtype():
  '''
  make realistic subtype for allele
  '''
    subtypes = [
        "01",               # Домінантний
        "02", "03", "04",   # Дуже часті
        "05", "06", "07",   # Часті
        "08", "09", "10",   # Рідші
        "11", "12", "13"    # Ще рідші, але реальні
    ]

    # Ваги (Weights) - визначають, як часто випадає кожне число.
    # Логіка: :01 випадає дуже часто, :13 - дуже рідко.
    weights = [
        60,                 # 01 - (найбільша вага, ~60% шансу)
        15, 10, 5,          # 02-04
        3, 2, 1,            # 05-07
        1, 0.5, 0.5,        # 08-10
        0.3, 0.3, 0.3       # 11-13 (дуже рідко)
    ]
    chosen_subtype = random.choices(subtypes, weights=weights)[0]
    return chosen_subtype


def generate_person_alleles():
    person_alleles = set()
    for locus in LOCUS_LIST:
        if locus == 'A':
            options = list(A_ALLELE_WEIGHTS.keys())
            chances = list(A_ALLELE_WEIGHTS.values())
        elif locus == 'B':
            options = list(B_ALLELE_WEIGHTS.keys())
            chances = list(B_ALLELE_WEIGHTS.values())
        else:
            options = list(DR_ALLELE_WEIGHTS.keys())
            chances = list(DR_ALLELE_WEIGHTS.values())
        for i in range(2):
            if i != 1 or random.random() >= homozygosity_rate:
                group = random.choices(options, weights=chances)[0]
                spec_prot = get_realistic_subtype()
                allele = f"{locus}*{group:02}:{spec_prot:02}"
                person_alleles.add(allele)
    return person_alleles

def generate_database(recipients: int, donors: int, donor = False, recipient = False):
    if recipients > donors:
        return None, None
    recipients_list = []
    for _ in range(recipients):
        recipients_list.append(generate_person_alleles())
    donors_list = []
    for _ in range(donors):
        donors_list.append(generate_person_alleles())
    if donor:
        return donors_list
    if recipient:
        return recipients_list
    return recipients_list, donors_list
