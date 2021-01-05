# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_menuDialogBase(object):
    def setupUi(self, menuDialogBase):
        menuDialogBase.setObjectName("menuDialogBase")
        menuDialogBase.resize(863, 799)
        self.dockWidget = QtWidgets.QDockWidget(menuDialogBase)
        self.dockWidget.setGeometry(QtCore.QRect(0, 0, 141, 791))
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.btnAdminUsers = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnAdminUsers.setGeometry(QtCore.QRect(10, 720, 121, 51))
        self.btnAdminUsers.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton::hover{\n"
"background : rgb(104, 69, 13);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton:disabled {\n"
"background: rgb(217, 217, 217)\n"
"}")
        self.btnAdminUsers.setText("")
        self.btnAdminUsers.setIconSize(QtCore.QSize(112, 112))
        self.btnAdminUsers.setObjectName("btnAdminUsers")
        self.btnInterPad = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnInterPad.setGeometry(QtCore.QRect(10, 660, 121, 51))
        self.btnInterPad.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton::hover{\n"
"background : rgb(104, 69, 13);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton:disabled {\n"
"background: rgb(217, 217, 217)\n"
"}")
        self.btnInterPad.setText("")
        self.btnInterPad.setIconSize(QtCore.QSize(112, 112))
        self.btnInterPad.setObjectName("btnInterPad")
        self.despliega = QtWidgets.QPushButton(self.dockWidgetContents)
        self.despliega.setGeometry(QtCore.QRect(9, 0, 121, 50))
        self.despliega.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton::hover{\n"
"background : rgb(104, 69, 13);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton:disabled {\n"
"background: rgb(217, 217, 217)\n"
"}")
        self.despliega.setIconSize(QtCore.QSize(112, 112))
        self.despliega.setObjectName("despliega")
        self.btnAsigCampo = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnAsigCampo.setGeometry(QtCore.QRect(10, 420, 121, 51))
        self.btnAsigCampo.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton::hover{\n"
"background : rgb(104, 69, 13);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton:disabled {\n"
"background: rgb(217, 217, 217)\n"
"}")
        self.btnAsigCampo.setText("")
        self.btnAsigCampo.setIconSize(QtCore.QSize(112, 112))
        self.btnAsigCampo.setObjectName("btnAsigCampo")
        self.btnDibujo = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnDibujo.setGeometry(QtCore.QRect(9, 120, 121, 51))
        self.btnDibujo.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton::hover{\n"
"background : rgb(104, 69, 13);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton:disabled {\n"
"background: rgb(217, 217, 217)\n"
"}")
        self.btnDibujo.setText("")
        self.btnDibujo.setIconSize(QtCore.QSize(112, 112))
        self.btnDibujo.setObjectName("btnDibujo")
        self.btnCargaMasiva = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnCargaMasiva.setGeometry(QtCore.QRect(10, 360, 121, 51))
        self.btnCargaMasiva.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton::hover{\n"
"background : rgb(104, 69, 13);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton:disabled {\n"
"background: rgb(217, 217, 217)\n"
"}")
        self.btnCargaMasiva.setText("")
        self.btnCargaMasiva.setIconSize(QtCore.QSize(112, 112))
        self.btnCargaMasiva.setObjectName("btnCargaMasiva")
        self.btnFusDiv = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnFusDiv.setGeometry(QtCore.QRect(10, 300, 121, 51))
        self.btnFusDiv.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton::hover{\n"
"background : rgb(104, 69, 13);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton:disabled {\n"
"background: rgb(217, 217, 217)\n"
"}")
        self.btnFusDiv.setText("")
        self.btnFusDiv.setIconSize(QtCore.QSize(112, 112))
        self.btnFusDiv.setObjectName("btnFusDiv")
        self.btnAsigRev = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnAsigRev.setGeometry(QtCore.QRect(10, 480, 121, 51))
        self.btnAsigRev.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton::hover{\n"
"background : rgb(104, 69, 13);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton:disabled {\n"
"background: rgb(217, 217, 217)\n"
"}")
        self.btnAsigRev.setText("")
        self.btnAsigRev.setIconSize(QtCore.QSize(112, 112))
        self.btnAsigRev.setObjectName("btnAsigRev")
        self.btnEliminar = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnEliminar.setGeometry(QtCore.QRect(9, 180, 121, 51))
        self.btnEliminar.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton::hover{\n"
"background : rgb(104, 69, 13);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton:disabled {\n"
"background: rgb(217, 217, 217)\n"
"}")
        self.btnEliminar.setText("")
        self.btnEliminar.setIconSize(QtCore.QSize(112, 112))
        self.btnEliminar.setObjectName("btnEliminar")
        self.btnAsigPad = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnAsigPad.setGeometry(QtCore.QRect(10, 540, 121, 51))
        self.btnAsigPad.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton::hover{\n"
"background : rgb(104, 69, 13);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton:disabled {\n"
"background: rgb(217, 217, 217)\n"
"}")
        self.btnAsigPad.setText("")
        self.btnAsigPad.setIconSize(QtCore.QSize(112, 112))
        self.btnAsigPad.setObjectName("btnAsigPad")
        self.btnInterRev = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnInterRev.setGeometry(QtCore.QRect(10, 600, 121, 51))
        self.btnInterRev.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton::hover{\n"
"background : rgb(104, 69, 13);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton:disabled {\n"
"background: rgb(217, 217, 217)\n"
"}")
        self.btnInterRev.setText("")
        self.btnInterRev.setIconSize(QtCore.QSize(112, 112))
        self.btnInterRev.setObjectName("btnInterRev")
        self.btnConsulta = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnConsulta.setGeometry(QtCore.QRect(9, 60, 121, 51))
        self.btnConsulta.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton::hover{\n"
"background : rgb(104, 69, 13);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton:disabled {\n"
"background: rgb(217, 217, 217)\n"
"}")
        self.btnConsulta.setText("")
        self.btnConsulta.setIconSize(QtCore.QSize(112, 112))
        self.btnConsulta.setObjectName("btnConsulta")
        self.btnTopologia = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnTopologia.setGeometry(QtCore.QRect(10, 240, 121, 51))
        self.btnTopologia.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton::hover{\n"
"background : rgb(104, 69, 13);\n"
"color : rgb(255, 255, 255);\n"
"border-radius : 4px;\n"
"}\n"
"QPushButton:disabled {\n"
"background: rgb(217, 217, 217)\n"
"}")
        self.btnTopologia.setText("")
        self.btnTopologia.setIconSize(QtCore.QSize(112, 112))
        self.btnTopologia.setObjectName("btnTopologia")
        self.dockWidget.setWidget(self.dockWidgetContents)
        self.mdiArea = QtWidgets.QMdiArea(menuDialogBase)
        self.mdiArea.setGeometry(QtCore.QRect(180, 0, 671, 791))
        self.mdiArea.setObjectName("mdiArea")
        self.subwindow = QtWidgets.QWidget()
        self.subwindow.setObjectName("subwindow")
        self.radioButton = QtWidgets.QRadioButton(self.subwindow)
        self.radioButton.setGeometry(QtCore.QRect(140, 40, 82, 17))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.subwindow)
        self.radioButton_2.setGeometry(QtCore.QRect(130, 80, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.subwindow_2 = QtWidgets.QWidget()
        self.subwindow_2.setObjectName("subwindow_2")
        self.pushButton = QtWidgets.QPushButton(self.subwindow_2)
        self.pushButton.setGeometry(QtCore.QRect(30, 30, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.subwindow_2)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 80, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(menuDialogBase)
        QtCore.QMetaObject.connectSlotsByName(menuDialogBase)

    def retranslateUi(self, menuDialogBase):
        _translate = QtCore.QCoreApplication.translate
        menuDialogBase.setWindowTitle(_translate("menuDialogBase", "menu"))
        self.despliega.setText(_translate("menuDialogBase", "desplega"))
        self.subwindow.setWindowTitle(_translate("menuDialogBase", "Subwindow"))
        self.radioButton.setText(_translate("menuDialogBase", "RadioButton"))
        self.radioButton_2.setText(_translate("menuDialogBase", "RadioButton"))
        self.subwindow_2.setWindowTitle(_translate("menuDialogBase", "Subwindow"))
        self.pushButton.setText(_translate("menuDialogBase", "PushButton"))
        self.pushButton_2.setText(_translate("menuDialogBase", "PushButton"))

