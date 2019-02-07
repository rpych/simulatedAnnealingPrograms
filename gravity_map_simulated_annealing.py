from random import randint, random, uniform
import math
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col


def probability_function(x_old, x_new, temp):
    ans = math.exp(((x_old - x_new)) / temp)
    return ans


def is_in_circle(x, y ,r, n):
    x0 = n // 2
    y0 = x0
    x_diff = x - x0
    y_diff = y - y0
    return (x_diff*x_diff + y_diff*y_diff) < (r*r)


def generate_colors():
    colors_values = {"blue": (0.50), "green": (0.75), "yellow": (1.), "red": (1.25)}
    return colors_values


def generate_color_map(colors, n, points_num):
    r = n // 2
    color_map = [[] for e in range(n)]
    for i in range(n):
        color_map[i] = ["empty" for e in range(n)]

    for p in range(points_num):
        x = randint(0, n-1)
        y = randint(0, n-1)
        while color_map[y][x] != "empty":  # or (not is_in_circle(x, y, r, n))
            x = randint(0, n - 1)
            y = randint(0, n - 1)
        color_map[y][x] = colors[randint(0, 3)]

    return color_map


def change_state(A, y1, x1, y2, x2):
    temp = A[y1][x1]
    A[y1][x1] = A[y2][x2]
    A[y2][x2] = temp

    return A


def get_point_energy(A, color, colors_values, y, x, n):
    # middle of circle inserted in square NxN
    x0 = n // 2
    y0 = x0
    color_val = colors_values[color]
    y_diff = y - y0
    x_diff = x - x0
    return (y_diff * y_diff + x_diff * x_diff) * color_val


def get_initial_energy(A, colors_values, n):
    energy = 0.0
    for i in range(n):
        for j in range(n):
            if A[i][j] != "empty":
                energy += get_point_energy(A, A[i][j], colors_values, i, j, n)

    return energy


def energy_function(A, colors_values, y1, x1, y2, x2, min_energy, n):
    # subtract old point_energy values
    min_energy -= (get_point_energy(A, A[y2][x2], colors_values, y1, x1, n)
                   + get_point_energy(A, A[y1][x1], colors_values, y2, x2, n))

    # calculate new point_energy values
    min_energy += (get_point_energy(A, A[y1][x1], colors_values, y1, x1, n)
                   + get_point_energy(A, A[y2][x2], colors_values, y2, x2, n))

    return min_energy


def simulated_annealing(A, colors_values, n):
    temp = 0.45 #0.65
    coef = 0.00001
    steps = 0
    min_cost = get_initial_energy(A, colors_values, n)
    min_perm = A
    while min_cost != 0:
        print("Steps = ", steps, ", min_energy = ", min_cost)
        copied_A = copy.deepcopy(A)
        while True:
            x1 = randint(0, n - 1)
            y1 = randint(0, n - 1)
            x2 = randint(0, n - 1)
            y2 = randint(0, n - 1)
            if x1 == x2 and y1 == y2:
                continue
            elif copied_A[y1][x1] == "empty" or copied_A[y2][x2] == "empty":
                continue
            else:
                break

        changed = change_state(copied_A, y1, x1, y2, x2)
        curr_cost = energy_function(changed, colors_values, y1, x1, y2, x2, min_cost, n)
        if curr_cost < min_cost:
            min_cost = curr_cost
            A = changed
            min_perm = A
        else:
            if uniform(0.0, 1.0) < probability_function(min_cost, curr_cost, temp):
                min_cost = curr_cost
                A = changed
                min_perm = A


        steps += 1
        if temp >= 0.17:
            temp -= coef
        else:
            break

    print("Minimal cost = ", min_cost)
    return min_perm


def get_points_for_plot(A, colors_dict, n):
    x = []
    y = []
    colors = []
    for i in range(n):
        for j in range(n):
            if A[i][j] != "empty":
                c = colors_dict[A[i][j]]
                colors.append(c)
                x.append(j)
                y.append(i)

    return x, y, colors


def main():

    n = 20
    colors1 = ["blue", "green", "yellow", "red"]
    color_map = generate_color_map(colors1, n, 150)
    colors_values = generate_colors()
    for i in range(n):
        print(color_map[i])

    colors_dict = {"blue": 'b', "green": 'g', "yellow": 'y', "red": 'r'}

    print("*********************** Simulated annealing Pt. 1 **************************", end="\n\n")

    x, y, colors = get_points_for_plot(color_map, colors_dict, n)
    print("x = ", x)
    print("y = ", y)
    print("colors = ", colors)

    f = plt.figure()
    f, axes = plt.subplots(nrows=2, ncols=2)
    norm = plt.Normalize(-22, 22)
    sc = axes[0][0].scatter(x, y, c=colors, marker="s", norm=norm)
    axes[0][0].set_xlabel('First Map', labelpad=5)

    solution = simulated_annealing(color_map, colors_values, n)
    x, y, colors = get_points_for_plot(solution, colors_dict, n)
    print("x = ", x)
    print("y = ", y)
    print("colors = ", colors)

    axes[1][0].scatter(x, y, c=colors, marker='s', norm=norm)
    axes[1][0].set_xlabel('First Map', labelpad=5)

    print("*********************** Simulated annealing Pt. 2 **************************", end="\n\n")
    n = 18
    color_map = generate_color_map(colors1, n, 225)
    x, y, colors = get_points_for_plot(color_map, colors_dict, n)
    print("x = ", x)
    print("y = ", y)
    print("colors = ", colors)

    axes[0][1].scatter(x, y, c=colors, marker='o', norm=norm)
    axes[0][1].set_xlabel('Second Map')

    solution = simulated_annealing(color_map, colors_values, n)
    x, y, colors = get_points_for_plot(solution, colors_dict, n)
    print("x = ", x)
    print("y = ", y)
    print("colors = ", colors)

    axes[1][1].scatter(x, y, c=colors, marker='o', norm=norm)
    axes[1][1].set_xlabel('Second Map')

    plt.show()





if __name__ == '__main__':
    main()