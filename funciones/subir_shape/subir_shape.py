# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SubirShape
                                 A QGIS plugin
 Modulo para subir shp a postgres
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-09-09
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Oliver
        email                : foo@bar.com
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
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.utils import iface
from qgis.core import *

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .subir_shape_dialog import SubirShapeDialog
import os.path
import json


class SubirShape:
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
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SubirShape_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.dlg = SubirShapeDialog()
        self.dlg.cargarButton.clicked.connect(self.cargar)

        # Declare instance attributes
        #self.actions = []
        #self.menu = self.tr(u'&Subir Shape')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

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
        return QCoreApplication.translate('SubirShape', message)


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

        icon_path = ':/plugins/subir_shape/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Subir shape'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Subir Shape'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        print("GREEC")

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def cargar(self):
        xMan = QSettings().value('xManzana')
        print(xMan)
        xPredG = QSettings().value('xPredGeom')
        print(xPredG)


        path = "/home/oliver/CAPAS A SUBIR/Nuevo Archivo WinRAR ZIP_1/Manzanas.shp"
        vlayer = QgsVectorLayer(path, "manzana", "ogr")
        if not vlayer.isValid():
            print("Layer failed to load!")
        else:
            QgsProject.instance().addMapLayer(vlayer)
        self.listaAGuardar = []
        self.agregarALista("manzana", vlayer)

        jsonParaGuardarAtributos = json.dumps(self.listaAGuardar)

        url = 'http://localhost:8080/featureswkn/api/manzana/'
        payload = jsonParaGuardarAtributos
        headers = {'Content-Type': 'application/json', 'Authorization': self.obtenerToken()}
        try:
            response = requests.post(url, headers=headers, data=payload)

        except requests.exceptions.RequestException:
            self.UTI.mostrarAlerta("No se ha podido conectar al servidor v1", QMessageBox.Critical,
                                   "Guardar Cambios v1")  # Error en la peticion de consulta

        print(response.json())
        print(response.status_code)


    def agregarALista(self, idCapa, capa):

        for feat in capa.getFeatures():
            campos = {}
            campos['wkt'] = feat.geometry().asWkt()
            campos['srid'] = QSettings().value('srid')
            campos['tabla'] = self.UTI.tablas[capa.name()]
            atributos = {}
            nombresAtrbutos = capa.fields()

            nombres = [campo.name() for campo in nombresAtrbutos]

            for x, campo in enumerate(nombresAtrbutos):
                atributo = feat.attributes()[x]
                if str(atributo) == "NULL":
                    atributo = None
                atributos[str(campo)] = atributo

                if idCapa == 'predios.geom':
                    punto = self.exteriorPredio(feat.geometry())
                    if punto != None:
                        atributos['numExt'] = punto['numExt']
                        atributos['geom_num'] = punto.geometry().asWkt()

                elif idCapa == 'horizontales.geom':
                    punto = self.exteriorCondom(feat.geometry())
                    if punto != None:
                        atributos['num_ofi'] = punto['num_ofi']
                        atributos['geom_num'] = punto.geometry().asWkt()

                campos['nuevo'] = True
                campos['eliminado'] = False

            campos['attr'] = atributos
            self.listaAGuardar.append(campos)


    def cargar_old(self):

        xMan = QSettings().value('xManzana')
        print(xMan)
        xPredG = QSettings().value('xPredGeom')
        print(xPredG)


        ALTA_LAYER = 0

        path = "/home/oliver/Downloads/fwdpoligono(1)/limitemuni_poo.shp"
        vlayer = QgsVectorLayer(path, "limitemuni", "ogr")
        if not vlayer.isValid():
            print("Layer failed to load!")
        else:
            QgsProject.instance().addMapLayer(vlayer)

        capas_cargadas = QgsProject.instance().mapLayers()

        capas = capas_cargadas.items()

        for k, v in capas:

            print("Lyr_source: ", v.source())
            if ALTA_LAYER == 0:

                fields = QgsFields()
                fields.append(QgsField("layer", QVariant.String))
                # fields.append(QgsField("myreal", QVariant.Double))

                exptr = QgsVectorLayerExporter(
                    u'dbname=\'spatial-mete-oliver\' host=177.225.106.243 port=5432 user=\'sigemun\' key=\'id\' table="public"."e_municipio" (geom) sql=',
                    'postgres', fields, QgsWkbTypes.MultiPolygon
                    , QgsCoordinateReferenceSystem(3857)
                    )

                l_features = v.getFeatures()
                for feature in l_features:
                    print(feature)
                    # exptr.addFeature(feature)


            elif ALTA_LAYER == 1:
                con_string = """dbname='spatial-mete-oliver' host='177.225.106.243' port='5432' user='sigemun' password='sigemun' key=postgres type=MULTIPOLYGON table="public"."e_municipio" (geom)"""
                err = QgsVectorLayerExporter.exportLayer(v, con_string, 'postgres',
                                                         QgsCoordinateReferenceSystem(3857), False)

                print(err)
            elif ALTA_LAYER == 2:
                for feature in v.getFeatures():
                    print("Feature ID: ", feature.id())
                    print("Geom:", feature.geometry())
                    attrs = feature.attributes()
                    print(attrs)

                    # TODO: Esto deeria ser dinamico
                    clave = feature['EntityHand']

                    f = QgsFeature()
                    f.setGeometry(feature.geometry())
                    f.setAttributes([100, "", clave, ""])
                    data_provider = QgsProviderRegistry.instance().createProvider("postgres",
                                                                                  u'dbname=\'spatial-mete-oliver\' host=177.225.106.243 port=5432 user=\'sigemun\' password=\'sigemun\' key=\'id\' table="public"."e_municipio" (geom) sql=')
                    print("Data Provider: ", type(data_provider))
                    print(data_provider.errors())
                    data_provider.addFeatures([f])


    def obtenerToken(self):
        url= 'http://localhost:8080/auth/login'
        payload = {"username" : "user", "password" : "user"}
        payload = json.dumps(payload)
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, headers = headers, data = payload)
        if response.status_code == 200:
            #print('habemus token')
            data = response.content
        else:
            print(response)
            self.UTI.mostrarAlerta('No se ha conseguido token del plugin de integracion', QMessageBox().Critical, 'Autenticacion')
            return

        return 'bearer ' + json.loads(data)['access_token']