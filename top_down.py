from copy import deepcopy

import numpy as np
from matplotlib import pyplot as plt


def div_func(X):
    clusters = np.zeros([1, len(X)])
    # centroids = np.zeros([1, len(X)])

    # Y = c = None
    for i in range(len(X) - 1):
        # if i == 0:
        #   indexs = np.where(clusters[0] == 0)
        #     else:
        #         for j in np.unique(Y):
        #             indexes = np.where(clusters[i] == j)
        #             #distances = dist(X[indexes], c)
        #             #cluster = np.argmin(distances)
        #         # for j in range(len(y) - 1):
        #         #     print()
        #         #     print(y[j])
        #         #     print(c[j])
        #         #     print()

        counts = np.bincount(clusters[i].astype(int))
        maxcluster = np.argmax(counts)
        ind = np.where(clusters[i] == maxcluster)
        y, c = kmeans_func(X[ind], 2)
        # d = dist(c, centroids_old, None)
        # m = np.max(d)
        Y = deepcopy(clusters[i])
        Y[ind] = y
        Y = Y + 2
        clusters = np.append(clusters, Y.reshape(1, len(Y)), axis=0)

    return clusters


def div_plot(X, clusters, k):
    cluster = clusters[k - 1]
    labels = np.unique(cluster)
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k', 'orange', 'navy', 'cyan', 'crimson', 'teal', 'sienna', 'khaki',
              'fuchsia']
    color = 0
    fig, ax = plt.subplots()

    for i in labels:
        points = np.array([X[j] for j in range(len(X)) if cluster[j] == i])
        ax.scatter(points[:, 0], points[:, 1], s= 15, c=colors[color])
        color += 1

    # plt.show(block=False)


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
