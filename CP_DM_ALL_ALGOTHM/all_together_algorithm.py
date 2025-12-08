
from generate_data import generate_database
from compatibility_rating import compatibility_rating
from hungarian_algorithm import hungarian_algorithm
LOCUS_LIST = ['A', 'B', 'C']
MAX_GROUP = 20
MAX_SPEC_PROT = 5

def main():
    try:
        recipients = int(input("Recipients (number): "))
        donors = int(input("Donors (number): "))
    except ValueError:
        print("Please enter integer numbers.")
        return

    if recipients > donors:
        print("Warning: recipients > donors. generate_database у даній реалізації поверне (None, None).")
    donors_list = generate_database(recipients, donors, True)
    recipients_list = generate_database(recipients, donors, False, True)

    if donors_list is None or recipients_list is None:
        print("Database generation failed (None returned). Перевір параметри.")
        return

    grade_compatibility = compatibility_rating(recipients_list, donors_list)  # опціонально
    cost_matrix = compatibility_rating(recipients_list, donors_list, cost_matrix=True)
    print(cost_matrix)


    assignment = hungarian_algorithm(cost_matrix)
    print("Assignment:", assignment)

if __name__ == "__main__":
    main()
