# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Master_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MasterDialogBase(object):
    def setupUi(self, MasterDialogBase):
        MasterDialogBase.setObjectName("MasterDialogBase")
        MasterDialogBase.resize(400, 300)
        self.button_box = QtWidgets.QDialogButtonBox(MasterDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")

        self.retranslateUi(MasterDialogBase)
        self.button_box.accepted.connect(MasterDialogBase.accept)
        self.button_box.rejected.connect(MasterDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(MasterDialogBase)

    def retranslateUi(self, MasterDialogBase):
        _translate = QtCore.QCoreApplication.translate
        MasterDialogBase.setWindowTitle(_translate("MasterDialogBase", "Master"))

