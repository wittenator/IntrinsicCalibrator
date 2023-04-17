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
        layout.addWidget(self.imv, 0, 1, 0, 3)
    
        # create board view
        self.board_imv = pg.ImageView()
        self.board_imv.show()
        layout.addWidget(self.board_imv, 1, 2)


        self.parameter_detection_dict = [
            {
                'name': 'Aruco Dictionary',
                'type': 'list',
                'values': ["4x4_1000"],
                'value': "4x4_1000"
            },
            {
                'name': 'Columns',
                'type': 'int',
                'value': "30"
            },
            {
                'name': 'Rows',
                'type': 'int',
                'value': "21"
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
        
        # Create tree of Parameter objects for Board Detection
        self.parameter_detection = Parameter.create(name='params',
                                  type='group',
                                  children=self.parameter_detection_dict)
        self.tree_detection = ParameterTree()
        self.tree_detection.setParameters(self.parameter_detection, showTop=False)
        self.parameter_detection.sigTreeStateChanged.connect(self.handle_tree_detection_changed)
        layout.addWidget(self.tree_detection, 1, 0)

        self.parameter_calibration_dict = [
            {
                'name': 'Run Calibration',
                'type': 'action'
            }
        ]
        
        # Create tree of Parameter objects for Board Detection
        self.parameter_calibration = Parameter.create(name='params',
                                  type='group',
                                  children=self.parameter_calibration_dict)
        self.tree_calibration = ParameterTree()
        self.tree_calibration.setParameters(self.parameter_calibration, showTop=False)
        self.parameter_calibration.sigTreeStateChanged.connect(self.handle_tree_calibration_changed)
        layout.addWidget(self.tree_calibration, 1, 1)

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
        self.current_image = img
        self.imv.setImage(img.T)

    def handle_tree_detection_changed(self, tree_state, tree_change):
        """
        When the selection changes, load the image into the image view
        """
        print("selection changed")
        values = tree_state.getValues()
        aruco_dict = cv2.aruco.getPredefinedDictionary({
                "aruco_orig" : cv2.aruco.DICT_ARUCO_ORIGINAL,
                "4x4_250"    : cv2.aruco.DICT_4X4_250,
                "4x4_1000"    : cv2.aruco.DICT_4X4_1000,
                "5x5_250"    : cv2.aruco.DICT_5X5_250,
                "6x6_250"    : cv2.aruco.DICT_6X6_250,
                "7x7_250"    : cv2.aruco.DICT_7X7_250}[values['Aruco Dictionary'][0]])
        print(values['Aruco Dictionary'][0])
        self.charuco_board = cv2.aruco.CharucoBoard((values['Columns'][0], values['Rows'][0]), values['Square Size'][0], values['Marker Size'][0], aruco_dict)
        aruco_parameters = cv2.aruco.DetectorParameters()
        #aruco_parameters.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
        charuco_detector = cv2.aruco.CharucoDetector(self.charuco_board, detectorParams=aruco_parameters)

        # print board
        board_img = self.charuco_board.generateImage((2000, 2000))
        self.board_imv.setImage(board_img.T)

        # detect board in images
        for image in self.model.images:
            img = cv2.imread(image.file_path, 0)
            image.board_detections = charuco_detector.detectBoard(img)


    def handle_tree_calibration_changed(self, tree_state, tree_change):
        """
        When the selection changes, load the image into the image view
        """
        charuco_corners, charuco_ids = zip(*[image.board_detections[:2] for image in self.model.images if image.board_detections is not None])
        print(charuco_corners)
        print(charuco_ids)
        reproj_err, self.intrinsics, self.distortion, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(charuco_corners, charuco_ids, self.charuco_board, self.current_image.shape, None, None)
        print("Reprojection error: {}".format(reproj_err))


    
        

