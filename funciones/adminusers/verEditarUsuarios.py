# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'verEditarUsuarios.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(570, 470)
        Dialog.setMinimumSize(QtCore.QSize(570, 430))
        Dialog.setMaximumSize(QtCore.QSize(570, 470))
        Dialog.setStyleSheet("background-color: white;")
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setStyleSheet("background : rgb(250,238,224)")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 550, 450))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lbContrDos = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lbContrDos.setMinimumSize(QtCore.QSize(94, 0))
        self.lbContrDos.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbContrDos.setFont(font)
        self.lbContrDos.setObjectName("lbContrDos")
        self.gridLayout.addWidget(self.lbContrDos, 5, 2, 1, 2)
        self.lbContrUno = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lbContrUno.setMinimumSize(QtCore.QSize(94, 0))
        self.lbContrUno.setMaximumSize(QtCore.QSize(94, 16777215))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbContrUno.setFont(font)
        self.lbContrUno.setObjectName("lbContrUno")
        self.gridLayout.addWidget(self.lbContrUno, 5, 0, 1, 1)
        self.leContrDos = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.leContrDos.setMinimumSize(QtCore.QSize(257, 25))
        self.leContrDos.setMaximumSize(QtCore.QSize(8000, 25))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.leContrDos.setFont(font)
        self.leContrDos.setStyleSheet("background : rgb(255,255,255)")
        self.leContrDos.setObjectName("leContrDos")
        self.gridLayout.addWidget(self.leContrDos, 6, 2, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setMinimumSize(QtCore.QSize(94, 0))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)
        self.leCorreo = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.leCorreo.setMinimumSize(QtCore.QSize(257, 25))
        self.leCorreo.setMaximumSize(QtCore.QSize(500, 25))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.leCorreo.setFont(font)
        self.leCorreo.setStyleSheet("background : rgb(255,255,255)")
        self.leCorreo.setObjectName("leCorreo")
        self.gridLayout.addWidget(self.leCorreo, 7, 1, 1, 2)
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setMinimumSize(QtCore.QSize(94, 0))
        self.label.setMaximumSize(QtCore.QSize(94, 16777215))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.btnAgregaRoles = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btnAgregaRoles.setMinimumSize(QtCore.QSize(130, 30))
        self.btnAgregaRoles.setMaximumSize(QtCore.QSize(130, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnAgregaRoles.setFont(font)
        self.btnAgregaRoles.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255)\n"
"}\n"
"QPushButton::disabled {\n"
"background : rgb(187, 129, 13);\n"
"color : rgb(245,245,245);\n"
"border: 1px solid #adb2b5;\n"
"}")
        self.btnAgregaRoles.setObjectName("btnAgregaRoles")
        self.gridLayout.addWidget(self.btnAgregaRoles, 8, 3, 1, 1, QtCore.Qt.AlignRight)
        self.leContrUno = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.leContrUno.setMinimumSize(QtCore.QSize(257, 25))
        self.leContrUno.setMaximumSize(QtCore.QSize(8000, 25))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.leContrUno.setFont(font)
        self.leContrUno.setStyleSheet("background : rgb(255,255,255)")
        self.leContrUno.setObjectName("leContrUno")
        self.gridLayout.addWidget(self.leContrUno, 6, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_4.setMinimumSize(QtCore.QSize(94, 0))
        self.label_4.setMaximumSize(QtCore.QSize(94, 16777215))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setMinimumSize(QtCore.QSize(94, 0))
        self.label_3.setMaximumSize(QtCore.QSize(94, 16777215))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.leApellidos = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.leApellidos.setMinimumSize(QtCore.QSize(257, 25))
        self.leApellidos.setMaximumSize(QtCore.QSize(257, 25))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.leApellidos.setFont(font)
        self.leApellidos.setStyleSheet("background : rgb(255,255,255)")
        self.leApellidos.setObjectName("leApellidos")
        self.gridLayout.addWidget(self.leApellidos, 1, 2, 1, 2)
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
        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)
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
        self.twRoles.setColumnCount(2)
        self.twRoles.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.twRoles.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.twRoles.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.twRoles, 9, 0, 1, 4)
        self.leUsuario = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.leUsuario.setMinimumSize(QtCore.QSize(257, 25))
        self.leUsuario.setMaximumSize(QtCore.QSize(800, 25))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.leUsuario.setFont(font)
        self.leUsuario.setStyleSheet("background : rgb(255,255,255)")
        self.leUsuario.setObjectName("leUsuario")
        self.gridLayout.addWidget(self.leUsuario, 4, 1, 1, 2)
        self.leNombres = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.leNombres.setMinimumSize(QtCore.QSize(257, 25))
        self.leNombres.setMaximumSize(QtCore.QSize(8000, 25))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.leNombres.setFont(font)
        self.leNombres.setStyleSheet("background : rgb(255,255,255)")
        self.leNombres.setObjectName("leNombres")
        self.gridLayout.addWidget(self.leNombres, 1, 0, 1, 2)
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
        self.gridLayout.addWidget(self.btnCancelar, 10, 3, 1, 1)
        self.btnOk = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btnOk.setMinimumSize(QtCore.QSize(130, 30))
        self.btnOk.setMaximumSize(QtCore.QSize(130, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnOk.setFont(font)
        self.btnOk.setStyleSheet("QPushButton{\n"
"background : rgb(174, 116, 0);\n"
"color : rgb(255, 255, 255)\n"
"}\n"
"QPushButton::disabled {\n"
"background : rgb(187, 129, 13);\n"
"color : rgb(245,245,245);\n"
"border: 1px solid #adb2b5;\n"
"}")
        self.btnOk.setObjectName("btnOk")
        self.gridLayout.addWidget(self.btnOk, 10, 2, 1, 1)
        self.cbActivado = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.cbActivado.setFont(font)
        self.cbActivado.setStyleSheet("QCheckBox::indicator:unchecked {\n"
"image : url(:/plugins/AdminUsers/icons/uncheck.png);\n"
"    width: 20px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    image: url(:/plugins/AdminUsers/icons/check.png);\n"
"\n"
"    width: 25px;\n"
"    height: 25px;\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked:disabled {\n"
"image : url(:/plugins/AdminUsers/icons/uncheck_disable.png);\n"
"    width: 20px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked:disabled{\n"
"    image: url(:/plugins/AdminUsers/icons/check_disabled.png);\n"
"\n"
"    width: 25px;\n"
"    height: 25px;\n"
"}\n"
"\n"
"\n"
"\n"
"QCheckBox {\n"
"    spacing: 4px;\n"
"    outline: none;\n"
"    padding-top: 4px;\n"
"    padding-bottom: 4px;\n"
"}\n"
"\n"
"QCheckBox:focus {\n"
"    border: none;\n"
"}\n"
"\n"
"QCheckBox QWidget:disabled {\n"
"    background-color: #19232D;\n"
"    color: #787878;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    margin-left: 4px;\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}")
        self.cbActivado.setChecked(False)
        self.cbActivado.setObjectName("cbActivado")
        self.gridLayout.addWidget(self.cbActivado, 2, 0, 1, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Usuario"))
        self.lbContrDos.setText(_translate("Dialog", "Confirmar Contraseña:"))
        self.lbContrUno.setText(_translate("Dialog", "Contraseña:"))
        self.label_2.setText(_translate("Dialog", "Correo:"))
        self.label.setText(_translate("Dialog", "Usuario:"))
        self.btnAgregaRoles.setText(_translate("Dialog", "Agregar Roles"))
        self.label_4.setText(_translate("Dialog", "Apellido (s):"))
        self.label_3.setText(_translate("Dialog", "Nombre (s):"))
        self.label_5.setText(_translate("Dialog", "Roles:"))
        item = self.twRoles.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Rol"))
        self.btnCancelar.setText(_translate("Dialog", "Cancelar"))
        self.btnOk.setText(_translate("Dialog", "Guardar"))
        self.cbActivado.setText(_translate("Dialog", "Activado"))

