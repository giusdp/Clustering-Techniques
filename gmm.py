import matplotlib.pyplot as plt

import numpy as np
from scipy.stats import multivariate_normal


class GMM:

    def __init__(self, X, k, iterations):
        self.iterations = iterations
        self.k = k
        self.X = X
        self.mu = None
        self.pi = None
        self.cov = None
        self.XY = None

    def run(self):

        self.reg_cov = 1e-6 * np.identity(len(self.X[0]))
        x, y = np.meshgrid(np.sort(self.X[:, 0]), np.sort(self.X[:, 1]))
        self.XY = np.array([x.flatten(), y.flatten()]).T

        """Set the initial mu, covariance and pi values"""
        self.mu = np.random.randint(min(self.X[:, 0]), max(self.X[:, 0]), size=(self.k, len(self.X[0])))
        self.cov = np.zeros((self.k, len(self.X[0]), len(self.X[0])))
        for dim in range(len(self.cov)):
            np.fill_diagonal(self.cov[dim], 5)
        self.pi = np.ones(self.k) / self.k

        for i in range(self.iterations):

            """E Step"""
            r_ic = np.zeros((len(self.X), len(self.cov)))
            for m, co, p, r in zip(self.mu, self.cov, self.pi, range(len(r_ic[0]))):
                co += self.reg_cov
                mn = multivariate_normal(mean=m, cov=co)
                r_ic[:, r] = p * mn.pdf(self.X) / np.sum(
                    [pi_c * multivariate_normal(mean=mu_c, cov=cov_c).pdf(self.X) for pi_c, mu_c, cov_c in
                     zip(self.pi, self.mu, self.cov + self.reg_cov)], axis=0)

            """M Step"""
            self.mu = []
            self.cov = []
            self.pi = []

            for c in range(len(r_ic[0])):
                m_c = np.sum(r_ic[:, c], axis=0)
                mu_c = (1 / m_c) * np.sum(self.X * r_ic[:, c].reshape(len(self.X), 1), axis=0)
                self.mu.append(mu_c)

                self.cov.append(((1 / m_c) * np.dot((np.array(r_ic[:, c]).reshape(len(self.X), 1) * (self.X - mu_c)).T,
                                                    (self.X - mu_c))) + self.reg_cov)

                self.pi.append(m_c / np.sum(r_ic))

    def predict(self, Y):

        prediction = []
        for m, c in zip(self.mu, self.cov):
            prediction.append(multivariate_normal(mean=m, cov=c).pdf(Y) / np.sum(
                [multivariate_normal(mean=mean, cov=cov).pdf(Y) for mean, cov in zip(self.mu, self.cov)]))

        return prediction

    def return_y(self):
        y = np.zeros(len(self.X))
        for i in range(len(self.X)):
            y[i] = np.argmax(self.predict(self.X[i]))

        return y

    def plot(self):

        colors = ['r', 'g', 'b', 'y', 'c', 'm', 'w', 'k', 'orange', 'navy', 'cyan', 'crimson', 'teal', 'sienna',
                  'khaki', 'fuchsia']
        fig, ax = plt.subplots()

        for i in range(self.k):
            points = np.array([self.X[j] for j in range(len(self.X)) if np.argmax(self.predict(self.X[j])) == i])
            ax.scatter(points[:, 0], points[:, 1], s=15, c=colors[i])

        i = 0
        for m, c in zip(self.mu, self.cov):
            c += self.reg_cov
            multi_normal = multivariate_normal(mean=m, cov=c)
            ax.contour(np.sort(self.X[:, 0]), np.sort(self.X[:, 1]),
                       multi_normal.pdf(self.XY).reshape(len(self.X), len(self.X)), colors=colors[i], alpha=0.3)
            ax.scatter(m[0], m[1], c=colors[i], zorder=10, marker='+', s=15)
            i += 1
