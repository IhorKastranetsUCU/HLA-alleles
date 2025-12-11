import random

LOCUS_LIST = ["A", "B", "DR"]
VALID_ALLELES = {
    "A": [
        "01", "02", "03", "11", "23", "24", "25", "26", "29", "30",
        "31", "32", "33", "68"
    ],

    "B": [
        "07", "08", "13", "14", "15", "18", "27", "35", "37", "38",
        "39", "40", "41", "44", "49", "50", "51", "52", "53", "55",
        "57", "58"
    ],

    "DR": [
        "01", "03", "04", "07", "08", "11", "12", "13",
        "14", "15", "16"
    ]
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
  '''
  generates persons alleles
  '''
    person_alleles = set()
    for locus in LOCUS_LIST:
        for i in range(2):
            if i != 1 or random.random() >= homozygosity_rate:
                group = random.choice(VALID_ALLELES[locus])
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
