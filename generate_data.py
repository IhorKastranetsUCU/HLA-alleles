import random
LOCUS_LIST = ['A', 'B', 'C']
MAX_GROUP = 20
MAX_SPEC_PROT = 5


def generate_person_alleles():
  person_alleles = set()
  for locus in LOCUS_LIST:
    count = random.choice([1, 2])
    for _ in range(count):
      group = random.randint(1, MAX_GROUP)
      spec_prot = random.randint(1, MAX_SPEC_PROT)
      allele = f'{locus}*{group:02}:{spec_prot:02}'
      person_alleles.add(allele)
  return person_alleles


def generate_database(recipients: int, donors: int):
  if recipients > donors:
    return None, None
  recipients_list = []
  for _ in range(recipients):
    recipients_list.append(generate_person_alleles())
  donors_list = []
  for _ in range(donors):
    donors_list.append(generate_person_alleles())
  return recipients_list, donors_list
