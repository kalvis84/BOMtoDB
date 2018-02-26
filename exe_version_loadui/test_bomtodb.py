import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
import BOMtoDB


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('BOMtoDB.ui', self)
        self.dbfilechoosen = 0
        self.dbfilename = None
        self.bomfilechoosen = 0
        self.bomfilename = None

    def check_completion(self):
        print("not yet complete")
        if self.dbfilechoosen == 1 and self.bomfilechoosen == 1:
            print("complete")
            self.statusbar.showMessage("Click 'Accept' button to finish.", 5000)
            self.buttonaccept.setEnabled(True)

    @pyqtSlot()
    def on_buttonaccept_clicked(self):
        if BOMtoDB.insert_bom_to_db(self.dbfilename, self.bomfilename):
            self.statusbar.showMessage("ERROR. Check cmd line window for details", 5000)

    @pyqtSlot()
    def on_button_choosedb_clicked(self):
        name = QFileDialog.getOpenFileName(None, "Choose Database File", '.', '*.db')
        self.labeldbname.setText(name[0])    # [0] element contains full path to the file.
        self.dbfilename = name[0]
        self.dbfilechoosen = 1
        self.check_completion()

    @pyqtSlot()
    def on_button_choosebom_clicked(self):
        name = QFileDialog.getOpenFileName(None, "Choose BOM File", '.', '*.xls')
        self.labelbomname.setText(name[0])    # [0] element contains full path to the file.
        self.bomfilename = name[0]
        self.bomfilechoosen = 1
        self.check_completion()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
