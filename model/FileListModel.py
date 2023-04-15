import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt
from pydantic import BaseModel

import numpy as np

class Image(BaseModel):
    file_path: str
    detected_corners: np.ndarray | None = None

    class Config:
        arbitrary_types_allowed = True

class FileListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, image_paths: list[str]=[], **kwargs):
        super(FileListModel, self).__init__(*args, **kwargs)
        self.images: list[Image] = [Image(file_path=path) for path in image_paths]

    def data(self, index: int, role) -> str:
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the data structure.
            item: Image = self.images[index.row()]
            # Return the todo text only.
            return item.file_path

    def rowCount(self, index):
        return len(self.images)
    
    def addImage(self, file_path: str):
        self.images.append(Image(file_path=file_path))
        self.layoutChanged.emit()