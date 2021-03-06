# -*- coding: utf-8 -*-
"""
/***************************************************************************
 busquedadireccion
                                 A QGIS plugin
 busqueda por direccion
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-11-13
        git sha              : $Format:%H$
        copyright            : (C) 2020 by 1
        email                : 1
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QObject
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QTableWidgetItem, QAbstractItemView

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
import json, requests
from osgeo import ogr, osr
from qgis.core import *
from .busqueda_direccion_dialog import busquedadireccionDialog
import os.path
from ..datos_inmueble import datos_inmueble



class busquedadireccion:
    """QGIS Plugin Implementation."""

    def __init__(self, iface, CFG, UTI):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'busquedadireccion_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&busquedadireccion')
        self.CFG = CFG
        self.UTI = UTI
        self.pluginIsActive = False
        self.dockwidget = busquedadireccionDialog(parent=iface.mainWindow())
        self.vialidad_id = None
        self.idPredios = []

        #llenamos los combos
        self.obtenerMunicipios()
        self.obtenerColonias()

        #comportamiento tablas
        self.dockwidget.twNumerosExteriores.hideColumn(4)
        self.dockwidget.twVias.hideColumn(1)

        self.dockwidget.twNumerosExteriores.setSelectionBehavior(QAbstractItemView.SelectRows)


        #eventos
        self.dockwidget.btBusqueda.clicked.connect(self.getVias)
        self.dockwidget.twNumerosExteriores.itemSelectionChanged.connect(self.setIdPredio)
        self.dockwidget.btLocalizar.clicked.connect(self.pintarPredios)
        self.dockwidget.btCerrar.clicked.connect(self.closeIt)
        self.dockwidget.btDetalle.clicked.connect(self.abrirDetallePredio)



        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    def abrirDetallePredio(self):
        #Para abrir el detalle del predio
        urlDetallePredio = self.CFG.urlDetallePredio
        headers = {'Content-Type': 'application/json', 'Authorization': self.UTI.obtenerToken()}
        try:
            
            response = requests.get(urlDetallePredio + str(self.datosPredio['id']), headers = headers)
            self.dataPrueba = response.json()
            self.DTP = datos_inmueble.datosinmueble(self.iface, self.dataPrueba)
            self.DTP.run()

        except Exception:
            self.UTI.mostrarAlerta("No se ha carcado un predio", QMessageBox.Critical, "Detalle del predio")#Error en la peticion de consulta

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
        return QCoreApplication.translate('busquedadireccion', message)


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
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/busqueda_direccion/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&busquedadireccion'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        self.dockwidget.show()

        if not self.pluginIsActive:
            self.pluginIsActive = True
            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = busquedaCatastralDialog()

            # connect to provide cleanup on closing of dockwidget

            # show the dockwidget
            # TODO: fix to allow choice of dock location

            self.dockwidget.show()

        result = self.dockwidget.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def obtenerMunicipios(self):

        self.dockwidget.cbDelegacion.clear()

        try:
            headers = {'Content-Type': 'application/json', 'Authorization' : self.UTI.obtenerToken()}
            respuesta = requests.get(self.CFG.urlMunicipios, headers = headers)
        except requests.exceptions.RequestException:
            self.UTI.mostrarAlerta("Error de servidor loc2", QMessageBox().Critical, "Cargar Municipios")
            print('ERROR: MUN0000')

        lenJson = len(list(respuesta.json()))

        if lenJson > 0:
            for localidad in respuesta.json():
                self.dockwidget.cbDelegacion.addItem(str.upper(localidad['other']), str(localidad['value']))
        else:
            self.UTI.mostrarAlerta("No existen Municipios registrados", QMessageBox().Information, "Cargar Municipios")


    def obtenerColonias(self):
        self.dockwidget.cbCoonia.clear()

        try:
            headers = {'Content-Type': 'application/json', 'Authorization': self.UTI.obtenerToken()}
            respuesta = requests.get(self.CFG.urlColonias, headers=headers)
        except requests.exceptions.RequestException:
            self.UTI.mostrarAlerta("Error de servidor loc2", QMessageBox().Critical, "Cargar Colonias")
            print('ERROR: MUN0000')

        lenJson = len(list(respuesta.json()))

        if lenJson > 0:
            for colonia in respuesta.json():
                self.dockwidget.cbCoonia.addItem(str.upper(colonia['descripcion']))
        else:
            self.UTI.mostrarAlerta("No existen Colonias registrados", QMessageBox().Information, "Cargar Colonias")

    def getVias(self):

        colonia = None
        delegacion = None

        if self.dockwidget.cbDelegacion.count() > 0:
            index = self.dockwidget.cbDelegacion.currentIndex()
            delegacion = self.dockwidget.cbDelegacion.itemText(index)
        if self.dockwidget.cbCoonia.count() > 0:
            index = self.dockwidget.cbCoonia.currentIndex()
            colonia = self.dockwidget.cbCoonia.itemText(index)
        elif self.dockwidget.leNombreColonia.text() and len(self.dockwidget.leNombreColonia.text().strip()) > 0:
            colonia = self.dockwidget.leNombreColonia.text()
        via = self.dockwidget.leNombreVia.text()

        payload = json.dumps({'vialidad': via,
                    'colonia' : colonia,
                    'delegacion': delegacion})

        try:
            headers = {'Content-Type': 'application/json', 'Authorization': self.UTI.obtenerToken()}
            respuesta = requests.post(self.CFG.urlBusquedaDeVias, headers=headers, data = payload)
        except requests.exceptions.RequestException:
            self.UTI.mostrarAlerta("Error de servidor loc2", QMessageBox().Critical, "Cargar Vias")
            print('ERROR: VIA0000')
        if respuesta and respuesta.status_code == 200:
            data = respuesta.json()
            if len(data) > 0:
                self.vialidad_id = data[0]['id']

                self.vaciarTabla(self.dockwidget.twListaVias)
                self.dockwidget.twListaVias.insertRow(0)
                item = QTableWidgetItem(data[0]['vialidad'])
                self.dockwidget.twListaVias.setItem(0, 0, item)

                if colonia or delegacion:
                    self.vaciarTabla(self.dockwidget.twColonias)
                    self.dockwidget.twColonias.insertRow(0)
                    if colonia:
                        item = QTableWidgetItem(colonia)
                        self.dockwidget.twColonias.setItem(0, 0, item)
                    if delegacion:
                        item = QTableWidgetItem(delegacion)
                        self.dockwidget.twColonias.setItem(0, 1, item)

                self.getPredios()
            else:
                self.UTI.mostrarAlerta("Vialidades no encontradas", QMessageBox().Critical, "Cargar Vias")
                print('ERROR: VIA0001')



    def getPredios(self):


        try:
            headers = {'Content-Type': 'application/json', 'Authorization': self.UTI.obtenerToken()}
            respuesta = requests.get(self.CFG.urlPredioByVialidad + str(self.vialidad_id), headers=headers)
        except requests.exceptions.RequestException:
            self.UTI.mostrarAlerta("Error de servidor loc2", QMessageBox().Critical, "Consultar predios by vialidad")
            return

        if respuesta.status_code == 200:
            predios = respuesta.json()
        else:
            self.UTI.mostrarAlerta(f"Error de peticion. Body: {respuesta.json()}",  QMessageBox().Critical, "Consultar predios by vialidad")
            return

        print(predios)
        if predios:
            if len(predios['intersectan']) > 0:
                #twVias
                self.vaciarTabla(self.dockwidget.twVias)

                for i, dict_ in enumerate(predios['intersectan']):
                    self.dockwidget.twVias.insertRow(i)
                    item = QTableWidgetItem(dict_['vialidad'])
                    self.dockwidget.twVias.setItem(i, 0, item)

                    item = QTableWidgetItem(dict_['id'])
                    self.dockwidget.twVias.setItem(i, 1, item)

            if len(predios['predios']) > 0:
                self.vaciarTabla(self.dockwidget.twNumerosExteriores)

                for i, dict_ in enumerate(predios['predios']):
                    self.dockwidget.twNumerosExteriores.insertRow(i)
                    item = QTableWidgetItem(dict_['numero'])
                    self.dockwidget.twNumerosExteriores.setItem(i, 0, item)

                    item = QTableWidgetItem(dict_['cveManzana'])
                    self.dockwidget.twNumerosExteriores.setItem(i, 2, item)

                    item = QTableWidgetItem(dict_['lote'])
                    self.dockwidget.twNumerosExteriores.setItem(i, 3, item)

                    item = QTableWidgetItem(str(dict_['id']))
                    self.dockwidget.twNumerosExteriores.setItem(i, 4, item)

    def setIdPredio(self):

        idPredios = []

        rows = [idx.row() for idx in self.dockwidget.twNumerosExteriores.selectionModel().selectedRows()]
        for row in rows:
            idPredios.append(self.dockwidget.twNumerosExteriores.item(row, 4).text())
        self.idPredios = idPredios


    def vaciarTabla(self, tabla_ref):

        tabla_ref.clearContents()
        tabla_ref.setRowCount(0)

        for row in range(0,tabla_ref.rowCount()):
            tabla_ref.removeRow(row)


    def pintarPredios(self):

        url = self.CFG.url_BC_getPredios_id

        resArray = []

        for id in self.idPredios:
            try:
                headers = {'Content-Type': 'application/json', 'Authorization': self.UTI.obtenerToken()}
                respuesta = requests.get(url + id, headers=headers)
            except requests.exceptions.RequestException:
                self.UTI.mostrarAlerta("Error de servidor loc2", QMessageBox().Critical, "Busqueda de predio por id")
                print('ERROR: BD0000')

            if respuesta.status_code == 200:
                data = respuesta.content

            else:
                self.UTI.mostrarAlerta('Error en peticion:\n' + response.text, QMessageBox().Critical, "Busqueda de predio por cve")
                print('ERROR: BCP0001')

            res = json.loads(data.decode('utf-8'))
            if not bool(res):
                self.UTI.mostrarAlerta("Error de servidor pintcap", QMessageBox().Critical, "Cargar capa de consulta")
                print('ERROR: BCP0002')

            resArray.append(res)

        #si se consulto mas de 1 predio, fusionaremos los features en los resultados de cada consulta
        for j in range(0,len(resArray)):
            res = resArray[j]
            if len(resArray) > 1:
                for i in range(1, len(resArray)):
                    res['features'].append(resArray[i]['features'])



            xPredG = QSettings().value('xPredGeom')
            self.xPredGeom = QgsProject.instance().mapLayer(xPredG)

            if self.xPredGeom is None:
                self.UTI.mostrarAlerta('No existe la capa ' + str(xPredG), QMessageBox().Critical, 'Cargar capas')
                return

            srid = QSettings().value("srid")

            inSpatialRef = osr.SpatialReference()
            inSpatialRef.ImportFromEPSG(int(srid))
            outSpatialRef = osr.SpatialReference()
            outSpatialRef.ImportFromEPSG(int(srid))
            coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)


            varKeys = res['features'][0]['properties']
            self.datosPredio = varKeys
            keys = list(varKeys.keys())
            properties = []
            geoms = []


            for feature in res['features']:

                geom = feature['geometry']

                property = feature['properties']
                geom = json.dumps(geom)
                geometry = ogr.CreateGeometryFromJson(geom)
                geometry.Transform(coordTrans)
                geoms.append(geometry.ExportToWkt())
                l = []
                for i in range(0, len(keys)):
                    l.append(property[keys[i]])
                properties.append(l)

            prov = self.xPredGeom.dataProvider()
            feats = [QgsFeature() for i in range(len(geoms))]

            parsed_geoms = []

            for i, feat in enumerate(feats):
                feat.setAttributes(properties[i])
                parse_geom = QgsGeometry.fromWkt(geoms[i])
                feat.setGeometry(parse_geom)
                parsed_geoms.append(parse_geom)

            prov.addFeatures(feats)

            geometria = parsed_geoms[0]

            for i in range(1, len(parsed_geoms)):
                geometria = geometria.combine(geometria[i])

            bbox = geometria.boundingBox()
            self.iface.mapCanvas().setExtent(bbox)
            self.iface.mapCanvas().refresh()



            #if nombreCapa == 'predios.geom':
             #   self.cargarPrediosEnComboDividir(feats)

            self.xPredGeom.triggerRepaint()

    def closeIt(self):
        self.dockwidget.close()




