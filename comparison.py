import time
from sys import setrecursionlimit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from quadtree import Quadtree
from kd_tree import KdTree
from geometry import Rectangle

setrecursionlimit(100000)
plt.style.use('bmh')


def get_small_rectangle():
    x = np.random.uniform(-1000, 980)
    y = np.random.uniform(-1000, 980)
    return Rectangle(x, x + 20, y, y + 20)


def get_big_rectangle():
    x = np.random.uniform(-1000, 0)
    y = np.random.uniform(-1000, 0)
    return Rectangle(x, x + 1000, y, y + 1000)


def print_table(df):
    for n in sorted(list(set(df.n))):
        quad_time = df[(df.n == n) & (df.type == 'quad')].time.mean()
        kd_time = df[(df.n == n) & (df.type == 'kd')].time.mean()
        print(f'{n} & {quad_time:.4f} & {kd_time:.4f} \\\\')

    sns.lineplot(data=df, x='n', y='time', hue='type', errorbar=('se', 1))
    plt.show()


def calculate(distribution, ns):
    construction_times = []
    small_find_times = []
    big_find_times = []

    for n in ns:
        print(n)
        for _ in range(10):
            points = distribution(n)
            small_rectangle = get_small_rectangle()  # 1/100
            big_rectangle = get_big_rectangle()  # 1/4

            start_time = time.process_time()
            tree1 = Quadtree(points)
            construction_times.append([n, 'quad', time.process_time() - start_time])
            start_time = time.process_time()
            tree2 = KdTree(points)
            construction_times.append([n, 'kd', time.process_time() - start_time])

            start_time = time.process_time()
            f1 = tree1.find(small_rectangle)
            small_find_times.append([n, 'quad', time.process_time() - start_time])
            start_time = time.process_time()
            f2 = tree2.find(small_rectangle)
            small_find_times.append([n, 'kd', time.process_time() - start_time])
            assert set(f1) == set(f2)

            start_time = time.process_time()
            f1 = tree1.find(big_rectangle)
            big_find_times.append([n, 'quad', time.process_time() - start_time])
            start_time = time.process_time()
            f2 = tree2.find(big_rectangle)
            big_find_times.append([n, 'kd', time.process_time() - start_time])
            assert set(f1) == set(f2)

    construction_times = pd.DataFrame(construction_times, columns=['n', 'type', 'time'])
    small_find_times = pd.DataFrame(small_find_times, columns=['n', 'type', 'time'])
    big_find_times = pd.DataFrame(big_find_times, columns=['n', 'type', 'time'])

    print_table(construction_times)
    print_table(small_find_times)
    print_table(big_find_times)


def uniformly_distributed_points(n):
    return list(zip(np.random.uniform(-1000, 1000, n), np.random.uniform(-1000, 1000, n)))


def pair_of_points(n):
    points = []
    for _ in range(n // 2):
        x = np.random.uniform(-1000, 1000)
        y = np.random.uniform(-1000, 1000)
        points.append((x, y))
        points.append((x + 1e-10, y))
    return points


calculate(uniformly_distributed_points, (10_000, 25_000, 50_000, 75_000, 100_000))
calculate(pair_of_points, (10_000, 25_000, 50_000, 75_000, 100_000))
