# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VentanaFusionV3
                                 A QGIS plugin
 VentanaFusionV3
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-07-03
        git sha              : $Format:%H$
        copyright            : (C) 2018 by VentanaFusionV3
        email                : VentanaFusionV3
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .VentanaFusionV3_dialog import VentanaFusionV3Dialog
import os.path

from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QSize
from PyQt5.QtGui import QIcon, QColor, QCursor, QPixmap, QStandardItemModel
from PyQt5.QtWidgets import QAction, QWidget,QVBoxLayout, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5 import QtCore

# Initialize Qt resources from file resources.py
from qgis.core import *
from qgis.utils import iface, loadPlugin, startPlugin, reloadPlugin
from qgis.gui import QgsLayerTreeView, QgsMapToolEmitPoint, QgsMapTool, QgsRubberBand, QgsVertexMarker

# Import the code for the DockWidget
import os.path
import os, json, requests, sys
from osgeo import ogr, osr


class VentanaFusionV3:

    def __init__(self, iface, pluginFD):
        
        self.pluginFD = pluginFD
        self.dlg = VentanaFusionV3Dialog(parent = iface.mainWindow(), DIV = pluginFD)
        #self.dlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # Create the dialog (after translation) and keep reference
        
        self.listaCampos = ['cve_cat', 'clave', 'cve_cat_ant', 'cve_tipo_pred', 'num_ext', 'fondo', 'frente', 'sup_terr', 'uso_predio']
        self.listaEtiquetas = ['Clave Catastral', 'Clave', 'Cve. Cat. Anterior', 'Clave Tipo Predio', 'Numero Exterior', 'Fondo', 'Frente', 'Superficie de terreno', 'Uso de predio']

        self.dlg.btnConfirmar.clicked.connect(self.confirmarFusion)
        self.dlg.btnCancelar.clicked.connect(self.cancelarFusion)
        self.dlg.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.dlg.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.dlg.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)


        self.dlg.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.dlg.tableWidget.setColumnWidth(0, 175)
        self.dlg.tableWidget.setColumnWidth(1, 60)
        self.dlg.tableWidget.setColumnWidth(2, 175)
        self.dlg.tableWidget.setColumnWidth(3, 95)
        self.dlg.tableWidget.setColumnWidth(4, 85)
        self.dlg.tableWidget.setColumnWidth(5, 80)
        self.dlg.tableWidget.setColumnWidth(6, 80)
        self.dlg.tableWidget.setColumnWidth(7, 140)
        self.dlg.tableWidget.setColumnWidth(8, 80)

#---------------------------------------------------------------------------

    def cancelarFusion(self):
        self.pluginFD.enFusion = False
        self.dlg.close()
        self.pluginFD.dlg.btnCargarPredio.setEnabled(True)

#----------------------------------------------------------------------

    def confirmarFusion(self):
        numQueda = sorted(set(index.row() for index in self.dlg.tableWidget.selectedIndexes()))

        if numQueda == None:
            self.pluginFD.UTI.mostrarAlerta('Debes seleccionar un reglon de la tabla', QMessageBox().Critical, 'Error de seleccion')
            return

        if len(numQueda) != 1:
            self.pluginFD.UTI.mostrarAlerta('Debes seleccionar solo un reglon de la tabla', QMessageBox().Critical, 'Error de seleccion')
            return

        numQueda = numQueda[0]
        self.pluginFD.fusionarPredios(numQueda)
        self.dlg.close()
#--------------------------------------------------------------------------

    def llenarTablaComp(self, predio1, predio2):
        
        self.vaciarTabla()
        self.dlg.tableWidget.setRowCount(2)

        for x in range(0, len(self.listaCampos)):

            valItem1 = ''
            valItem2 = ''
            if str(predio1[self.listaCampos[x]]).lower() != 'null':
                valItem1 = str(predio1[self.listaCampos[x]])
                valItem2 = str(predio2[self.listaCampos[x]])

            item1 = QtWidgets.QTableWidgetItem(valItem1)
            item2 = QtWidgets.QTableWidgetItem(valItem2)

            self.dlg.tableWidget.setItem(0, x , item1)
            self.dlg.tableWidget.setItem(1, x , item2)

#------------------------------------------------------
    def vaciarTabla(self): #Vaciar tabla

        self.dlg.tableWidget.clearContents()
        self.dlg.tableWidget.setRowCount(0)

        for row in range(0, self.dlg.tableWidget.rowCount()):        
            self.dlg.tableWidget.removeRow(row) 