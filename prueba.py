# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prueba.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuuno = QtWidgets.QMenu(self.menubar)
        self.menuuno.setObjectName("menuuno")
        self.menudos = QtWidgets.QMenu(self.menubar)
        self.menudos.setObjectName("menudos")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actiondos = QtWidgets.QAction(MainWindow)
        self.actiondos.setObjectName("actiondos")
        self.actiontres = QtWidgets.QAction(MainWindow)
        self.actiontres.setObjectName("actiontres")
        self.actionuno = QtWidgets.QAction(MainWindow)
        self.actionuno.setObjectName("actionuno")
        self.menuuno.addAction(self.actiondos)
        self.menuuno.addAction(self.actiontres)
        self.menudos.addAction(self.actionuno)
        self.menubar.addAction(self.menuuno.menuAction())
        self.menubar.addAction(self.menudos.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuuno.setTitle(_translate("MainWindow", "uno"))
        self.menudos.setTitle(_translate("MainWindow", "dos"))
        self.actiondos.setText(_translate("MainWindow", "dos"))
        self.actiontres.setText(_translate("MainWindow", "tres"))
        self.actionuno.setText(_translate("MainWindow", "uno"))

