from random import randint, random
import math
import itertools
import copy

# problem of travelling salesman


def generate_points(n, start, end):
    points = []
    for i in range(n):
        x = randint(start, end)
        y = randint(start, end)
        points.append((x, y))
    return points


def distance_function(A, n):
    dist = 0.0
    for i in range(n-1):
        x_diff = A[i+1][0] - A[i][0]
        y_diff = A[i+1][1] - A[i][1]
        dist += math.sqrt((x_diff * x_diff) + (y_diff * y_diff))

    # link between last and first point
    x_diff = A[0][0] - A[n-1][0]
    y_diff = A[0][1] - A[n-1][1]
    dist += math.sqrt((x_diff * x_diff) + (y_diff * y_diff))
    return dist


def basic_solution(A, n):
    min_dist = 10e4
    min_perm = []

    for p in itertools.permutations(A):
        curr_dist = distance_function(p, n)
        if curr_dist < min_dist:
            min_dist = curr_dist
            min_perm = p
    print("Minimal distance = ", min_dist)
    return min_perm


def probability_function(x_old, x_new, temp):
    ans = math.exp(((x_old - x_new)) / temp)
    return ans


def simulated_annealing(A, n):
    temp = 10000
    coef = 0.9999
    min_dist = distance_function(A, n)
    st = min_dist
    min_perm = A
    steps = 0
    while temp > 1:
        print("Steps = ", steps, ", min_dist = ", min_dist)
        x1 = randint(0, n-1)
        x2 = randint(0, n-1)
        if x1 == x2:
            continue
        changed = copy.deepcopy(A)
        changed[x1], changed[x2] = changed[x2], changed[x1]
        curr_dist = distance_function(changed, n)
        if curr_dist < min_dist:
            min_dist = curr_dist
            A = changed
            min_perm = A
        else:
            if 0.6 < probability_function(min_dist, curr_dist, temp):
                min_dist = curr_dist
                A = changed
                min_perm = A
        steps += 1
        temp *= coef

    print("Minimal distance = ", min_dist, "st = ", st)
    return min_perm


def main():
    n = 100
    A = generate_points(n, -10, 20)
    print("A = \n", A, end='\n\n')
    print("*********************** Simulated annealing **************************", end="\n\n")
    print("Cities with minimal distance = ", simulated_annealing(A, n))
    print("\n\n*********************** Basic solution **************************", end="\n\n")
    #print("Cities with minimal distance = ", basic_solution(A, n), end="\n\n")




if __name__ == '__main__':
    main()


