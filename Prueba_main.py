import os
import operator

from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox, QListView, QGraphicsView, QGraphicsScene, QFileDialog, QVBoxLayout, QApplication

from qgis.utils import iface
from qgis.core import QgsProject

import os, json, requests, sys, datetime, base64, time, hashlib
import sys

FORM_CLASS, _ = uic.loadUiType(os.path.join(
	os.path.dirname(__file__), 'prueba.ui'))

class Prueba(QtWidgets.QMainWindow, FORM_CLASS):
	def __init__(self, parent=None, iface=None):
		"""Constructor."""
		super(Prueba, self).__init__(iface.mainWindow(), \
		flags=Qt.WindowMinimizeButtonHint)



	def initGui(self):

		self.setupUi(self)
		self.setWindowTitle('ShapeViewer')

		icon_path = ':/plugins/Master/icon.png'

		self.show()

	def showEvent(self, event):
		print('iniciamos perros desgraciados')