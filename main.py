# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License
# Copyright (c) 2015 Pierre Raybaut

"""
Simple example illustrating Qt Charts capabilities to plot curves with 
a high number of points, using OpenGL accelerated series
"""

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication, QMainWindow)
from PyQt5.QtGui import QFont 
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPolygonF, QPainter

import numpy as np

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        self.chart = QChart()
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)
        self.init_buttons()

    def init_buttons(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.clicked.connect(self.doAction)
        btn.resize(btn.sizeHint())

    
    def doAction(self):
        print("Button pressed")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.setWindowTitle("Simple example")
    window.show()
    window.resize(640, 400)

    sys.exit(app.exec_())