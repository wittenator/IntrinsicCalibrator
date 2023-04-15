from PyQt6.QtWidgets import QListView, QWidget, QGridLayout, QSizePolicy

import pyqtgraph as pg
import cv2
from pyqtgraph.parametertree import (
    Parameter,
    ParameterTree,
    RunOptions,
    InteractiveFunction,
    Interactor,
)


class CalibrateTab(QWidget):
    def __init__(self, model):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)

        # create a list view from FileListModel
        self.model = model
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
    
        # create board view
        self.board_imv = pg.ImageView()
        self.board_imv.show()
        layout.addWidget(self.board_imv, 1, 1)


        self.params = [
            {
                'name': 'Aruco Dictionary',
                'type': 'list',
                'values': ["4x4_1000"],
                'value': "4x4_1000"
            },
            {
                'name': 'Columns',
                'type': 'int',
                'value': "20"
            },
            {
                'name': 'Rows',
                'type': 'int',
                'value': "29"
            },
            {
                'name': 'Marker Size',
                'type': 'float',
                'value': "0.019"
            },
            {
                'name': 'Square Size',
                'type': 'float',
                'value': "0.025"
            },
            {
                'name': 'Run Detection',
                'type': 'action'
            }
        ]

        # Create tree of Parameter objects
        self.p = Parameter.create(name='params',
                                  type='group',
                                  children=self.params)
        self.t = ParameterTree()
        self.t.setParameters(self.p, showTop=False)
        self.p.sigTreeStateChanged.connect(self.handle_tree_changed)
        layout.addWidget(self.t, 1, 0)

    def handle_selection_changed(self, selected, deselected):
        """
        When the selection changes, load the image into the image view
        """
        # load the image data into the ImageView
        index = selected.indexes()[0]
        image = self.model.images[index.row()]
        file_path = image.file_path
        img = cv2.imread(file_path, 0) # 0 = grayscale
        if image.board_detections:
            charuco_corners, charuco_ids, marker_corners, marker_ids = image.board_detections
            if not (marker_ids is None) and len(marker_ids) > 0:
                cv2.aruco.drawDetectedMarkers(img, marker_corners)
            if not (charuco_ids is None) and len(charuco_ids) > 0:
                cv2.aruco.drawDetectedCornersCharuco(img, charuco_corners, charuco_ids)
        self.imv.setImage(img.T)

    def handle_tree_changed(self, selected, deselected):
        """
        When the selection changes, load the image into the image view
        """
        print("selection changed")
        values = selected.getValues()
        aruco_dict = cv2.aruco.getPredefinedDictionary({
                "aruco_orig" : cv2.aruco.DICT_ARUCO_ORIGINAL,
                "4x4_250"    : cv2.aruco.DICT_4X4_250,
                "4x4_1000"    : cv2.aruco.DICT_4X4_1000,
                "5x5_250"    : cv2.aruco.DICT_5X5_250,
                "6x6_250"    : cv2.aruco.DICT_6X6_250,
                "7x7_250"    : cv2.aruco.DICT_7X7_250}[values['Aruco Dictionary'][0]])
        print(values['Aruco Dictionary'][0])
        charuco_board = cv2.aruco.CharucoBoard((values['Columns'][0], values['Rows'][0]), values['Square Size'][0], values['Marker Size'][0], aruco_dict, legacy=True)
        aruco_parameters = cv2.aruco.DetectorParameters()
        aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_parameters)
        charuco_detector = cv2.aruco.CharucoDetector(charuco_board)

        # print board
        board_img = charuco_board.generateImage((2000, 2000))
        self.board_imv.setImage(board_img.T)

        # detect board in images
        for image in self.model.images:
            img = cv2.imread(image.file_path, 0)
            image.board_detections = charuco_detector.detectBoard(img, )


    
        

