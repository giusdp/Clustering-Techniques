from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout

from bottom_up import create_blob_dataset
from mpl_widget import MplWidget


class BUClusteringWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
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

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def do_make_blobs(self):
        pass

    def do_make_dendrogram(self):
        pass
