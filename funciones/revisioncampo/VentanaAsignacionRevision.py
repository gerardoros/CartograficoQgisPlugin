# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VentanaAsignacionRevision
                                 A QGIS plugin
 VentanaAsignacionRevision
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-06-21
        git sha              : $Format:%H$
        copyright            : (C) 2018 by VentanaAsignacionRevision
        email                : VentanaAsignacionRevision
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
from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5 import QtCore
from PyQt5 import QtWidgets
# Initialize Qt resources from file resources.py

# Import the code for the dialog
from .VentanaAsignacionRevision_dialog import VentanaAsignacionRevisionDialog
import os.path
from qgis.utils import *
import os, json, requests
from osgeo import ogr, osr

class VentanaAsignacionRevision:
    """QGIS Plugin Implementation."""

    def __init__(self, iface, pluginM):
        
        # Save reference to the QGIS interface
        self.iface = iface
        self.pluginM = pluginM
        # Create the dialog (after translation) and keep reference
        self.indexSel = []
        self.dlg = VentanaAsignacionRevisionDialog()
        #self.dlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dlg.tablaMazPred.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.dlg.btnLiberar.clicked.connect(self.preguntarLiberar)
        self.dlg.tablaMazPred.hideColumn(0)
        self.dlg.chkTodo.stateChanged.connect(self.marcarTodoMazPred)
        
        self.dlg.fldUsuario.setReadOnly(True)

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        #self.pluginM.UTI.strechtTabla(self.dlg.tablaMazPred)
        self.traerAsignaciones()
        # Run the dialog event loop
        #result = self.dlg.exec_()
        # See if OK was pressed
        #if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
        #    pass

#--------------------------------------------------------------------------------------------------

    def traerAsignaciones(self):

        indiceUsuario = self.pluginM.dlg.cmbUsuario.currentIndex()
        cveUsuario = self.pluginM.enviosUsuario[indiceUsuario]
        self.usuarioDes = cveUsuario
        nombreCompleto = self.pluginM.dlg.cmbUsuario.itemText(indiceUsuario)
        self.dlg.fldUsuario.setText(nombreCompleto)

        try:
            headers = {'Content-Type': 'application/json', 'Authorization' : self.pluginM.UTI.obtenerToken()}
            respuesta = requests.get(self.pluginM.CFG.urlAsigRevConsultar + cveUsuario, headers = headers)

            if respuesta.status_code == 200:
                
                datos = respuesta.json()
                self.pluginM.vaciarTabla(self.dlg.tablaMazPred)

                for x in range(0, len(datos)):
                    self.dlg.tablaMazPred.insertRow(x)
                    dato = datos[x]
                    
                    cveCatastral = dato['cveCatastral']
                    cveManzana = cveCatastral[0:20]
                    cveManzanaCorta = cveManzana[-3:]
                    cvePredio = cveCatastral[-8:] if len(cveCatastral) == 16 else cveCatastral[-5:]
                    item = QtWidgets.QTableWidgetItem(str(cveCatastral))
                    self.dlg.tablaMazPred.setItem(x, 0 , item)

                    item = QtWidgets.QTableWidgetItem(str(cveManzanaCorta))
                    item.setFlags( QtCore.Qt.ItemIsUserCheckable |  QtCore.Qt.ItemIsEnabled )
                    item.setCheckState(QtCore.Qt.Unchecked)
                    self.dlg.tablaMazPred.setItem(x, 1 , item)

                    item = QtWidgets.QTableWidgetItem(str(cvePredio))
                    self.dlg.tablaMazPred.setItem(x, 2 , item)
                
            else:
                self.pluginM.UTI.mostrarAlerta(str(respuesta), QMessageBox().Critical, "Asignacion de campo")

        except requests.exceptions.RequestException:
            self.pluginM.UTI.mostrarAlerta(str(respuesta), QMessageBox().Critical, "Asignacion de campo")

#--------------------------------------------------------------------------------------------------------

    def preguntarLiberar(self):
        
        self.indexSel = []
        for c in range(0, self.dlg.tablaMazPred.rowCount()):
            if self.dlg.tablaMazPred.item(c, 1).checkState() == QtCore.Qt.Checked:
                self.indexSel.append(c)

        if len(self.indexSel) > 0:
            #self.dlg.setWindowFlags(self.dlg.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
            mensaje = "Desear liberar las asignaciones seleccionadas?"
            
            self.dlg.close()
            respuesta = QMessageBox().question(iface.mainWindow(), "Liberar asignaciones", mensaje, QMessageBox.Yes, QMessageBox.No)
            
            if respuesta == QMessageBox.Yes:
                self.liberarAsignaciones()

            else:
                self.dlg.show()
                self.traerAsignaciones()
            
        else:
            self.pluginM.UTI.mostrarAlerta("No has seleccionado ninguna asignacion a liberar", QMessageBox().Information, 'Liberar asignaciones')


#----------------------------------------------------------------------------------------------------------

    def liberarAsignaciones(self):

        listaEliminar = []
        
        for ix in self.indexSel:
            cveCatastral = str(self.dlg.tablaMazPred.item(ix, 0).text())
            cvePredio = str(self.dlg.tablaMazPred.item(ix, 2).text())
            
            objeto = {}
            objeto['cveCatastral'] = cveCatastral
            objeto['cveUsuario'] = self.usuarioDes

            listaEliminar.append(objeto)

        listaEliminar = json.dumps(listaEliminar)

        try:
            headers = {'Content-Type': 'application/json', 'Authorization' : self.pluginM.UTI.obtenerToken()}
            respuesta = requests.post(self.pluginM.CFG.urlAsigRevEliminar, headers = headers, data = listaEliminar)

            if respuesta.status_code == 200:
                
                self.pluginM.UTI.mostrarAlerta("Desasignacion completa", QMessageBox().Information, "Liberar asignaciones")
                self.dlg.close()
                self.pluginM.llenadoDeTablas()

            else:
                self.pluginM.UTI.mostrarAlerta("Error de servidor v1", QMessageBox().Critical, "Liberar asignaciones")

        except requests.exceptions.RequestException:
            self.pluginM.UTI.mostrarAlerta("Error de servidor v2", QMessageBox().Critical, "Liberar asignaciones")
        
#-----------------------------------------------------------------------------------------

    def marcarTodoMazPred(self):
        if self.dlg.chkTodo.checkState() == QtCore.Qt.Checked:
            if self.dlg.tablaMazPred.rowCount() > 0:
                for c in range(0, self.dlg.tablaMazPred.rowCount()):
                    self.dlg.tablaMazPred.item(c, 1 ).setCheckState(QtCore.Qt.Checked)
            else:
                self.dlg.chkTodo.setCheckState(QtCore.Qt.Unchecked)
        else:
            for c in range(0, self.dlg.tablaMazPred.rowCount()):
                self.dlg.tablaMazPred.item(c, 1 ).setCheckState(QtCore.Qt.Unchecked)     