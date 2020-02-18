# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'agregarRoles.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(425, 300)
        Dialog.setMinimumSize(QtCore.QSize(425, 300))
        Dialog.setMaximumSize(QtCore.QSize(425, 300))
        Dialog.setStyleSheet("background-color: white;")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setStyleSheet("background : rgb(250,238,224)")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 405, 280))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnNuevoRol = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btnNuevoRol.setMinimumSize(QtCore.QSize(150, 30))
        self.btnNuevoRol.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnNuevoRol.setFont(font)
        self.btnNuevoRol.setStyleSheet("QPushButton{\n"
                                       "background : rgb(174, 116, 0);\n"
                                       "color : rgb(255, 255, 255)\n"
                                       "}\n"
                                       "QPushButton::disabled {\n"
                                       "background : rgb(187, 129, 13);\n"
                                       "color : rgb(245,245,245);\n"
                                       "border: 1px solid #adb2b5;\n"
                                       "}")
        self.btnNuevoRol.setObjectName("btnNuevoRol")
        self.gridLayout_2.addWidget(self.btnNuevoRol, 0, 2, 1, 1)
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
        self.gridLayout_2.addWidget(self.btnAceptar, 3, 1, 1, 1)
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
        self.gridLayout_2.addWidget(self.btnCancelar, 3, 2, 1, 1)
        self.twRoles = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.twRoles.setMinimumSize(QtCore.QSize(0, 150))
        self.twRoles.setMaximumSize(QtCore.QSize(16777215, 250))
        self.twRoles.setStyleSheet("QTableWidget {background-color: white;}\n"
                                   "QHeaderView::section\n"
                                   "{\n"
                                   "background-color: rgb(238,225,200);\n"
                                   "color : rgb(52, 42, 24 );\n"
                                   "text-align: right;\n"
                                   "font-size:12px;\n"
                                   "height:24px\n"
                                   "}\n"
                                   "QHeaderView {background-color: white;}")
        self.twRoles.setObjectName("twRoles")
        self.twRoles.setColumnCount(1)
        self.twRoles.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.twRoles.setHorizontalHeaderItem(0, item)
        self.gridLayout_2.addWidget(self.twRoles, 2, 0, 1, 3)
        self.lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background : rgb(255,255,255)")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_5.setMinimumSize(QtCore.QSize(94, 0))
        self.label_5.setMaximumSize(QtCore.QSize(94, 16777215))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Agregar Roles"))
        self.btnNuevoRol.setText(_translate("Dialog", "Nuevo"))
        self.btnAceptar.setText(_translate("Dialog", "Aceptar"))
        self.btnCancelar.setText(_translate("Dialog", "Cancelar"))
        item = self.twRoles.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Rol"))
        self.label_5.setText(_translate("Dialog", "Roles:"))
