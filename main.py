# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License
# Copyright (c) 2015 Pierre Raybaut

"""
Simple example illustrating Qt Charts capabilities to plot curves with 
a high number of points, using OpenGL accelerated series
"""

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMainWindow, QSizePolicy, QVBoxLayout, QHBoxLayout)
import matplotlib
matplotlib.use('QT5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas

from bottom_up import create_blob_dataset, bottom_up_clustering

# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

# Matplotlib widget
class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()        # Create canvas object
        self.vbl = QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        self.init_ui()
        
    def init_ui(self):
        btn = QPushButton('Button')
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.clicked.connect(self.doAction)
        btn.resize(btn.sizeHint())

        btn2 = QPushButton('Button2')

        vbox = QVBoxLayout()
        vbox.addStretch(1)

        vbox.addWidget(btn)
        vbox.addWidget(btn2)


        self.plotWidget = MplWidget()

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)        
        hbox.addWidget(self.plotWidget)
        self.setLayout(hbox)   

    def plot_data(self):
        x=range(0, 10)
        y=range(0, 20, 2)
        self.plotWidget.canvas.ax.plot(x, y)
        self.plotWidget.canvas.draw()
    
    def doAction(self):
        print("button 1 pressed")
        # df = create_blob_dataset(100, 5)
        self.plot_data

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.setWindowTitle("Simple example")
    window.show()
    window.resize(640, 400)

    sys.exit(app.exec_())