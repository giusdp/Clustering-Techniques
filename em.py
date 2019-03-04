import numpy as np
import scipy.stats
from matplotlib import pyplot
from sklearn.mixture import GaussianMixture


def em_clustering(X):
    pyplot.figure()
    pyplot.scatter(X[:, 0], X[:, 1])

    gmm = GaussianMixture(n_components=3, covariance_type='full')
    gmm.fit(X)

    pyplot.scatter(X[:, 0], X[:, 1], cmap='rainbow')

    pyplot.scatter(X[:, 0], X[:, 1], s=1)

    centers = np.empty(shape=(gmm.n_components, X.shape[1]))
    for i in range(gmm.n_components):
        density = scipy.stats.multivariate_normal(cov=gmm.covariances_[i], mean=gmm.means_[i]).logpdf(X)
        centers[i, :] = X[np.argmax(density)]
    pyplot.scatter(centers[:, 0], centers[:, 1], s=20)
    pyplot.show()