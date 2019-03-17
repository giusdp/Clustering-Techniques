# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License
# Copyright (c) 2015 Pierre Raybaut

"""
Simple example illustrating Qt Charts capabilities to plot curves with 
a high number of points, using OpenGL accelerated series
"""

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QPushButton, QWidget, QLineEdit)
from matplotlib import pyplot
from pandas import DataFrame
from sklearn.datasets import make_blobs

from bottom_up import bottom_up_clustering
from em import em_clustering
from hierarchical import div_func, div_plot
from kmeans_sk import k_means_clustering


def create_blob_dataset(n_elems, n_groups):
    X, y = make_blobs(n_samples=n_elems, centers=n_groups, n_features=2)  # generate 2d dataset
    df = DataFrame(dict(x=X[:, 0], y=X[:, 1], label=y))
    return X, df


class Window(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.current_dataset = None

        self.gen_data_button = QPushButton('Gen Dataset')
        self.gen_data_button.clicked.connect(self.gen_dataset)

        self.aggl_button = QPushButton('Agglomerative')
        self.aggl_button.clicked.connect(self.run_aggl_clustering)
        self.aggl_button.setDisabled(True)

        self.div_button = QPushButton('Divisive')
        self.div_button.clicked.connect(self.run_div_clustering)
        self.div_button.setDisabled(True)

        self.kmeans_button = QPushButton('K-Means')
        self.kmeans_button.clicked.connect(self.run_k_means)
        self.kmeans_button.setDisabled(True)

        self.em_button = QPushButton('EM')
        self.em_button.clicked.connect(self.run_em)
        self.em_button.setDisabled(True)

        vbox = QVBoxLayout()

        # self.textbox = QLineEdit(self)
        # self.textbox.resize(40, 40)
        # vbox.addWidget(self.textbox, alignment=Qt.AlignCenter)

        vbox.addWidget(self.gen_data_button, alignment=Qt.AlignCenter)
        vbox.addWidget(self.aggl_button, alignment=Qt.AlignCenter)
        vbox.addWidget(self.div_button, alignment=Qt.AlignCenter)
        vbox.addWidget(self.kmeans_button, alignment=Qt.AlignCenter)
        vbox.addWidget(self.em_button, alignment=Qt.AlignCenter)

        self.setLayout(vbox)

    def gen_dataset(self):
        self.current_dataset = create_blob_dataset(50, 3)

        # max 16 colors to identify clusters.
        # So DO NOT set more than 16 clusters at a time. Otherwise error with colors[key] below
        colors = ['r', 'g', 'b', 'y', 'c', 'm', 'w', 'k', 'orange', 'navy', 'cyan', 'crimson', 'teal', 'sienna',
                  'khaki',
                  'fuchsia']
        _, axes = pyplot.subplots()
        grouped = self.current_dataset[1].groupby('label')
        pyplot.title("Created Clusters")
        for key, group in grouped:
            group.plot(ax=axes, kind='scatter', x='x', y='y', label=key, color=colors[key])

        pyplot.pause(0.001)
        pyplot.show()

        self.aggl_button.setDisabled(False)
        self.div_button.setDisabled(False)
        self.kmeans_button.setDisabled(False)
        self.em_button.setDisabled(False)

    def run_aggl_clustering(self):
        bottom_up_clustering(self.current_dataset[1])
        pyplot.pause(0.001)
        pyplot.show()

    def run_div_clustering(self):
        clusters = div_func(self.current_dataset[0])
        print(len(clusters))
        div_plot(self.current_dataset[0], clusters, 3)
        pyplot.pause(0.001)
        pyplot.show()

    def run_k_means(self):
        k_means_clustering(self.current_dataset[0])
        pyplot.pause(0.001)
        pyplot.show()

    def run_em(self):
        em_clustering(self.current_dataset[0])
        pyplot.pause(0.001)
        pyplot.show()
        # from gmm import GMM
        # em = GMM(self.current_dataset[0], 3, 10)
        # em.run()
        # em.plot()
        # pyplot.pause(0.001)
        # pyplot.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.setWindowTitle("Clustering")
    window.resize(150, 250)
    window.show()

    sys.exit(app.exec_())
