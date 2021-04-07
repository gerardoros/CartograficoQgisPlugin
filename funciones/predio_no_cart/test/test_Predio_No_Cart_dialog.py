# coding=utf-8
"""Dialog test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'Predio_No_Cart'
__date__ = '2021-03-09'
__copyright__ = 'Copyright 2021, Predio_No_Cart'

import unittest

from qgis.PyQt.QtGui import QDialogButtonBox, QDialog

from Predio_No_Cart_dialog import Predio_No_CartDialog

from utilities import get_qgis_app
QGIS_APP = get_qgis_app()


class Predio_No_CartDialogTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.dialog = Predio_No_CartDialog(None)

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_dialog_ok(self):
        """Test we can click OK."""

        button = self.dialog.button_box.button(QDialogButtonBox.Ok)
        button.click()
        result = self.dialog.result()
        self.assertEqual(result, QDialog.Accepted)

    def test_dialog_cancel(self):
        """Test we can click cancel."""
        button = self.dialog.button_box.button(QDialogButtonBox.Cancel)
        button.click()
        result = self.dialog.result()
        self.assertEqual(result, QDialog.Rejected)

if __name__ == "__main__":
    suite = unittest.makeSuite(Predio_No_CartDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

