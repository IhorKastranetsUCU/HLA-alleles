import argparse
import pandas as pd
import matplotlib.pyplot as plt
from generating_alleles import generate_database
from CP_DM_ALL_ALGOTHM.get_real_data import get_data_from_csv
from hungarian_algorithm import hungarian_algorithm
from cost_matrix import cost_matrix

def main(donor_file, recipient_file, min_match, use_random):
    if use_random:
        num_recipients = int(input("Кількість рецепієнтів: "))
        num_donors = int(input("Кількість донорів: "))

        donors = generate_database(num_recipients, num_donors, donor=True)
        recipients = generate_database(num_recipients, num_donors, recipient=True)
    else:
        donors = get_data_from_csv(donor_file)
        recipients = get_data_from_csv(recipient_file)
    first_matrix = cost_matrix(recipients, donors)
    death = []
    for i, v_1 in enumerate(first_matrix):
        for j, v_2 in enumerate(v_1):
            if v_2 > min_match:
               death.append((i,j))
    try:
        assignment = hungarian_algorithm(first_matrix, min_match)
    except AttributeError:
        return "Кількість рецепієнтів не повинно перевищувати кількість донорів"
    print("")
    recipients_set = sorted(set(r for r, d in assignment))
    donors_set = sorted(set(d for r, d in assignment))
    matrix = []
    count_d = 0
    count_t = 0
    count_c = 0
    for r in recipients_set:
        row = []
        for d in donors_set:
            if (r, d) in assignment:
                row.append(f"{'✅':^7}")
                count_t += 1
            elif (r, d) in death:
                row.append(f"{'💀':^7}")
                count_d += 1
            else:
                row.append(f"{'❌':^7}")
                count_c += 1
        matrix.append(row)
    if len(recipients_set) <= 12:
        print("               " + "   ".join(f"Донор {d + 1}" for d in donors_set))
        for i, r in enumerate(recipients_set):
            print(f"Рецепієнт {r + 1}   " + "  ".join(matrix[i]))
    else:
        df = pd.DataFrame(matrix, columns=[f"Дон. {d+1}" for d in donors_set], index=[f"Рец. {r+1} "for i, r in enumerate(recipients_set)])
        df.to_excel("results.xlsx", index=True)
        print("Таблиця збережена у results.xlsx")
    total = count_t + count_d + count_c
    print("\nСтатистика збігів:")
    print(f"  ✅ Успішні збіги: {count_t} ({count_t/total*100:.1f}%)")
    print(f"  💀 Несумісні пари: {count_d} ({count_d/total*100:.1f}%)")
    print(f"  ❌ Невідповідність: {count_c} ({count_c/total*100:.1f}%)")
    if len(recipients_set) <= 30:
        x_rec = [0] * len(recipients_set)
        y_rec = list(range(len(recipients_set)))
        x_don = [2] * len(donors_set)
        y_don = list(range(len(donors_set)))
        plt.figure(figsize=(8,5))
        plt.scatter(x_rec, y_rec, color='skyblue', s=200, label="Реципієнти")
        plt.scatter(x_don, y_don, color='lightgreen', s=200, label="Донори")
        for i, r in enumerate(recipients_set):
            plt.text(x_rec[i]-0.1, y_rec[i], f"R{r+1}", fontsize=12, ha='right', va='center')
        for i, d in enumerate(donors_set):
            plt.text(x_don[i]+0.1, y_don[i], f"D{d+1}", fontsize=12, ha='left', va='center')
        for r, d in assignment:
            if r in recipients_set and d in donors_set:
                plt.plot([x_rec[recipients_set.index(r)], x_don[donors_set.index(d)]],
                        [y_rec[recipients_set.index(r)], y_don[donors_set.index(d)]],
                        color='green', linewidth=2)
                plt.scatter(x_don[donors_set.index(d)], y_don[donors_set.index(d)], color='green', s=100, marker='o')
        if len(recipients_set) <= 10:
            for r in recipients_set:
                for d in donors_set:
                    if (r,d) not in assignment and (r,d) not in death:
                        plt.plot([x_rec[recipients_set.index(r)], x_don[donors_set.index(d)]],
                                [y_rec[recipients_set.index(r)], y_don[donors_set.index(d)]],
                                color='black', linewidth=1, linestyle='--')
                        plt.scatter(x_don[donors_set.index(d)], y_don[donors_set.index(d)], color='black', s=50, marker='x')
        plt.axis('off')
        plt.title("Інтерпретація 'теореми Холла'")
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Алгоритм для обробки двох файлів")

    parser.add_argument('--donor_file', type=str, required=True, help="Файл з донорами")
    parser.add_argument('--recipient_file', type=str, required=True, help="Файл з рецепієнтами")
    parser.add_argument('--min_match', type=float, required=True, help="Поріг збіжності")
    parser.add_argument('--random', action='store_true', help="Генерувати випадкові дані")
    args = parser.parse_args()
    main(args.donor_file, args.recipient_file, args.min_match, args.random)
