# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EliminacionV3
                                 A QGIS plugin
 EliminacionV3
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-07-02
        git sha              : $Format:%H$
        copyright            : (C) 2018 by EliminacionV3
        email                : EliminacionV3
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
from .EliminacionV3_dialog import EliminacionV3Dialog
import os.path

from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QSize
from PyQt5.QtGui import QIcon, QColor, QCursor, QPixmap
from PyQt5.QtWidgets import QAction, QWidget,QVBoxLayout, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5 import QtWidgets

from qgis.gui import * #QgsLayerTreeView, QgsMapToolEmitPoint, QgsMapTool, QgsRubberBand, QgsVertexMarker
from qgis.core import * #QgsProject
from qgis.utils import *

import os.path

class EliminacionV3:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        
        self.CFG = None
        self.UTI = None
        self.DFS = None
        self.DBJ = None
        self.ACA = None
        self.DFS = None
        self.TPG = None

        self.pluginIsActive = False
        self.dockwidget = EliminacionV3Dialog(parent = iface.mainWindow())

        self.listaEliminadaCompleta = []
        self.listaEliminadaCompletaRef = []
        self.tablas = {'manzana': 'e_manzana', 
        'predios.geom': 'e_predio', 
        'construcciones': 'e_construccion',
        'horizontales.geom':'e_condominio_horizontal',
        'verticales':'e_condominio_vertical',
        'cves_verticales':'e_condominio_vert_clave',
        'Estado' : 'e_estado',
        'Region Catastral' : 'e_region_carto',
        'Municipios' : 'e_municipio',
        'Secciones' : 'e_seccion',		
        'Localidades' : 'e_localidad',
        'Sectores' : 'e_sector',
        'Manzanas' : 'e_manzana',
        'Predios' : 'e_predio',
        'Calles' : 'e_calle',
        'Colonias' : 'e_colonia',
        'Codigo Postal' : 'e_cp',
        'Zona Uno' : 'e_zona_uno',
        'Zona Dos' : 'e_zona_dos',
        'Area de Valor' : 'e_area_valor'
        }

        self.tablasReferencias = {
        'Estado' : 'e_estado',
        'Region Catastral' : 'e_region_carto',
        'Municipios' : 'e_municipio',
        'Secciones' : 'e_seccion',		
        'Localidades' : 'e_localidad',
        'Sectores' : 'e_sector',
        'Manzanas' : 'e_manzana',
        'Predios' : 'e_predio',
        'Calles' : 'e_calle',
        'Colonias' : 'e_colonia',
        'Codigo Postal' : 'e_cp',
        'Zona Uno' : 'e_zona_uno',
        'Zona Dos' : 'e_zona_dos',
        'Area de Valor' : 'e_area_valor'
        }
        self.dockwidget.botonEliminar.clicked.connect(self.alternarEliminar)

        self.capasConFuncion = []
        
        self.capasRecapeadas = []

        self.capaManzana = None
        self.capaPrediosGeom = None
        self.capaPrediosNum = None
        self.capaConstrucciones = None
        self.capaHorizontalesGeom = None
        self.capaHorizontalesNum = None
        self.capaVerticales = None
        self.capaCvesVert = None

        self.capaEstado = None
        self.capaMunicipios = None
        self.capaRegion = None
        self.capaSecciones = None
        self.capaLocalidades = None
        self.capaSectores = None

        self.capaCalles = None
        self.capaColonias = None
        self.capaCP = None
        self.capaZona1 = None
        self.capaZona2 = None
        self.capaArea = None
        self.modoEliminar = False
        self.capaVictima = None

        
        #self.dockwidget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # Declare instance attributes
        '''
        self.actions = []
        self.menu = self.tr(u'&EliminacionV3')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'EliminacionV3')
        self.toolbar.setObjectName(u'EliminacionV3')
        '''

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('EliminacionV3', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/EliminacionV3/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'EliminacionV3'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&EliminacionV3'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dockwidget.show()
        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING EliminarPoligonos"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = EliminarPoligonosDockWidget()

            # connect to provide cleanup on closing of dockwidget


            # show the dockwidget
            # TODO: fix to allow choice of dock location

            self.dockwidget.show()
            iface.currentLayerChanged.connect(self.agregarFuncionEliminar)
        result = self.dockwidget.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    ########################################################################################################

    def agregarFuncionEliminar(self):
        
        if iface.activeLayer() != None and self.esCapaChida:
            if not iface.activeLayer() in self.capasConFuncion:
                if not iface.activeLayer().id() == self.ACA.traducirIdCapa('Predios') and not iface.activeLayer().id() == self.ACA.traducirIdCapa('Manzanas'):
                    #nombreCapa = self.ACA.traducirIdCapa( iface.activeLayer().id())
                    if self.ACA.esCapaReferencia(iface.activeLayer().id()):
                        print('entra aquiiii vato')
                        iface.activeLayer().selectionChanged.connect(self.cargarEliminar)
                        self.capasConFuncion.append(iface.activeLayer())


#########################################################################

    def esCapaChida(self):
        if iface.activeLayer().id() == self.ACA.obtenerIdCapa('manzana'):
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('predios.geom'):
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('predios.num'):
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('construcciones'):
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('horizontales.geom'):
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('horizontales.num'):
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('verticales'):
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('cves_verticales'):
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('Area de Valor'): #Areas de valor
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('Zona Uno') or iface.activeLayer().id() == self.ACA.obtenerIdCapa('Zona Dos'): #Zonas
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('Predios'): #Zonas
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('Colonias'): #Codigo Postal
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('Codigo Postal'): #Colonia
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('Calles'): #Calles
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('Sectores'): #Sector
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('Localidades'): #Localidades
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('Secciones'): #Secciones
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('Municipios'): #Municipios
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('Region Catastral'): #Region Catastral
            return True
        elif iface.activeLayer().id() == self.ACA.obtenerIdCapa('Estado'): #Estado
            return True
        else:
            return False

######################################################################################################

    



    def cargarEliminar(self):

        self.capaActiva = iface.activeLayer()
        nombreCapa = self.ACA.traducirIdCapa( self.capaActiva.id())



        if self.modoEliminar and ( (not self.ACA.esCapaReferencia(nombreCapa)) or nombreCapa == self.pluginM.ACA.capaEnEdicion ):
            
            self.seleccion = self.capaActiva.selectedFeatures()

            if len(self.seleccion) > 1:
                self.UTI.mostrarAlerta('Solo debes seleccionar un elemento', QMessageBox().Critical, 'Error de seleccion')
            elif len(self.seleccion) == 1:

                feat = self.seleccion[0]
                if nombreCapa == 'manzana':
                    mensajeCapa = 'Manzana con clave: ' + str(feat['clave']) + '\nNOTA: Se eliminaran todos los predios, construcciones y condominios contenidos en la manzana'
                elif nombreCapa == 'predios.geom':
                    mensajeCapa = 'Predio con clave: ' + str(feat['clave']) + '\nNOTA: Se eliminaran todos las construcciones y condominios contenidos en el predio'
                elif nombreCapa == 'predios.num':
                    mensajeCapa = 'Predio con numero exterior: ' + str(feat['numExt'])
                elif nombreCapa == 'construcciones':
                    mensajeCapa = 'Construccion con Nombre de volumen: ' + str(feat['nom_volumen']) + '\n'
                elif nombreCapa == 'horizontales.geom':
                    mensajeCapa = 'Condominio horizontal con clave: ' + str(feat['clave']) + '\nNOTA: Se eliminaran todos los numeros oficiales del condominio'
                elif nombreCapa == 'horizontales.num':
                    mensajeCapa = 'Condominio horizontal con numero oficial: ' + str(feat['num_ofi'])
                elif nombreCapa == 'verticales':
                    mensajeCapa = 'Condominio vertical con clave: ' + str(feat['clave']) +  '\nNOTA: Se eliminaran todas las claves verticales del condominio'
                elif nombreCapa == 'cves_verticales':
                    mensajeCapa = 'Clave vertical: ' + str(feat['clave']) 

                elif nombreCapa == 'Estado':
                    mensajeCapa = 'Estado: ' + str(feat['nombre']) +  '\nNOTA: Se eliminaran todas las regiones, municipios, secciones, localidades y sectores del estado'
                elif nombreCapa == 'Region Catastral':
                    mensajeCapa = 'Region Catastral: ' + str(feat['clave']) +  '\nNOTA: Se eliminaran todas los municipios, secciones, localidades y sectores de la region catastral'
                elif nombreCapa == 'Municipios':
                    mensajeCapa = 'Municipio: ' + str(feat['nombre']) +  '\nNOTA: Se eliminaran todas las secciones, localidades y sectores del municipio'
                elif nombreCapa == 'Secciones':
                    mensajeCapa = 'Seccion: ' + str(feat['clave']) +  '\nNOTA: Se eliminaran todas las localidades y sectores de la seccion'
                elif nombreCapa == 'Localidades':
                    mensajeCapa = 'Seccion: ' + str(feat['nombre']) +  '\nNOTA: Se eliminaran todos los sectores de la localidad'
                elif nombreCapa == 'Sectores':
                    mensajeCapa = 'Seccion: ' + str(feat['nombre']) +  '\n'

                elif nombreCapa == 'Calles':
                    mensajeCapa = 'Calle: ' + str(feat['calle']) 
                elif nombreCapa == 'Colonias':
                    mensajeCapa = 'Colonia: ' + str(feat['descripcion']) 
                elif nombreCapa == 'Codigo Postal':
                    mensajeCapa = 'Codigo Postal: ' + str(feat['cve_cp'])
                elif nombreCapa == 'Zona Uno':
                    mensajeCapa = 'Zona Uno: ' + str(feat['descripcion'])
                elif nombreCapa == 'Zona Dos':
                    mensajeCapa = 'Zona Dos: ' + str(feat['descripcion'])
                elif nombreCapa == 'Area de Valor':
                    mensajeCapa = 'Area de Valor: ' + str(feat['descripcion'])

                mensaje = "Deseas eliminar? \n" + mensajeCapa
                respuesta = QMessageBox.question(iface.mainWindow(), "Eliminar elemento", mensaje, QMessageBox.Yes, QMessageBox.No)

                if respuesta == QMessageBox.Yes:
                    self.eliminacionConjunta()

#############################################################################################################

    def eliminacionConjunta(self):
        self.capaActiva.startEditing()
        self.listaEliminadaCompleta = []
        self.listaEliminadaCompletaRef = []
        nombreCapa = self.ACA.traducirIdCapa( self.capaActiva.id())

        if nombreCapa == 'manzana':
            self.eliminarYGuardarInterseccion(self.ACA.obtenerIdCapa('predios.geom'))
            self.eliminarYGuardarInterseccion(self.ACA.obtenerIdCapa('construcciones'))
            self.eliminarYGuardarInterseccion(self.ACA.obtenerIdCapa('horizontales.geom'))
            self.eliminarYGuardarInterseccion(self.ACA.obtenerIdCapa('verticales'))
            self.eliminarYGuardarInterseccion(self.ACA.obtenerIdCapa('cves_verticales'))
        elif nombreCapa == 'predios.geom':
            self.eliminarYGuardarInterseccion(self.ACA.obtenerIdCapa('construcciones'))
            self.eliminarYGuardarInterseccion(self.ACA.obtenerIdCapa('horizontales.geom'))
            self.eliminarYGuardarInterseccion(self.ACA.obtenerIdCapa('verticales'))
            self.eliminarYGuardarInterseccion(self.ACA.obtenerIdCapa('cves_verticales'))
        elif nombreCapa == 'horizontales.geom':
            self.eliminarYGuardarInterseccion(self.ACA.obtenerIdCapa('construcciones'))
        elif nombreCapa == 'verticales':
            self.eliminarYGuardarInterseccion(self.ACA.obtenerIdCapa('cves_verticales'))
        
        self.capaVictima = self.capaActiva
        self.eliminarYGuardar(self.seleccion[0])
        self.capaActiva.removeSelection()
        self.capaActiva.triggerRepaint()
        self.capaActiva.commitChanges()
        listaTemp = QSettings().value('listaEliminada')
        listaTempRef = QSettings().value('listaEliminadaRef')   
        for feat in self.listaEliminadaCompleta:
            listaTemp.append(feat)
        for feat in self.listaEliminadaCompletaRef:
            listaTempRef.append(feat)
        QSettings().setValue('listaEliminada', listaTemp)
        QSettings().setValue('listaEliminadaRef', listaTempRef)

####################################################################################################




    def eliminarYGuardarInterseccion(self, capaVictima):

        self.capaVictima = QgsProject.instance().mapLayer(capaVictima)

        if self.capaVictima == None:
            return

        geoSel = self.seleccion[0].geometry()
        features = self.capaVictima.getFeatures()
        
        self.capaVictima.startEditing()

        capaSel = self.obtenerCapa(self.seleccion[0])

        aTumbar = []

        salidos = []

        for feat in features: #Los features que aun con buffer negativo toquen dentro, se eliminan
            bufferNeg = feat.geometry().buffer(-0.0001, 1)
            if geoSel.intersects(bufferNeg):
                aTumbar.append(feat)
            else: #Los que no, pasan a otra seccion
                salidos.append(feat)

        tocados = []

        for feat in salidos: #De todos los poligonos salidos vemos cuales son tocados por el feat seleccionado
            bufferPos = feat.geometry().buffer(0.00001, 1)
            if geoSel.intersects(bufferPos):
                tocados.append(feat)

        for feat in tocados: #De los tocados obtenemos todos los de la capa seleccionada que tocan
            listaCompartida = []

            for conten in capaSel.getFeatures():
                
                if conten.geometry().intersects(feat.geometry().buffer(0.00001, 1)):
                    listaCompartida.append(conten)

            area = 0
            objetivo = None
            for comp in listaCompartida: #Comparamos las areas y obtenemos el area mayor
                temp = comp.geometry().intersection(feat.geometry().buffer(0.00001, 1)).area()

                if temp > area:
                    area = temp
                    objetivo = comp

            if objetivo.geometry().equals(self.seleccion[0].geometry()): #Si el objeto con area mayor es el mismo que nuestra seleccion entonces se borra
                aTumbar.append(feat)

        for victimas in aTumbar: #Borramos
            self.eliminarYGuardar(victimas)

        self.capaVictima.triggerRepaint()
        self.capaVictima.commitChanges()

####################################################################################################

    def eliminarYGuardarInterseccionDirecta(self, capaVictima):

        self.capaVictima = QgsProject.instance().mapLayer(capaVictima)
        
        if self.capaVictima == None:
            return

        geoSel = self.seleccion[0].geometry()
        victimas = self.capaVictima.getFeatures()

        for feat in victimas: #Los features que aun con buffer negativo toquen dentro, se eliminan
            bufferNeg = geoSel.buffer(-0.0001, 1)
            if bufferNeg.intersects(feat.geometry()):
                self.eliminarYGuardar(feat)

##########################################################################################################

    def eliminarExteriores(self, feat):

        capa = self.obtenerCapa(feat)
        if capa.id() == self.ACA.obtenerIdCapa( 'predios.geom'):
            capaPuntos = QgsProject.instance().mapLayer(self.ACA.obtenerIdCapa('predios.num'))
        elif capa.id() == self.ACA.obtenerIdCapa( 'horizontales.geom'):
            capaPuntos = QgsProject.instance().mapLayer(self.ACA.obtenerIdCapa('horizontales.num'))

        puntoOficial = None
        for punto in capaPuntos.getFeatures():
            if punto.geometry().intersects(feat.geometry()):
                puntoOficial = punto
                
        if puntoOficial != None:
            #if capa.id() == self.ACA.obtenerIdCapa('predios.geom'):
            #    feat['numExt'] = puntoOficial['numExt']
            #   feat['geom_num'] = puntoOficial.geometry().asWkt()
            #elif capa.id() == self.ACA.obtenerIdCapa('horizontales.geom'):
            #    feat['num_ofi'] = punto['num_ofi']
            #    feat['geom_num'] = punto.geometry().asWkt()
            
            capaPuntos.startEditing()
            capaPuntos.dataProvider().deleteFeatures([puntoOficial.id()])
            capaPuntos.triggerRepaint()
            capaPuntos.commitChanges()

#############################################################################################################

    def eliminarYGuardar(self, feat):

        #capa = self.obtenerCapa(feat)
        if self.capaVictima != None:
            capa = self.capaVictima
        else:
            capa = QgsProject.instance().mapLayer(self.ACA.obtenerIdCapa('predios.geom'))

        
        #print(capa.name())

        #print('tumbamos' + str(capa.name()))
        if not self.ACA.esCapaReferencia(capa.id()):
            campos = {}
            campos['wkt'] = feat.geometry().asWkt()
            campos['srid'] = 32614

            if (capa.id() != self.ACA.obtenerIdCapa('predios.num') and capa.id() != self.ACA.obtenerIdCapa('horizontales.num')):
                campos['tabla'] = self.tablas[self.ACA.traducirIdCapa( capa.id())]
                atributos = {}
                nombresAtrbutos = capa.fields()   

                nombres = [campo.name() for campo in nombresAtrbutos]

                if capa.id() == self.ACA.obtenerIdCapa('predios.geom') or capa.id() == self.ACA.obtenerIdCapa('horizontales.geom'):
                    self.eliminarExteriores(feat)

                for x in range(0, len(nombres)):
                    atributo = feat.attributes()[x]
                    if str(feat.attributes()[x]) == "NULL":
                        atributo = None
                    atributos[str(nombres[x])] = atributo
                    
                campos['attr'] = atributos

                if campos['attr']['id'] == None:
                    campos['nuevo'] = True
                    campos['eliminado'] = True
                else:
                    campos['nuevo'] = False
                    campos['eliminado'] = True
            
                self.listaEliminadaCompleta.append(campos)

        else:
            capa.setReadOnly(False)

            campos = {}
            campos['geomWKT'] = feat.geometry().asWkt()
            campos['srid'] = 32614
            campos['nombre'] = self.tablasReferencias[capa.name()]
            atributos = {}
            nombresAtrbutos = capa.fields()   

            nombres = [campo.name() for campo in nombresAtrbutos]

            for x in range(0, len(nombres)):
                atributo = feat.attributes()[x]
                if str(feat.attributes()[x]) == "NULL":
                    atributo = None
                atributos[str(nombres[x])] = atributo
                
            campos['propiedades'] = atributos
            campos['accion'] = 'delete'

            if campos['propiedades']['id'] != None:
                self.listaEliminadaCompletaRef.append(campos)



        capa.startEditing()
        capa.dataProvider().deleteFeatures([feat.id()])
        capa.triggerRepaint()
        capa.commitChanges()

        #if self.ACA.esCapaReferencia(capa.name()) and capa.name() !=:
        #    capa.setReadOnly(True)

############################################################################################################

    def obtenerCapa(self, feat):

        self.recapeoCompleto()

        for capa in self.capasRecapeadas:
            if feat.fields() == capa.fields():
                return capa
        
        return None

#########################################################################################

    def recapeoCompleto(self):

        self.capasRecapeadas = []
        
        self.recapeo(self.capaManzana, self.ACA.obtenerIdCapa('manzana'))
        self.recapeo(self.capaPrediosGeom, self.ACA.obtenerIdCapa('predios.geom'))
        self.recapeo(self.capaPrediosNum, self.ACA.obtenerIdCapa('predios.num'))
        self.recapeo(self.capaConstrucciones, self.ACA.obtenerIdCapa('construcciones'))
        self.recapeo(self.capaHorizontalesGeom, self.ACA.obtenerIdCapa('horizontales.geom'))
        self.recapeo(self.capaHorizontalesNum, self.ACA.obtenerIdCapa('horizontales.num'))
        self.recapeo(self.capaVerticales, self.ACA.obtenerIdCapa('verticales'))
        self.recapeo(self.capaCvesVert, self.ACA.obtenerIdCapa('cves_verticales'))

        self.recapeo(self.capaEstado, self.ACA.obtenerIdCapa('Estado'))
        self.recapeo(self.capaRegion, self.ACA.obtenerIdCapa('Region Catastral'))
        self.recapeo(self.capaMunicipios, self.ACA.obtenerIdCapa('Municipios'))
        self.recapeo(self.capaSecciones, self.ACA.obtenerIdCapa('Secciones'))
        self.recapeo(self.capaLocalidades, self.ACA.obtenerIdCapa('Localidades'))
        self.recapeo(self.capaSectores, self.ACA.obtenerIdCapa('Sectores'))
        
        self.recapeo(self.capaCalles, self.ACA.obtenerIdCapa('Calles'))
        self.recapeo(self.capaColonias, self.ACA.obtenerIdCapa('Colonias'))
        self.recapeo(self.capaCP, self.ACA.obtenerIdCapa('Codigo Postal'))
        self.recapeo(self.capaZona1, self.ACA.obtenerIdCapa('Zona Uno'))
        self.recapeo(self.capaZona2, self.ACA.obtenerIdCapa('Zona Dos'))
        self.recapeo(self.capaArea, self.ACA.obtenerIdCapa('Area de Valor'))

############################################################################################

    def recapeo(self, capa, idCapa):
        try:
            capa = QgsProject.instance().mapLayer(idCapa)
            self.capasRecapeadas.append(capa)
        except:
            capa = None

###########################################################################################

    def alternarEliminar(self):

        if self.modoEliminar:
            
            self.modoEliminar = False
            self.dockwidget.labelStatus.setText("DESACTIVADO")
            self.dockwidget.labelStatus.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            estilo = """color: rgb(255, 0, 0);
"""
            self.dockwidget.labelStatus.setStyleSheet(estilo)


        else:

            iface.actionSelect().trigger()
            self.modoEliminar = True
            self.dockwidget.labelStatus.setText("ACTIVADO")
            self.dockwidget.labelStatus.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            estilo = """color: rgb(1, 239, 1);
"""
            self.dockwidget.labelStatus.setStyleSheet(estilo)


####################################################################################################
