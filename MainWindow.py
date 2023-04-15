import sys
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QTabWidget, QMainWindow, QFileDialog
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QAction, QIcon

from views.RecordTab import RecordTab

from qt_material import apply_stylesheet


class Window(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("My App")
        layout = QGridLayout()
        self.setLayout(layout)

        button_action = QAction(QIcon("bug.png"), "&Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.open_dialog)
        button_action.setCheckable(True)

        # set up tabs

        #tab "record"
        self.recordTab = RecordTab()

        #tab "calibrate"
        label2 = QLabel("Widget in Tab 2.")

        #tab "analyze"
        label3 = QLabel("Widget in Tab 2.")

        # create tab widget
        tabwidget = QTabWidget()
        tabwidget.addTab(self.recordTab, "Record")
        tabwidget.addTab(label2, "Calibrate")
        tabwidget.addTab(label3, "Analyze")
        layout.addWidget(tabwidget, 0, 0)
        self.setCentralWidget(tabwidget)

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
        self.recordTab.addFiles(fname[0])


app = QApplication(sys.argv)
screen = Window()
apply_stylesheet(app, theme='light_teal.xml')
app.setStyleSheet("QLabel{font-size: 18pt;}")
screen.show()
sys.exit(app.exec())