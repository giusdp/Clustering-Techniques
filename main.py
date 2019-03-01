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
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QSizePolicy, QVBoxLayout,
                             QHBoxLayout)

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas

from bottom_up import *
matplotlib.use('QT5Agg')


# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


# Matplotlib widget
class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)  # Inherit from QWidget
        self.canvas = MplCanvas()  # Create canvas object
        self.vbl = QVBoxLayout()  # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

    def plot_data(self, df):
        self.canvas.axes.scatter(df.x, df.y)
        self.canvas.draw()
        self.canvas.axes.cla()

    def draw_dendrogram(self, df):
        # max 16 colors to identify clusters. So DO NOT set more than 16 clusters at a time.
        # Otherwise error with colors[key] below
        colors = ['r', 'g', 'b', 'y', 'c', 'm', 'w', 'k', 'orange', 'navy', 'cyan', 'crimson', 'teal', 'sienna',
                  'khaki', 'fuchsia']
        grouped = df.groupby('label')
        for key, group in grouped:
            group.plot(ax=self.canvas.axes, kind='scatter', x='x', y='y', label=key, color=colors[key])

        # pyplot.figure(figsize=dataframe.shape)  
        self.canvas.fig = Figure(figsize=df.shape)
        dendrogram(linkage(df, 'ward'))

        self.canvas.draw()
        # self.canvas.axes.cla()

    def set_title(self, title):
        self.canvas.axes.set_title(title)


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        self.current_df = None
        blob_button = QPushButton('1 - Make Blobs')
        blob_button.setToolTip('Create blobs of data points.')
        blob_button.clicked.connect(self.do_make_blobs)
        blob_button.resize(blob_button.sizeHint())

        self.dendrogram_button = QPushButton('2 - Dendogram')
        self.dendrogram_button.setToolTip('Draw the dendogram related to the last blobs made.')
        self.dendrogram_button.clicked.connect(self.do_make_dendrogram)

        self.dendrogram_button.setDisabled(True)
        hbox = QHBoxLayout()

        hbox.addWidget(blob_button)
        hbox.addWidget(self.dendrogram_button)

        self.plotWidget = MplWidget()

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.plotWidget)
        self.setLayout(vbox)

    def do_make_blobs(self):
        self.plotWidget.set_title("Blobs of data")
        self.current_df = create_blob_dataset(100, 3)
        self.plotWidget.plot_data(self.current_df)
        self.dendrogram_button.setDisabled(False)

    def do_make_dendrogram(self):
        self.plotWidget.set_title("Dendrogram")
        self.plotWidget.draw_dendrogram(self.current_df)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.setWindowTitle("Simple example")
    window.resize(1024, 720)
    window.show()

    sys.exit(app.exec_())
