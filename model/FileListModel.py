import sys
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QModelIndex
from pydantic import BaseModel

import numpy as np

class Image(BaseModel):
    file_path: str
    board_detections: list | None = None
    selected: bool = True

    class Config:
        arbitrary_types_allowed = True

class FileListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, image_paths: list[str]=[], **kwargs):
        super(FileListModel, self).__init__(*args, **kwargs)
        self.images: list[Image] = [Image(file_path=path) for path in image_paths]

    def data(self, index: int, role) -> str:
        item: Image = self.images[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return item.file_path
        elif role == Qt.ItemDataRole.CheckStateRole:
            return item.selected

    def rowCount(self, index):
        return len(self.images)
    
    def addImage(self, file_path: str):
        self.images.append(Image(file_path=file_path))
        self.layoutChanged.emit()
    
    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return super().flags(index) | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsSelectable