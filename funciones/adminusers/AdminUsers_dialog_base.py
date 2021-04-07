# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AdminUsers_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AdminUsersDialogBase(object):
    def setupUi(self, AdminUsersDialogBase):
        AdminUsersDialogBase.setObjectName("AdminUsersDialogBase")
        AdminUsersDialogBase.resize(400, 300)
        self.button_box = QtWidgets.QDialogButtonBox(AdminUsersDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")

        self.retranslateUi(AdminUsersDialogBase)
        self.button_box.accepted.connect(AdminUsersDialogBase.accept)
        self.button_box.rejected.connect(AdminUsersDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(AdminUsersDialogBase)

    def retranslateUi(self, AdminUsersDialogBase):
        _translate = QtCore.QCoreApplication.translate
        AdminUsersDialogBase.setWindowTitle(_translate("AdminUsersDialogBase", "AdminUsers"))

