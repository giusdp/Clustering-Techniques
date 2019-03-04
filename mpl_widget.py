from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from scipy.cluster.hierarchy import dendrogram, linkage

matplotlib.use('QT5Agg')


# Matplotlib canvas class to create figure
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, self.fig)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)


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
        self.canvas.axes.cla()

    def set_title(self, title):
        self.canvas.axes.set_title(title)
