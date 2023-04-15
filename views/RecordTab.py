from PyQt6.QtWidgets import QListView, QWidget, QGridLayout
from model.FileListModel import FileListModel

import pyqtgraph as pg
import cv2

class RecordTab(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)

        # create a list view from FileListModel
        self.model = FileListModel()
        view = QListView()
        view.setModel(self.model)
        view.selectionModel().selectionChanged.connect(
            self.handle_selection_changed
        )
        layout.addWidget(view, 0, 0)

        # create image view
        self.imv = pg.ImageView()
        self.imv.show()
        layout.addWidget(self.imv, 0, 1)

    def addFiles(self, paths: list[str]):
        """
        Add an item to our todo list, getting the text from the QLineEdit .todoEdit
        and then clearing it.
        """
        for path in paths:
            self.model.addImage(file_path=path)

    def handle_selection_changed(self, selected, deselected):
        """
        When the selection changes, load the image into the image view
        """
        # load the image data into the ImageView
        index = selected.indexes()[0]
        file_path = self.model.images[index.row()].file_path
        img = cv2.imread(file_path, 0) # 0 = grayscale
        self.imv.setImage(img.T)
        

