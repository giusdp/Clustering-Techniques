import matplotlib.pyplot as pyplot
from sklearn.cluster import KMeans


def k_means_clustering(X):
    pyplot.figure()
    pyplot.scatter(X[:, 0], X[:, 1], label='True Position')

    kmeans = KMeans()
    kmeans.fit_predict(X)

    pyplot.scatter(X[:, 0], X[:, 1], c=kmeans.labels_, cmap='rainbow')
    pyplot.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], color='black')  # Centroidi

