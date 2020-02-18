# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VentanaClavesV3
                                 A QGIS plugin
 VentanaClavesV3
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-07-03
        git sha              : $Format:%H$
        copyright            : (C) 2018 by VentanaClavesV3
        email                : VentanaClavesV3
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
from .VentanaClavesV3_dialog import VentanaClavesV3Dialog
import os.path

from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QSize
from PyQt5.QtGui import QIcon, QColor, QCursor, QPixmap
from PyQt5.QtWidgets import QAction, QWidget,QVBoxLayout, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QLineEdit
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from qgis.core import *
from qgis.utils import iface, loadPlugin, startPlugin, reloadPlugin
from qgis.gui import QgsLayerTreeView, QgsMapToolEmitPoint, QgsMapTool, QgsRubberBand, QgsVertexMarker

import os.path
import os, json, requests, sys
from osgeo import ogr, osr


class VentanaClavesV3:
    """QGIS Plugin Implementation."""

    def __init__(self, iface, pluginDFS):
        
        self.dlg = VentanaClavesV3Dialog(pluginV=self, parent = iface.mainWindow())
        self.entradaLibre = False
        self.DFS = pluginDFS
        self.listaQuitada = []
        self.listaClaves = []

        self.primeraVez = True
        self.dlg.btnAutomatico.clicked.connect(self.asignacionAutomatica)

        self.dlg.txtClave.setEnabled(False)
        self.capaPredio = QgsProject.instance().mapLayer(self.DFS.ACA.obtenerIdCapa('predios.geom'))
        if self.capaPredio:
            self.capaPredio.selectionChanged.connect(self.cargarAsignacionManual)
        #self.dlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        
        self.dlg.btnClave.clicked.connect(self.asignacionDesManual)
        self.dlg.btnCompletar.clicked.connect(self.completarSubdivision)
        self.dlg.cmbClaves.currentIndexChanged.connect(self.cargarDelCombo)
        self.dlg.btnDesasignarTodo.clicked.connect(self.desasignarTodasClaves)
        self.subCompleta = False
        #self.btnRollback.clicked.connect(self.DFS.rollBack)

        self.dlg.txtClave.setEnabled(False)
        self.dlg.cmbClaves.setEnabled(False)
        self.dlg.btnClave.setEnabled(False)

    def llenar(self, apagarInput):

        self.dlg.cmbClaves.clear()

        #self.rellenarClaves()
        #lista.sort()
        for elemento in self.listaClaves:
            self.dlg.cmbClaves.addItem(elemento)

        if apagarInput:
            self.dlg.txtClave.setEnabled(False)

#------------------------------------------------------------------
    
    def asignacionAutomatica(self):
        
        #cuentaNueva = 49999
        self.capaPredio.startEditing()
        
        rango = len(self.listaClaves)
        listaTrunca = self.listaClaves[1:rango-1]
        rango = len(listaTrunca)

        #totalPredios = [list(self.capaPredio.getFeatures())]
        totalPredios = []
        for predio in self.capaPredio.getFeatures():
            if predio['clave'] == '':
                totalPredios.append(predio)


        cuantosPredios = len(totalPredios)
        listaPredios = []
        if cuantosPredios >= rango:
            listaPredios = totalPredios[0:rango-1]
        else:
            listaPredios = totalPredios
            rango = len(totalPredios)

        for i in range(0, rango):
            feat = totalPredios[i]
            nuevaClave = listaTrunca[i]
            feat['clave'] = nuevaClave
            print('asignamos', nuevaClave)
            if nuevaClave == self.DFS.predioEnDivision['clave']:
                feat['id'] = self.DFS.predioEnDivision['id']
                feat['cve_cat'] = self.DFS.predioEnDivision['cve_cat']

            if nuevaClave in self.listaClaves:
                self.listaClaves.remove(nuevaClave)
                self.listaQuitada.append(nuevaClave)

            self.capaPredio.updateFeature(feat)

        
        self.capaPredio.removeSelection()
        self.DFS.UTI.mostrarAlerta('Claves asignadas', QMessageBox().Information, 'Claves asignadas')
        #seleccion = self.capaPredio.selectedFeatures()
        #if len (seleccion) == 1:
        #    self.dlg.txtClave.setText(self.seleccion[0]['clave'])
        #else:
        #    self.dlg.txtClave.setText('')
            
        self.capaPredio.triggerRepaint()
        self.capaPredio.commitChanges()
        self.dlg.txtClave.setEnabled(False)
        self.dlg.cmbClaves.setEnabled(False)
        self.dlg.btnClave.setEnabled(False)

#------------------------------------------------------------------

    def cargarAsignacionManual(self):
        self.seleccion = self.capaPredio.selectedFeatures()

        if len(self.seleccion) == 1:

            seleccion = self.seleccion[0]
            claveAsignada = seleccion['clave']
            
            
            if seleccion.geometry().asWkt() in self.DFS.listaNuevosPredios: #Cuando es predio nuevo
               
                #self.dlg.btnClave.setEnabled(True)
                if claveAsignada == '':
                    #print('es aquiiii')
                    self.dlg.txtClave.setEnabled(self.entradaLibre)
                    self.dlg.btnClave.setEnabled(True)
                    self.dlg.cmbClaves.setEnabled(True)
                    self.dlg.txtClave.setText('')
                    self.dlg.btnClave.setText('Asignar Clave')
                else:
                    self.dlg.txtClave.setEnabled(False)
                    self.dlg.btnClave.setEnabled(True)
                    self.dlg.cmbClaves.setEnabled(False)
                    self.dlg.txtClave.setText(claveAsignada)
                    self.dlg.btnClave.setText('Desasignar Clave')
            else: #Cuando NO es predio nuevo
                self.dlg.txtClave.setEnabled(False)
                self.dlg.cmbClaves.setEnabled(False)
                self.dlg.btnClave.setEnabled(False)
                
        else: #Cuando la seleccion esta vacia
            self.dlg.txtClave.setEnabled(False)
            self.dlg.cmbClaves.setEnabled(False)
            self.dlg.btnClave.setEnabled(False)

#--------------------------------------------------------------

    def asignacionDesManual(self):
        
        clave = self.seleccion[0]['clave']
        bandera = True

        if clave == '':   #Asignacion

            if self.entradaLibre:      
                texto = self.dlg.txtClave.text()
                mensaje = "Clave asignada: " + texto
                #print('1', texto)
                bandera = False

                pre = ''
                sting = str(texto)
                if len(sting) == 1:
                    pre = '0000'
                elif len(sting) == 2:
                    pre = '000'
                elif len(sting) == 3:
                    pre = '00'
                elif len(sting) == 4:
                    pre = '0'
                
                post = pre + texto

                texto = post
                self.dlg.txtClave.setText(texto)
                #print('2', texto)
                if self.DFS.UTI.esEntero(texto):
                    if len(texto) == 5:
                        bandera = True
            else: #Sin clave libre
                bandera = True
                texto = self.dlg.cmbClaves.currentText()
                mensaje = "Clave asignada: " + texto
                #p#rint('3', texto)
            apagarInput = True

            
        else:    #Desasignacion
            #texto = ''
            texto = self.dlg.txtClave.text()
            mensaje = "Clave desasignada: " + texto
            if texto in self.listaQuitada:
                self.listaClaves.append(texto)
                self.listaQuitada.remove(texto)
            texto = ''
            apagarInput = False

            

        if bandera:

            noRepetida = True

            for feat in self.capaPredio.getFeatures():
                if texto == '':
                    break
                if feat['clave'] == '':
                    continue
                if feat['clave'] == texto:
                    noRepetida = False
                    break

            if noRepetida:
                self.capaPredio.startEditing()
                self.seleccion[0]['clave'] = texto
                

                if texto == self.DFS.predioEnDivision['clave']:
                    self.seleccion[0]['id'] = self.DFS.predioEnDivision['id']
                    self.seleccion[0]['cve_cat'] = self.DFS.predioEnDivision['cve_cat']
                else:
                    self.seleccion[0]['id'] = None
                    self.seleccion[0]['cve_cat'] = ''

                self.capaPredio.updateFeature(self.seleccion[0])
                self.capaPredio.triggerRepaint()
                self.capaPredio.commitChanges()
                if texto != '':
                    if texto in self.listaClaves:
                        self.listaClaves.remove(texto)
                        self.listaQuitada.append(texto)

                self.DFS.UTI.mostrarAlerta(mensaje, QMessageBox().Information, 'Clave asignada')

                #self.capaPredio.removeSelection()

                if clave == '':
                    self.dlg.txtClave.setEnabled(False)
                    self.dlg.cmbClaves.setEnabled(False)
                    self.dlg.txtClave.setText(texto)
                    self.dlg.btnClave.setText('Desasignar Clave')
                else:

                    self.dlg.txtClave.setEnabled(True)
                    self.dlg.cmbClaves.setEnabled(True)
                    self.dlg.btnClave.setEnabled(True)
                    self.dlg.btnClave.setText('Asignar Clave')

                self.llenar(apagarInput)
            else:
                self.DFS.UTI.mostrarAlerta('La clave ya ha sido asignada', QMessageBox().Critical, 'Error de asignacion')
        else:
            self.DFS.UTI.mostrarAlerta('La clave debe constar de 5 numeros', QMessageBox().Information, 'Clave asignada')

#---------------------------------------------------------------------------------

    def completarSubdivision(self):

        bandera = True

        for feat in self.capaPredio.getFeatures():
            if feat.geometry().asWkt() in self.DFS.listaNuevosPredios:
                if feat['clave'] == '':
                    bandera = False
                    break
        
        if bandera:

            bandera = False
            for feat in self.capaPredio.getFeatures():
                
                if feat['clave'] == self.DFS.predioEnDivision['clave']:
                    bandera = True
                    break

            if bandera:
                self.DFS.UTI.mostrarAlerta('Subdivision completa', QMessageBox().Information, 'Subdivision completa, Parte 2 de 2')
                self.dlg.close()
                self.DFS.dlg.close()
                self.primeraVez = True
                self.DFS.enClaves = False
                self.subCompleta = True
                self.dlg.close()
                self.subCompleta = False
                self.DFS.VentanaAreas.close()
                self.DFS.vaciarRubbers()
                #self.rellenarClaves()
                #self.llenar(
            else:
                self.DFS.UTI.mostrarAlerta('No puedes continuar hasta que un predio contenga la clave: ' + str(self.DFS.predioEnDivision['clave']), QMessageBox().Critical, 'Error al completar subdivision')
        else:
            self.DFS.UTI.mostrarAlerta('No puedes continuar hasta que todos los predios resultados de la subdivision\ntengan clave asignada', QMessageBox().Critical, 'Error al completar subdivision')

#--------------------------------------------------------------------------------------

    def desasignarTodasClaves(self):
        for feat in self.capaPredio.getFeatures():
            if feat.geometry().asWkt() in self.DFS.listaNuevosPredios:
                self.capaPredio.startEditing()
                feat['clave'] = ''
                feat['id'] = None
                feat['cve_cat'] = ''
                self.capaPredio.updateFeature(feat)
                self.capaPredio.triggerRepaint()
                self.capaPredio.commitChanges()

#----------------------------------------------------------------------------------------------

    def cargarDelCombo(self):

        #if len(self.seleccion) == 1:
        self.entradaLibre = self.dlg.cmbClaves.currentIndex() == 0
        
        self.dlg.txtClave.setEnabled(self.entradaLibre)
        
        if self.primeraVez:
            self.dlg.txtClave.setEnabled(False)
            self.primeraVez = False

    
#----------------------------------------------------------

    def rellenarClaves(self):

        try:
            idp = self.DFS.predioEnDivision['clave']
            self.listaClaves = [ 'ENTRADA MANUAL', str(idp), '10101', '20202', '30303']
        except:
            return