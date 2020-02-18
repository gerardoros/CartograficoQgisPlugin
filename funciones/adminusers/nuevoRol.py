# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nuevoRol.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(290, 93)
        Dialog.setMinimumSize(QtCore.QSize(290, 93))
        Dialog.setMaximumSize(QtCore.QSize(290, 93))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(290, 93))
        self.scrollArea.setMaximumSize(QtCore.QSize(290, 93))
        self.scrollArea.setStyleSheet("background : rgb(250,238,224)")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 288, 91))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnAceptar = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btnAceptar.setMinimumSize(QtCore.QSize(130, 30))
        self.btnAceptar.setMaximumSize(QtCore.QSize(130, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnAceptar.setFont(font)
        self.btnAceptar.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255)\n"
"}\n"
"QPushButton::disabled {\n"
"background : rgb(187, 129, 13);\n"
"color : rgb(245,245,245);\n"
"border: 1px solid #adb2b5;\n"
"}")
        self.btnAceptar.setObjectName("btnAceptar")
        self.gridLayout_2.addWidget(self.btnAceptar, 1, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_5.setMinimumSize(QtCore.QSize(60, 0))
        self.label_5.setMaximumSize(QtCore.QSize(50, 25))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.btnCancelar = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btnCancelar.setMinimumSize(QtCore.QSize(130, 30))
        self.btnCancelar.setMaximumSize(QtCore.QSize(130, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnCancelar.setFont(font)
        self.btnCancelar.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255)\n"
"}\n"
"QPushButton::disabled {\n"
"background : rgb(187, 129, 13);\n"
"color : rgb(245,245,245);\n"
"border: 1px solid #adb2b5;\n"
"}")
        self.btnCancelar.setObjectName("btnCancelar")
        self.gridLayout_2.addWidget(self.btnCancelar, 1, 2, 1, 2)
        self.leBusqueda = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.leBusqueda.setMinimumSize(QtCore.QSize(0, 25))
        self.leBusqueda.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.leBusqueda.setFont(font)
        self.leBusqueda.setStyleSheet("background : rgb(255,255,255)")
        self.leBusqueda.setObjectName("leBusqueda")
        self.gridLayout_2.addWidget(self.leBusqueda, 0, 1, 1, 3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Nuevo Rol"))
        self.btnAceptar.setText(_translate("Dialog", "Aceptar"))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p>Rol:</p></body></html>"))
        self.btnCancelar.setText(_translate("Dialog", "Cancelar"))

