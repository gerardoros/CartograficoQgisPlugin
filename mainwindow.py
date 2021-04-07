import os
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from pathlib import Path
from qgis.utils import iface
from PyQt5.QtWidgets import QApplication, QMainWindow ## NUEVA LÍNEA
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox, qApp, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'mainwindow.ui'))
class MainWindow(QtWidgets.QMainWindow, FORM_CLASS): ## NUEVA LÍNEA
    def __init__(self, iface, parent = iface.mainWindow()):
        super(MainWindow, self).__init__(parent, \
            flags=Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        
        self.setupUi(self)
        self._create_ui()


    def _create_ui(self):
        self.setGeometry(500, 500, 500, 500)           
        
        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        menu = menubar.addMenu('&Edit')
        menu = menubar.addMenu('&Show')
        fileMenu.addAction(exitAction)
        
        
        self.setWindowTitle('PyQt5 Basic Menubar')  
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
    self.dlg.show()
        # Run the dialog event loop
    result = self.dlg.exec_()
        # See if OK was pressed
        #self.irAConsulta()

    if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            
        pass
