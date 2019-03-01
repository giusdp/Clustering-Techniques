# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License
# Copyright (c) 2015 Pierre Raybaut

"""
Simple example illustrating Qt Charts capabilities to plot curves with 
a high number of points, using OpenGL accelerated series
"""

import sys

from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout,
                             QTabWidget, QMainWindow)

from agglomerative import BUClusteringWidget


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        # self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Agglomerative Clustering")
        self.tabs.addTab(self.tab2, "Divisive Clustering")
        self.tabs.addTab(self.tab3, "K-Means Clustering")
        self.tabs.addTab(self.tab4, "EM Clustering")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        # self.pushButton1 = QPushButton("PyQt5 button")
        self.tab1.layout.addWidget(BUClusteringWidget())
        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.setWindowTitle("Simple example")
    window.resize(1024, 720)
    window.show()

    sys.exit(app.exec_())
