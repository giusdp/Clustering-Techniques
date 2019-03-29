# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License
# Copyright (c) 2015 Pierre Raybaut

"""
Simple example illustrating Qt Charts capabilities to plot curves with 
a high number of points, using OpenGL accelerated series
"""

import sys

import numpy
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLineEdit)
from matplotlib import pyplot
from pandas import DataFrame, read_csv
from sklearn.datasets import make_blobs, make_circles

from bottom_up import bottom_up_clustering
from top_down import div_func, div_plot
from kmeans_sk import k_means_clustering

X_data = 0
y_data = 0

def show_dataset(dataframe):
    # max 16 colors to identify clusters.
    # So DO NOT set more than 15 clusters at a time. Otherwise error with colors[key] below
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k', 'orange', 'navy', 'cyan', 'crimson', 'teal', 'sienna',
              'khaki',
              'fuchsia']
    _, axes = pyplot.subplots()
    grouped = dataframe.groupby('label')
    pyplot.title("Created Clusters")
    for key, group in grouped:
        group.plot(ax=axes, kind='scatter', x='x', y='y', s=15, label=key, color=colors[key])

    pyplot.pause(0.001)
    pyplot.show()

def create_blob_dataset(n_elems, n_groups):
    X, y = make_blobs(n_samples=n_elems, centers=n_groups, n_features=2)  # generate 2d dataset
    global X_data
    X_data = X
    global y_data
    y_data = y
    #X, y = make_circles(100)
    df = DataFrame(dict(x=X[:, 0], y=X[:, 1], label=y))

    with open('dataset.csv', 'w') as f:
        df.to_csv(f)
    return df

def extract_X(dataframe):
    dX = list(zip(dataframe.x, dataframe.y))
    dX = list(map(list, dX))
    ndx = numpy.array(dX)
    return ndx

def load_blob_dataset():
    with open('dataset.csv', 'r') as f:
        df = read_csv(f)
    return df

class Window(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.current_dataset = None

        self.gen_data_button = QPushButton('Gen Dataset')
        self.gen_data_button.clicked.connect(self.gen_dataset)

        self.aggl_button = QPushButton('Agglomerative')
        self.aggl_button.clicked.connect(self.run_aggl_clustering)
        self.aggl_button.setDisabled(True)

        self.line_clusters = QLineEdit(self)
        self.line_clusters.resize(32, 32)

        self.div_button = QPushButton('Divisive')
        self.div_button.clicked.connect(self.run_div_clustering)
        self.div_button.setDisabled(True)

        self.kmeans_button = QPushButton('K-Means')
        self.kmeans_button.clicked.connect(self.run_k_means)
        self.kmeans_button.setDisabled(True)

        self.em_button = QPushButton('EM')
        self.em_button.clicked.connect(self.run_em)
        self.em_button.setDisabled(True)

        self.load_button = QPushButton('Load')
        self.load_button.clicked.connect(self.load_data)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        # self.textbox = QLineEdit(self)
        # self.textbox.resize(40, 40)
        # vbox.addWidget(self.textbox, alignment=Qt.AlignCenter)

        hbox.addWidget(self.gen_data_button, alignment=Qt.AlignCenter)
        hbox.addWidget(self.load_button, alignment=Qt.AlignCenter)
        vbox.addLayout(hbox)

        vbox.addWidget(self.line_clusters, alignment=Qt.AlignCenter)
        vbox.addWidget(self.aggl_button, alignment=Qt.AlignCenter)
        vbox.addWidget(self.div_button, alignment=Qt.AlignCenter)
        vbox.addWidget(self.kmeans_button, alignment=Qt.AlignCenter)
        vbox.addWidget(self.em_button, alignment=Qt.AlignCenter)

        self.setLayout(vbox)

    def gen_dataset(self):
        if not self.line_clusters.text():
            print("Dai numero di clusters")
            return

        nc = int(self.line_clusters.text())
        self.current_dataset = create_blob_dataset(1000, nc)

        show_dataset(self.current_dataset)

        self.aggl_button.setDisabled(False)
        self.div_button.setDisabled(False)
        self.kmeans_button.setDisabled(False)
        self.em_button.setDisabled(False)

    def load_data(self):
        self.current_dataset = load_blob_dataset()
        show_dataset(self.current_dataset)
        self.aggl_button.setDisabled(False)
        self.div_button.setDisabled(False)
        self.kmeans_button.setDisabled(False)
        self.em_button.setDisabled(False)

    def run_aggl_clustering(self):
        if not self.line_clusters.text():
            print("Dai numero di clusters per agglomerative")
            return

        nc = int(self.line_clusters.text())

        bottom_up_clustering(extract_X(self.current_dataset), nc)
        pyplot.pause(0.001)
        pyplot.show()

    def run_div_clustering(self):
        if not self.line_clusters.text():
            print("Dai numero di clusters per divisive")
            return

        nc = int(self.line_clusters.text())

        X = extract_X(self.current_dataset)
        clusters = div_func(X)
        div_plot(X, clusters, nc)

        pyplot.title("Hierarchical Top-Down Approach")
        pyplot.pause(0.001)
        pyplot.show()

    def run_k_means(self):
        if not self.line_clusters.text():
            print("Dai numero di clusters per kmeans")
            return

        nc = int(self.line_clusters.text())
        k_means_clustering(extract_X(self.current_dataset), nc)
        pyplot.pause(0.001)
        pyplot.show()

    def run_em(self):
        #from gmm import GMM
        from em import em_clustering
        if not self.line_clusters.text():
            print("Dai numero di clusters per em")
            return

        nc = int(self.line_clusters.text())
        em_clustering(X_data, y_data, nc, 10)
        # em.run()
        # em.plot()
        #pyplot.title("EM - Gassian Mixture")
        pyplot.pause(0.001)
        pyplot.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.setWindowTitle("Clustering")
    window.resize(150, 250)
    window.show()

    sys.exit(app.exec_())
