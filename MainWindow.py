import sys
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QTabWidget, QMainWindow, QFileDialog
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QAction, QIcon
from model.FileListModel import FileListModel
from views.CalibrateTab import CalibrateTab

from views.RecordTab import RecordTab

from qt_material import apply_stylesheet


class Window(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("My App")
        layout = QGridLayout()
        self.setLayout(layout)
        
        # initialize model
        self.model = FileListModel()

        # set up tabs

        #tab "record"
        self.recordTab = RecordTab(self.model)

        #tab "calibrate"
        self.calibrateTab = CalibrateTab(self.model)

        #tab "analyze"
        label3 = QLabel("Widget in Tab 2.")

        # create tab widget
        tabwidget = QTabWidget()
        tabwidget.addTab(self.recordTab, "Record")
        tabwidget.addTab(self.calibrateTab, "Calibrate")
        tabwidget.addTab(label3, "Analyze")
        layout.addWidget(tabwidget, 0, 0)
        self.setCentralWidget(tabwidget)

        # Create Menu
        button_action = QAction(QIcon("bug.png"), "&Load Images", self)
        button_action.setStatusTip("Load images from filesystem")
        button_action.triggered.connect(self.open_dialog)
        button_action.setCheckable(True)

        menu = self.menuBar()
        file_menu = menu.addMenu("Sources")
        file_menu.addAction(button_action)

    @pyqtSlot()
    def open_dialog(self):
        fname = QFileDialog.getOpenFileNames(
            self,
            "Open File",
            "${HOME}",
            "JPG Files (*.jpg);; PNG Files (*.png)",
        )
        paths = fname[0]
        for path in paths:
            self.addImage(path)

    def addImage(self, file_path: str):
        self.model.addImage(file_path=file_path)

app = QApplication(sys.argv)
screen = Window()
apply_stylesheet(app, theme='light_teal.xml')
app.setStyleSheet("QLabel{font-size: 18pt;}")
screen.show()
sys.exit(app.exec())