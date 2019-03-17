import numpy as np
from pandas import DataFrame
from sklearn.datasets import make_blobs

import kmeans
from matplotlib import pyplot as plt
from scipy.spatial.distance import pdist, squareform
from copy import deepcopy


def agg_func(X):
    y = np.array(range(len(X)))

    clusters = y.reshape(1, len(X))

    for i in range(len(X) - 1):

        centroids = []
        centroid_labels = []
        labels = np.unique(clusters[i])
        for j in labels:
            points = np.array([X[j] for p in range(len(X)) if clusters[i][p] == j])
            centroids.append(np.mean(points, axis=0))
            centroid_labels.append(j)

        dist = pdist(centroids)
        dist = squareform(dist)
        np.fill_diagonal(dist, np.inf)
        closest_1 = np.argmin(dist, axis=0)
        closest_2 = np.min(dist, axis=0)
        min_dist_cluster_1 = np.argmin(closest_2)
        min_dist_cluster_2 = closest_1[min_dist_cluster_1]

        min_dist_label_1 = centroid_labels[min_dist_cluster_1]
        min_dist_label_2 = centroid_labels[min_dist_cluster_2]

        y = deepcopy(clusters[i])
        for k in range(len(y)):

            if y[k] == min_dist_label_1:
                y[k] = min_dist_label_2

        clusters = np.append(clusters, y.reshape(1, len(y)), axis=0)

    return clusters


def div_func(X):
    clusters = np.zeros([1, len(X)])

    for i in range(len(X) - 1):
        counts = np.bincount(clusters[i].astype(int))
        maxcluster = np.argmax(counts)
        ind = np.where(clusters[i] == maxcluster)
        y, c = kmeans.kmeans_func(X[ind], 2)
        Y = deepcopy(clusters[i])
        Y[ind] = y
        Y = Y + 2
        clusters = np.append(clusters, Y.reshape(1, len(Y)), axis=0)

    return clusters


def agg_plot(X, clusters, k):
    cluster = clusters[len(clusters) - k]
    labels = np.unique(cluster)
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'w', 'k', 'orange', 'navy', 'cyan', 'crimson', 'teal', 'sienna', 'khaki',
              'fuchsia']
    color = 0
    fig, ax = plt.subplots()

    for i in labels:
        points = np.array([X[j] for j in range(len(X)) if cluster[j] == i])
        ax.scatter(points[:, 0], points[:, 1], s=50, c=colors[color])
        color += 1

    plt.show()


def div_plot(X, clusters, k):
    cluster = clusters[k - 1]
    labels = np.unique(cluster)
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'w', 'k', 'orange', 'navy', 'cyan', 'crimson', 'teal', 'sienna', 'khaki',
              'fuchsia']
    color = 0
    fig, ax = plt.subplots()

    for i in labels:
        points = np.array([X[j] for j in range(len(X)) if cluster[j] == i])
        ax.scatter(points[:, 0], points[:, 1], s=50, c=colors[color])
        color += 1

    # plt.show(block=False)


def transform_labels(y):
    labels = np.unique(y)
    Y = np.zeros(len(y))

    counter = 0
    for i in labels:
        ind = np.where(y == i)
        Y[ind] = counter
        counter += 1

    return Y
#
# if __name__ == '__main__':
#     X = create_blob_dataset(100, 3)
#     clusters = agg_func(X)
#     agg_plot(X, clusters, 4)