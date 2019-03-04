import matplotlib
import numpy as np

matplotlib.use('TkAgg')

from matplotlib import pyplot as plt

from copy import deepcopy

plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')


def dist(a, b, ax=1):
    return np.linalg.norm(a - b, axis=ax)


def kmeans_func(X, k):
    ind = np.random.choice(X.shape[0], k, replace=False)
    centroids = X[ind]

    centroids_old = np.zeros(centroids.shape)

    y = np.zeros(len(X))

    error = dist(centroids, centroids_old, None)

    while error != 0:

        for i in range(len(X)):
            distances = dist(X[i], centroids)
            cluster = np.argmin(distances)
            y[i] = cluster

        centroids_old = deepcopy(centroids)

        for i in range(k):
            points = [X[j] for j in range(len(X)) if y[j] == i]
            centroids[i] = np.mean(points, axis=0)

        error = dist(centroids, centroids_old, None)

    return y, centroids


def kmeans_plot(X, y, k, centroids):
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'w', 'k', 'orange', 'navy', 'cyan', 'crimson', 'teal', 'sienna', 'khaki',
              'fuchsia']
    # colors = cm.rainbow(np.linspace(0, 1, len(np.unique(y))))
    fig, ax = plt.subplots()

    for i in range(k):
        points = np.array([X[j] for j in range(len(X)) if y[j] == i])
        ax.scatter(points[:, 0], points[:, 1], s=50, c=colors[i])
        ax.scatter(centroids[i, 0], centroids[i, 1], marker='*', s=300, c=colors[i])

    plt.show(block=False)
