# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'estatusClaves_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EstatusClaveDialogBase(object):
    def setupUi(self, EstatusClaveDialogBase):
        EstatusClaveDialogBase.setObjectName("EstatusClaveDialogBase")
        EstatusClaveDialogBase.resize(316, 166)
        EstatusClaveDialogBase.setMinimumSize(QtCore.QSize(315, 165))
        EstatusClaveDialogBase.setMaximumSize(QtCore.QSize(316, 166))
        EstatusClaveDialogBase.setStyleSheet("QDialog{\n"
"background : rgb(250,238,224);\n"
"}\n"
"")
        self.gridLayout = QtWidgets.QGridLayout(EstatusClaveDialogBase)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(EstatusClaveDialogBase)
        self.widget.setStyleSheet("QWidget{\n"
"background : rgb(255,255,255);\n"
"}")
        self.widget.setObjectName("widget")
        self.botonAgregar = QtWidgets.QPushButton(self.widget)
        self.botonAgregar.setGeometry(QtCore.QRect(60, 100, 81, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.botonAgregar.setFont(font)
        self.botonAgregar.setStyleSheet("QPushButton{\n"
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
        self.botonAgregar.setObjectName("botonAgregar")
        self.botonCancelar = QtWidgets.QPushButton(self.widget)
        self.botonCancelar.setGeometry(QtCore.QRect(160, 100, 81, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.botonCancelar.setFont(font)
        self.botonCancelar.setStyleSheet("QPushButton{\n"
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
        self.botonCancelar.setObjectName("botonCancelar")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(10, 10, 271, 21))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.labelTituloEditar = QtWidgets.QLabel(self.widget)
        self.labelTituloEditar.setGeometry(QtCore.QRect(30, 40, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.labelTituloEditar.setFont(font)
        self.labelTituloEditar.setObjectName("labelTituloEditar")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(140, 40, 113, 20))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.labelTituloEditar_2 = QtWidgets.QLabel(self.widget)
        self.labelTituloEditar_2.setGeometry(QtCore.QRect(30, 70, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.labelTituloEditar_2.setFont(font)
        self.labelTituloEditar_2.setObjectName("labelTituloEditar_2")
        self.comboManzana = QtWidgets.QComboBox(self.widget)
        self.comboManzana.setGeometry(QtCore.QRect(140, 70, 113, 22))
        self.comboManzana.setStyleSheet("QComboBox QAbstractItemView::item { min-height: 25; font-family: \"Century Gothic\";}\n"
"QListView{color: black ; font-size: 16px; outline:none; font-weight:bold; font-family: \"Century Gothic\";}\n"
"\n"
"QComboBox{\n"
"background : rgb(250,238,224);\n"
"}\n"
"QComboBox:item:selected {\n"
"color: black ;\n"
"}")
        self.comboManzana.setObjectName("comboManzana")
        self.comboManzana.addItem("")
        self.comboManzana.addItem("")
        self.gridLayout.addWidget(self.widget, 0, 1, 1, 1)

        self.retranslateUi(EstatusClaveDialogBase)
        QtCore.QMetaObject.connectSlotsByName(EstatusClaveDialogBase)

    def retranslateUi(self, EstatusClaveDialogBase):
        _translate = QtCore.QCoreApplication.translate
        EstatusClaveDialogBase.setWindowTitle(_translate("EstatusClaveDialogBase", "Claves"))
        self.botonAgregar.setText(_translate("EstatusClaveDialogBase", "Confirmar"))
        self.botonCancelar.setText(_translate("EstatusClaveDialogBase", "Cancelar"))
        self.label.setText(_translate("EstatusClaveDialogBase", "Nuevo estatus de la clave anterior"))
        self.labelTituloEditar.setText(_translate("EstatusClaveDialogBase", "Clave anterior:"))
        self.lineEdit.setText(_translate("EstatusClaveDialogBase", "001"))
        self.labelTituloEditar_2.setText(_translate("EstatusClaveDialogBase", "Estatus:"))
        self.comboManzana.setItemText(0, _translate("EstatusClaveDialogBase", "INACTIVA"))
        self.comboManzana.setItemText(1, _translate("EstatusClaveDialogBase", "ACTIVA"))

