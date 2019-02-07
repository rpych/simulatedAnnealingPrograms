from random import randint, random, uniform
import math
import itertools
import copy


def generate_non_fixed_rows_numbers(A, n):
    for i in range(n):
        present = []
        for j in range(n):
            if A[i][j] > 0:
                present.append(A[i][j])

        for j in range(n):
            if A[i][j] > 0:
                continue
            else:
                for num in range(1, 10):
                    if num not in present:
                        A[i][j] = num
                        present.append(num)
                        break

    return A


def mark_fixed_values(A, n):
    #creating matrix
    bit_map = [[] for el in range(9)]
    for i in range(len(bit_map)):
        bit_map[i] = [0 for e in range(9)]

    for i in range(n):
        for j in range(n):
            if A[i][j] > 0:
                bit_map[i][j] = 1

    return bit_map


def cost_function(A, n):
    # for row
    non_present_values = 0
    for i in range(n):
        row = A[i]
        for num in range(1, 10):
            if num not in row:
                non_present_values += 1
    # for column
    for i in range(9):
        column = []
        for j in range(9):
            column.append(A[j][i])
        for num in range(1, 10):
            if num not in column:
                non_present_values += 1

    # for every small-square
    for i in range(3):
        for j in range(3):
            present = []
            for k in range(3 * i, 3 * i + 3):
                for l in range(3 * j, 3 * j + 3):
                    present.append(A[k][l])
            for num in range(1, 10):
                if num not in present:
                    non_present_values += 1

    return non_present_values


def change_random_row(A, bit_mask, row):
    while True:
        x1 = randint(0, 8)
        x2 = randint(0, 8)
        if x1 == x2:
            continue
        elif bit_mask[row][x1] == 1 or bit_mask[row][x2] == 1:
            continue
        else:
            temp = A[row][x1]
            A[row][x1] = A[row][x2]
            A[row][x2] = temp
            break

    return A


def is_change_possible(A, bit_mask, row, n):
    non_fixed = 0
    for i in range(n):
        if bit_mask[row][i] == 0:
            non_fixed += 1

    return non_fixed >= 2


def probability_function(x_old, x_new, temp):
    ans = math.exp(((x_old - x_new)) / temp)
    return ans


def simulated_annealing(A, bit_mask, n):
    temp = 0.45 #0.65
    coef = 0.00001
    steps = 0
    min_cost = cost_function(A, n)
    min_perm = A
    while min_cost != 0:
        print("Steps = ", steps, ", min_cost = ", min_cost)
        x = randint(0, 8)
        if not is_change_possible(A, bit_mask, x, n):
            continue
        copied_A = copy.deepcopy(A)
        changed = change_random_row(copied_A, bit_mask, x)
        curr_cost = cost_function(changed, n)
        if curr_cost < min_cost:
            min_cost = curr_cost
            A = changed
            min_perm = A
        else:
            if uniform(0.0, 1.0) < probability_function(min_cost, curr_cost, temp):
                min_cost = curr_cost
                A = changed
                min_perm = A

        if min_cost == 0:
            break
        steps += 1


    print("Minimal cost = ", min_cost)
    return min_perm



def main():
    n = 9
    A = [[5,3,0,0,7,0,0,0,0], [6,0,0,1,9,5,0,0,0], [0,9,8,0,0,0,0,6,0],
         [8,0,0,0,6,0,0,0,3], [4,0,0,8,0,3,0,0,1], [7,0,0,0,2,0,0,0,6],
         [0,6,0,0,0,0,2,8,0], [0,0,0,4,1,9,0,0,5], [0,0,0,0,8,0,0,7,9]]
    B = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    bit_map = mark_fixed_values(A, n)
    print("bit_map = \n", bit_map, end="\n\n")

    A = generate_non_fixed_rows_numbers(A, 9)
    for i in range(9):
        for j in range(9):
            print(A[i][j], end=" ")
        print("\n")

    '''bit_map = mark_fixed_values(B, n)
    print("bit_map = \n", bit_map, end="\n\n")
    B = generate_non_fixed_rows_numbers(B, 9)
    for i in range(9):
        for j in range(9):
            print(B[i][j], end=" ")
        print("\n")'''

    print("*********************** Simulated annealing **************************", end="\n\n")


    solution = simulated_annealing(A, bit_map, n)
    print("\n\n")
    for i in range(9):
        for j in range(9):
            print(solution[i][j], end=" ")
        print("\n")

    '''solution = simulated_annealing(B, bit_map, n)

    for i in range(9):
        for j in range(9):
            print(solution[i][j], end=" ")
        print("\n")'''




if __name__ == '__main__':
    main()
