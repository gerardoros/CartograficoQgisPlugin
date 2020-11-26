from PyQt5.QtCore import QThread
import qgis
from qgis.utils import iface
from qgis.core import *
from PyQt5.QtCore import QFileInfo, QSettings, QCoreApplication, QTimer
from PyQt5.QtWidgets import QAction, QMessageBox, QApplication
from PyQt5.QtGui import *
import json, requests, os, time, threading, jwt, datetime
from osgeo import ogr, osr
from pathlib import Path
from datetime import datetime as dt

class Startup():

    def __init__(self):

        ''' Controlar las acciones de algunos menus de Qgis
        menuVector = iface.vectorMenu().actions()
        menuOpciones = iface.settingsMenu().actions()
        menuOpciones2 = iface.settingsMenu()
        menuPlug = iface.pluginMenu().actions()
        '''
        
        helpBar = iface.helpToolBar()

        QSettings().setValue('listaEliminada', [])
        QSettings().setValue('listaEliminadaRef', [])
        QSettings().setValue('capaRefEdicion', 'None')

        # capas principales
        QSettings().setValue('xManzana', "None")
        QSettings().setValue('xPredGeom', "None")
        QSettings().setValue('xPredNum', "None")
        QSettings().setValue('xConst', "None")
        QSettings().setValue('xHoriGeom', "None")
        QSettings().setValue('xHoriNum', "None")
        QSettings().setValue('xVert', "None")
        QSettings().setValue('xCvesVert', "None")

        # referencia
        QSettings().setValue('xAreaValor', "None")
        QSettings().setValue('xZonaUno', "None")
        QSettings().setValue('xZonaDos', "None")
        QSettings().setValue('xCP', "None")
        QSettings().setValue('xColonia', "None")
        QSettings().setValue('xCalle', "None")
        QSettings().setValue('xSector', "None")
        QSettings().setValue('xLocal', "None")
        QSettings().setValue('xSeccion', "None")
        QSettings().setValue('xMunicipio', "None")
        QSettings().setValue('xRegion', "None")
        QSettings().setValue('xEstado', "None")
        QSettings().setValue('xManzanasRef', "None")
        QSettings().setValue('xPredRef', "None")
        QSettings().setValue('xConstRef', "None")

        self.var = QSettings()
        # set Rot13
        self.rot13 = str.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

        self.tablas = {
        'manzana': 'e_manzana', 
        'predios.geom': 'e_predio', 
        'construcciones': 'e_construccion',  
        'horizontales.geom':'e_condominio_horizontal', 
        'verticales':'e_condominio_vertical', 
        'cves_verticales':'e_condominio_vert_clave'}

        self.modoDesarrollo = False

        clickSalir = QAction(QIcon("C:/AplicacionQGIS/reload.png"), QCoreApplication.translate("Groundwater Modeling", "Cerrar Sesion"), iface.mainWindow())
        clickCerrar = QAction(QIcon("C:/AplicacionQGIS/cerrar.png"), QCoreApplication.translate("Groundwater Modeling", "Cerrar Sesion"), iface.mainWindow())
        clickBorrarTodo = QAction(QIcon("C:/AplicacionQGIS/notify_off.png"), QCoreApplication.translate("Groundwater Modeling", "btnPrueba"), iface.mainWindow())
        clickGuardar = QAction(QIcon("C:/AplicacionQGIS/guardar.png"), QCoreApplication.translate("Groundwater Modeling", "Guardar Cambios"), iface.mainWindow())

        clickSalir.triggered.connect(self.cerrarSinPreguntar)
        clickCerrar.triggered.connect(self.preguntarCerrarSesion)
        clickBorrarTodo.triggered.connect(self.borrarTodo)

        helpBar.addAction(clickSalir)
        #helpBar.addAction(clickBorrarTodo)
        #helpBar.addAction(clickGuardar)
        #helpBar.addAction(clickCerrar)
        self.var.setValue("reglasTopologicas", [])
        self.var.setValue("posibleGuardar", "False")
        self.var.setValue("posibleGuardarRef", "False")

        QSettings().setValue('integrando', 'False') 
        self.counter = 0
        '''
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
        '''
        #ThreadingExample()
        
        # inicializacion de diccionario de tablas
        self.diccionarioTabla = {}
        self.diccionarioTabla['manzana'] = 'sig:e_manzana'
        self.diccionarioTabla['predios.geom'] = 'sig:e_predio'
        self.diccionarioTabla['construcciones'] = 'sig:e_construccion'
        self.diccionarioTabla['horizontales.geom'] = 'sig:e_condominio_horizontal'
        self.diccionarioTabla['verticales'] = 'sig:e_condominio_vertical'
        self.diccionarioTabla['cves_verticales'] = 'sig:e_condominio_vert_clave'
        
        # inicializacion de diccionario de tipos de datos
        self.diccionarioTipo = {}
        self.diccionarioTipo["STRING"] = 'string'
        self.diccionarioTipo["INTEGER"] = 'integer'
        self.diccionarioTipo["DATETIME"] = 'date'
        self.diccionarioTipo["NUMERIC"] = 'real'
        self.diccionarioTipo["SMALLINT"] = 'integer'
        self.diccionarioTipo["BOOLEAN"] = 'string'
        
        # inicializacion de diccionario de tipos de datos
        self.diccionarioGeom = {}
        self.diccionarioGeom["manzana"] = 'Polygon'
        self.diccionarioGeom["predios.geom"] = 'Polygon'
        self.diccionarioGeom["predios.num"] = 'Point'
        self.diccionarioGeom["construcciones"] = 'Polygon'
        self.diccionarioGeom["horizontales.geom"] = 'Polygon'
        self.diccionarioGeom["horizontales.num"] = 'Point'
        self.diccionarioGeom["verticales"] = 'Polygon'
        self.diccionarioGeom["cves_verticales"] = 'Point'
        #self.diccionarioGeom["areas_inscritas"] = 'Polygon'


        

    def borrarTodo(self):
        #grupoLayers =  QgsProject.instance().layerTreeRoot().findGroup('consulta')
        #layers = grupoLayers.findLayers()
        #for layer in layers:
        #    layer.layer().startEditing()
        #    for f in layer.layer().getFeatures():
        #        layer.layer().dataProvider().deleteFeatures([f.id()])
        #    layer.layer().triggerRepaint()
        #    layer.layer().commitChanges()
        #print(self.capita.id())
        #capa = QgsProject.instance().mapLayer(self.capita.id())
        #print(capa.name())
        pass

    def recurring_timer(self):
        self.counter +=1

        if self.counter%10 == 0:
            self.borrarTodo()
        
        print("Counter: %d" % self.counter)
        

    def cerrarSinPreguntar(self):
        os.kill(os.getpid(), 9)


    def mostrarConsola(self):

        iface.actionShowPythonDialog().trigger()
        #print ('CONSOLA INICIADA')
        #root = QgsProject.instance().layerTreeRoot()
        #root.addGroup('edicion')
        #print ('CONSOLA INICIADA2')


    '''
    dependiendo de un archivo de inicializacion se define si QGIS des abre para interactuar con el 
    sistema cartografico o NO

    en la primera linea tendra un booleano - define si se uso una aplicacion externa para iniciar session
    en la segunda linea tendra el token    - cuando se inicie session se genera un token para realizar peticiones a WS
    en la tercera linea tendra un booleano - define si se encuentra logueado el usuario
    '''
    def checarLogin(self):
        
        file = Path("C:/AplicacionQGIS/start.det")
        # verifica si el archivo de inicializacion existe
        if file.is_file():
            # se abre el archivo de inicializacion
            archivo = open('C:/AplicacionQGIS/start.det', 'r')

            # el archivo contiene cinco lineas
            self.var.setValue("usoLogin", archivo.readline().replace('\n', ''))
        else:
            self.var.setValue("usoLogin", "False")

        if(self.var.value("usoLogin") == "True"):
            self.var.setValue("token", archivo.readline().replace('\n', ''))
            self.var.setValue("logeado", archivo.readline().replace('\n', ''))
            self.var.setValue("usuario", archivo.readline().replace('\n', ''))
            self.var.setValue("clave", archivo.readline().replace('\n', ''))
            
        else:
            self.var.setValue("logeado", "False")

        log = self.var.value("logeado")
        sal = self.var.value("salida")

        if file.is_file():
            archivo.close()

        # borra el contenido del archivo
        if(self.var.value("usoLogin") == "True"):
            archivo = open('C:/AplicacionQGIS/start.det', 'r+')
            archivo.truncate()
            archivo.close()
        

        if log == "True" or self.modoDesarrollo:  
            #print('etrnooooo rasaaaa')
            self.cargarCapas(log)
            #helpBar.addAction(clickSalir)
            #helpBar.addAction(clickGuardar)
            #helpBar.addAction(clickCerrar)
            #self.var.setValue("reglasTopologicas", [])
            #self.var.setValue("posibleGuardar", "False")
            #self.var.setValue("posibleGuardarRef", "False")
            #agregarBotones()


    def preguntarCerrarSesion(self):
        
        mensaje = "Se perderan las capas de los grupos de consulta y referencia, ademas de las reglas de topologia\nDeseas continuar?"
        respuesta = QMessageBox.question(iface.mainWindow(), "Nota de cierre de sesion", mensaje, QMessageBox.Yes, QMessageBox.No)

        if respuesta == QMessageBox.Yes:
            cerrarSesion()


    def preguntarGuardar(self):
        
        if QSettings().value("token") != "None" or self.modoDesarrollo:

            if QSettings().value("posibleGuardar") == "True" or self.modoDesarrollo:
            
                mensaje = "Deseas guardar los cambios?"
                respuesta = QMessageBox.question(iface.mainWindow(), "Guardar Cambios", mensaje, QMessageBox.Yes, QMessageBox.No)

                if respuesta == QMessageBox.Yes:
                    self.guardarCambios()
            
            else:
                createAlert('No es posible guardar los cambios debido a \n que no se ha validado la topologia', QMessageBox.Critical, 'Error al guardar cambios')

        else:
            createAlert('Inicia Sesion', QMessageBox.Critical, 'Guardar Cambios')
            ocultarIconos()

######################################################################################################################

    def cerrarSesion(self):

        if QSettings().value("token") != "None":
                #Creamos instancia del proyecto
            proyecto = QgsProject.instance()

            #Creamos la raiz
            root = QgsProject.instance().layerTreeRoot()

            #Borramos el grupo consulta y sus capas
            group = root.findGroup('consulta')
            if not group is None:
                for child in group.children():
                    dump = child.dump()
                    id = dump.split("=")[-1].strip()
                    QgsProject.instance().removeMapLayer(id)
                root.removeChildNode(group)

            #Borramos el grupo referencia y sus capas
            group = root.findGroup('referencia')
            if not group is None:
                for child in group.children():
                    dump = child.dump()
                    id = dump.split("=")[-1].strip()
                    QgsProject.instance().removeMapLayer(id)
                root.removeChildNode(group)

            #Devolver token
            QSettings().setValue("token", "None")
            QSettings().setValue("logeado", "False")
            #QSettings().setValue("salida", "True")
            ocultarIconos()

        else:
            createAlert('La sesion ya ha sido cerrada', QMessageBox.Critical, 'Cerrar Sesion')
            ocultarIconos()

######################################################################################################################
        
    def ocultarIconos(self):
        contadorHelp = 0
        for item in helpBar.actions():
            if(contadorHelp > 0):
                item.setVisible(False)
            contadorHelp = contadorHelp + 1

########################################################################################################################

    #Metodo que crea un elemento QMessageBox
    def createAlert(self, mensaje, icono, titulo):
        #Create QMessageBox
        msg = QMessageBox()
        #Add message
        msg.setText(mensaje)
        #Add icon of critical error
        msg.setIcon(icono)
        #Add tittle
        msg.setWindowTitle(titulo)
        #Show of message dialog
        msg.show()
        # Run the dialog event loop
        result = msg.exec_()

#######################################################################################################

    def cargarCapas(self, log):
        
        if not log:
            return 
	
        # Solicitar SRID para el municipio
        headers = {'Content-Type': 'application/json', 'Authorization' : self.obtenerToken()}

        #urlSrid = 'https://thesmartflat.cianet.mx/cartografico/api/busquedasimplewkn/api/cat/municipio/'

        urlSrid = 'http://192.168.0.25:8080/busquedasimplewkn/api/cat/municipio/'

        
        respuesta = requests.get(urlSrid, headers = headers)
        cveMpio = 0
        mpio = ''

        if respuesta.status_code == 200:
            salida = respuesta.json()
            if len(salida) > 0:
                srid = str(salida[0]['srid'])
                cveMpio = str(salida[0]['clave'])
                mpio = str(salida[0]['descripcion'])
            else:
                print('NO SE PUDO CARGAR SRDI, "salida" sin valor')
                srid = '32614'

            QSettings().setValue('srid', srid)
        else:
            print('NO SE PUDO CARGAR SRDI', respuesta)
            QSettings().setValue('srid', '32614')
        
        QSettings().setValue('cveMpio', cveMpio)
        QSettings().setValue('mpio', mpio)
        '''
        # Obtenemos la raiz para agregar grupos
        root = QgsProject.instance().layerTreeRoot() 
        root.addGroup('consulta')
        root.addGroup('referencia') 
        '''
        
        #self.consultarLlenadoDeCapa('areas_inscritas')
        self.consultarLlenadoDeCapa('cves_verticales')
        self.consultarLlenadoDeCapa('verticales')
        self.consultarLlenadoDeCapa('horizontales.num')
        self.consultarLlenadoDeCapa('horizontales.geom')
        self.consultarLlenadoDeCapa('construcciones')
        self.consultarLlenadoDeCapa('predios.num')
        self.consultarLlenadoDeCapa('predios.geom')
        self.consultarLlenadoDeCapa('manzana')
        
        '''
        wkt = "POLYGON ((79.87749999947846 6.997500000409782, 79.88249999947845 6.997500000409782, 79.88249999947845 7.002500000409782, 79.87749999947846 7.002500000409782, 79.87749999947846 6.997500000409782))"

        temp = QgsVectorLayer("Polygon?crs=epsg:" + srid, "result", "memory")
        #QgsProject.instance().addMapLayer(temp, False)
        '''
        '''
        temp.startEditing()
        geom = QgsGeometry()
        geom = QgsGeometry.fromWkt(wkt)
        feat = QgsFeature()
        feat.setGeometry(geom)
        temp.dataProvider().addFeatures([feat])
        temp.commitChanges()
        ' ''


        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup('consulta')
        capaArbol = QgsLayerTreeLayer(temp)

        group.insertChildNode(0, capaArbol)

        '''

#########################################################################################################################
    
    def etiquetarCapa(self, nombreCapa):

        
        capa = QgsProject.instance().mapLayer(self.obtenerIdCapa(nombreCapa))
        
        if capa == None:
            capa = QgsProject.instance().mapLayersByName(nombreCapa)[0]
        
        etiquetaField = ""
        colorCapa = ""
        esExpresion = False
        if nombreCapa == "manzana":
            etiquetaField = "clave"
            colorCapa = QColor(255,0,0)
        elif nombreCapa == "predios.geom":
            etiquetaField = "clave"
            colorCapa = QColor(0,255,0)
        elif nombreCapa == "predios.num":
            etiquetaField = "numExt"
            colorCapa = QColor(0,255,0)
        elif nombreCapa == "construcciones":
            etiquetaField = " if( cve_const_esp is null, concat(nom_volumen, '\n', num_niveles), concat(nom_volumen, '\n', cve_const_esp))"
            esExpresion = True
            colorCapa = QColor(0,0,255)
        elif nombreCapa == "horizontales.geom":
            etiquetaField = "clave"
            colorCapa = QColor(198,140,33)
        elif nombreCapa == "horizontales.num":
            etiquetaField = "num_ofi"
            colorCapa = QColor(198,140,33)
        elif nombreCapa == "verticales":
            etiquetaField = "clave"
            colorCapa = QColor(255,153,0)
        elif nombreCapa == "cves_verticales":
            etiquetaField = "clave"
            colorCapa = QColor(255,153,0)
        else:
            etiquetaField = "mensaje"
            colorCapa = QColor(255,153,0)

        '''
        elif nombreCapa == "areas_inscritas":
            etiquetaField = "clave"
            colorCapa = QColor(255,153,0)
        '''
        
        settings = QgsPalLayerSettings()
        settings.fieldName = etiquetaField
        settings.enabled = True
        settings.isExpression = esExpresion
        
        settings.centroidWhole = True

        textFormat = QgsTextFormat()
        textFormat.setColor(colorCapa)
        textFormat.setSize(8)
        textFormat.setNamedStyle('Bold')

        settings.setFormat(textFormat)

        #settings.placement= QgsPalLayerSettings.OverPoint
        labeling = QgsVectorLayerSimpleLabeling(settings)

        capa.setLabeling(labeling)
        capa.setLabelsEnabled(True)
        capa.triggerRepaint()

##############################################################################################################################

    def ineditarCapa(self, nombreCapa):
        #Predios ineditables

        capa = QgsProject.instance().mapLayer(self.obtenerIdCapa(nombreCapa))

        campos = capa.fields()   
        nombres = [field.name() for field in campos]

        for i in range (0, len(nombres)):
            config = capa.editFormConfig()
            config.setReadOnly(i, True)
            capa.setEditFormConfig(config)

#####################################################################################################################################

    def cargarWebService(self):

        #token = "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhZG1pbiIsInNjb3BlIjpbIm9wZW5pZCJdLCJleHAiOjE1MTk2ODcwMzgsImlhdCI6MTUxOTY4NjczOCwiYXV0aG9yaXRpZXMiOlsiUk9MRV9BRE1JTiIsIlJPTEVfVVNFUiJdLCJqdGkiOiJkMzI1ZWQ4Ni1iNmVlLTQ3ZDktYWI4YS1lYzE3YjgwMDNjNzEiLCJjbGllbnRfaWQiOiJ3ZWJfYXBwIn0.TMXvDbwtfMJLK_1UnnoTySt0TZ4o_4H1tp-A1CHBDlnU0aCQWnfcj3ja6jD5RAsNKmlc-5HD1gvRlFdKt5D9BBbLxykswD161N2690iurCV0NkjhmMia7yt8-X0EOI1vQoEyf7GdnzFo6Bi5fpmFE6YSS9LMZaxCy4NVhLRfqgNgq9ExKd4igedRSMmSVpQ5oV0u-5__7-sB07n3KCwGZjXeRJgVZQuKUiNI8pPljsY8X56vqYPlJlBNLzIjGjjxR_bkiYaXTdytd9LckbwSnm0914KHkIEhr66PS548V58nZfSAovLofaqV7-VCWViPo3SgvmuLDVxwdFem4b4ipQ"
        token = "bearer " + QSettings().value("token")

        cabecera = {'Content-type': 'application/json', 'Authorization' : token}

            #url del service
        url = 'http://201.165.150.64:8080/configuracion/api/adm-capas/getAllCapasConfiguration'

        respuesta = requests.get(url, headers = cabecera)

        if respuesta.status_code == 200:

            datos = respuesta.json()


            #Leemos los objetos capa del json
            for objeto in datos:

                stringDatos = "" #Los datos de la capa los guardamemos en un string

                #obtenemos el srid
                srid = objeto["catDependencia"]["municipio"]["srid"]

                #cargamos el srid en el string de los datos
                #stringDatos += objeto["layerType"]
                stringDatos += "Polygon"
                stringDatos += '?crs=epsg:'
                stringDatos += str(srid)

                #Obtenemos la dependencia de del objeto capa
                dependencia = objeto["catDependencia"]["nombre"]

                #Obtenemos los atributos de la capa y los pasamos al string
                for atributo in objeto["atributos"]:
                    stringDatos += '&field='
                    stringDatos += atributo["internalName"]
                    tipo = atributo["attrType"]
                    if tipo == 'STRING':
                        stringDatos += ':string(15)'
                    
                stringDatos += '&index=yes'    
                stringNombre = objeto["name"] #Obtenemos el nombre la capa

                #Creamos la capa con el string
                capa = QgsVectorLayer(stringDatos, stringNombre, "memory")

                capa.startEditing() #Iniciamos edicion de la capa

                root = QgsProject.instance().layerTreeRoot() #Obtenemos la raiz para agregar grupos

                QgsProject.instance().addMapLayer(capa, False) #Agregamos la capa en falso para que no se refleje hasta agregarla al grupo

                group = root.findGroup(dependencia) #Buscamos el grupo de la dependencia

                capaReinst = QgsLayerTreeLayer(capa) #La necesitamos para agregar al grupo

                renderer = capa.renderer() #Obtenemos el rendered
                colorRelleno = "#" + objeto["fillColor"] #Obtenemos el color de relleno de la capa
                colorBorde = "#" + objeto["strokeColor"] #Obtenemos el color del borde de la capa
                anchoBorde = str(objeto["strokeWidth"]) #Obtenemos el ancho del bode de la capa

                if capa.wkbType() == 3: #Si la capa es poligono aplicamos el estilo
                    symbol = QgsFillSymbol.createSimple({'color': colorRelleno, 'color_border': colorBorde, 'width_border': anchoBorde})
                    renderer.setSymbol(symbol)
                    capa.triggerRepaint()
                    capa.commitChanges() #Aceptamos los cambios

                if not group is None: #Si el grupo dependencia existe agregamos la capa
                    group.insertChildNode(0, capaReinst)
                else: #Si el grupo dependencia no existe lo creamos y luego agregamos la capa
                    root.insertGroup(0, dependencia)
                    group = root.findGroup(dependencia)
                    group.insertChildNode(0, capaReinst)

                #print QSettings().value("reglasTopologicas", [])
                reglas = QSettings().value("reglasTopologicas") #obtenemos las reglas ya almacenadas en qgis

                #print reglas
                reglasObjeto = objeto["topologias"]
                
                for regla in reglasObjeto:
                    descRegla = regla["reglaTopolia"]
                    capa1 = stringNombre
                    capa2 = regla["capa"]
                    tupla = (descRegla, capa1, capa2)
                    reglas.append(tupla)
                
                QSettings().setValue("reglasTopologicas", reglas)

##########################################################################################################################

    def obtenerToken(self):

        # validar la caducidad del token
        # se obtiene el token almacenado
        var = QSettings()
        token = var.value('token')

        # se decodifica el token (JWT)
        decode = jwt.decode(token, verify=False)
        
        # se obtiene la fecha de expiracion (timestamp)
        ttFromJWT = decode['exp']

        # se convierte a fecha legible para compararse con la fecha actual
        exp = dt.fromtimestamp(ttFromJWT).strftime('%Y-%m-%d %H:%M:%S')
        exp = dt.strptime(exp,'%Y-%m-%d %H:%M:%S')

        # se obtiene la fecha actual
        currentDate = datetime.datetime.now()

        # se compara para verificar que se haya caducado el token
        if currentDate > exp:
            #url= 'https://thesmartflat.cianet.mx/cartografico/api/auth/login'
            url= 'http://192.168.0.25:8080/auth/login'
            payload = {"username" : self.decodeRot13(var.value('usuario')), "password" : self.decodeRot13(var.value('clave'))}
            payload = json.dumps(payload)
            headers = {'Content-Type': 'application/json'}

            response = requests.post(url, headers = headers, data = payload)
            if response.status_code == 200:
                data = response.content
            else:
                self.createAlert('No se ha conseguido token de startup', QMessageBox().Critical, 'Autenticacion')
                return

            var.setValue('token', json.loads(data)['access_token'])
            return 'bearer ' + json.loads(data)['access_token']
        else:
            return 'bearer ' + token


    def decodeRot13(self, cadena):
        return str.translate(cadena, self.rot13)




        




#################################################################################################################

    def cargarJSON(self):


        stringJson = """ [
    {
    "name": "PRUEBA1",
    "layerType": "WMS",
    "strokeColor": "ABCDEF",
    "strokeWidth": 0.5,
    "fillColor": "FFBF00",
    "atributos": [
        {
        "internalName": "clv",
        "attrType": "STRING"
        }
    ],
    "catDependencia": {
        "nombre": "catastro",
        "municipio": {
        "srid": 32614
        },
        "topologias": [
        {
            "reglaTopolia": "interseccion",
            "capa": "PRUEBA1"
        },
        {
            "reglaTopolia": "inclusion",
            "capa": "PRUEBA2"
        }
        ]
    }
    },
    {
    "name": "PRUEBA2",
    "layerType": "WMS",
    "strokeColor": "A9F5A9",
    "strokeWidth": 0.3,
    "fillColor": "A9F5A9",
    "atributos": [
        {
        "internalName": "clv",
        "attrType": "STRING"
        }
    ],
    "catDependencia": {
        "nombre": "catastro",
        "municipio": {
        "srid": 32614
        },
        "topologias": [
        {
            "reglaTopolia": "interseccion",
            "capa": "PRUEBA2"
        }
        ]
    }
    }

    ] """

        datos = json.loads(stringJson)


        #Leemos los objetos capa del json
        for objeto in datos:

            stringDatos = "" #Los datos de la capa los guardamemos en un string

            #obtenemos el srid
            srid = objeto["catDependencia"]["municipio"]["srid"]

            #cargamos el srid en el string de los datos
            #stringDatos += objeto["layerType"]
            stringDatos += "Polygon"
            stringDatos += '?crs=epsg:'
            stringDatos += str(srid)

            #Obtenemos la dependencia de del objeto capa
            dependencia = objeto["catDependencia"]["nombre"]

            #Obtenemos los atributos de la capa y los pasamos al string
            for atributo in objeto["atributos"]:
                stringDatos += '&field='
                stringDatos += atributo["internalName"]
                tipo = atributo["attrType"]
                if tipo == 'STRING':
                    stringDatos += ':string(15)'
                
            stringDatos += '&index=yes'    
            stringNombre = objeto["name"] #Obtenemos el nombre la capa

            #Creamos la capa con el string
            capa = QgsVectorLayer(stringDatos, stringNombre, "memory")

            capa.startEditing() #Iniciamos edicion de la capa

            root = QgsProject.instance().layerTreeRoot() #Obtenemos la raiz para agregar grupos

            QgsProject.instance().addMapLayer(capa, False) #Agregamos la capa en falso para que no se refleje hasta agregarla al grupo

            group = root.findGroup(dependencia) #Buscamos el grupo de la dependencia

            capaReinst = QgsLayerTreeLayer(capa) #La necesitamos para agregar al grupo

            renderer = capa.renderer() #Obtenemos el rendered
            colorRelleno = "#" + objeto["fillColor"] #Obtenemos el color de relleno de la capa
            colorBorde = "#" + objeto["strokeColor"] #Obtenemos el color del borde de la capa
            anchoBorde = str(objeto["strokeWidth"]) #Obtenemos el ancho del bode de la capa

            if capa.wkbType() == 3: #Si la capa es poligono aplicamos el estilo
                symbol = QgsFillSymbol.createSimple({'color': colorRelleno, 'color_border': colorBorde, 'width_border': anchoBorde})
                renderer.setSymbol(symbol)
                capa.triggerRepaint()
                capa.commitChanges() #Aceptamos los cambios

            if not group is None: #Si el grupo dependencia existe agregamos la capa
                group.insertChildNode(0, capaReinst)
            else: #Si el grupo dependencia no existe lo creamos y luego agregamos la capa
                root.insertGroup(0, dependencia)
                group = root.findGroup(dependencia)
                group.insertChildNode(0, capaReinst)

            #print QSettings().value("reglasTopologicas", [])
            reglas = QSettings().value("reglasTopologicas") #obtenemos las reglas ya almacenadas en qgis

            #print reglas
            reglasObjeto = objeto["catDependencia"]["topologias"]
            
            for regla in reglasObjeto:
                descRegla = regla["reglaTopolia"]
                capa1 = stringNombre
                capa2 = regla["capa"]
                tupla = (descRegla, capa1, capa2)
                reglas.append(tupla)
            
            QSettings().setValue("reglasTopologicas", reglas)

##############################################################################################################

        
    def obtenerIdCapa(self, nombreCapa):

        if nombreCapa == "manzana":
            return QSettings().value('xManzana')
        elif nombreCapa == "predios.geom":
            return QSettings().value('xPredGeom')
        elif nombreCapa == "predios.num":
            return QSettings().value('xPredNum')
        elif nombreCapa == "construcciones":
            return QSettings().value('xConst')
        elif nombreCapa == "horizontales.geom":
            return QSettings().value('xHoriGeom')
        elif nombreCapa == "horizontales.num":
            return QSettings().value('xHoriNum')
        elif nombreCapa == "verticales":
            return QSettings().value('xVert')
        elif nombreCapa == "cves_verticales":
            return QSettings().value('xCvesVert')
        elif nombreCapa == "Area de Valor":
            return QSettings().value('xAreaValor')
        elif nombreCapa == "Zona Uno":
            return QSettings().value('xZonaUno')
        elif nombreCapa == "Zona Dos":
            return QSettings().value('xZonaDos')
        elif nombreCapa == "Codigo Postal":
            return QSettings().value('xCP')
        elif nombreCapa == "Colonias":
            return QSettings().value('xColonia')
        elif nombreCapa == "Calles":
            return QSettings().value('xCalle')
        elif nombreCapa == "Sectores":
            return QSettings().value('xSector')
        elif nombreCapa == "Localidades":
            return QSettings().value('xLocal')
        elif nombreCapa == "Secciones":
            return QSettings().value('xSeccion')
        elif nombreCapa == "Municipios":
            return QSettings().value('xMunicipio')
        elif nombreCapa == "Region Catastral":
            return QSettings().value('xRegion')
        elif nombreCapa == "Estado":
            return QSettings().value('xEstado')
        
        return 'None'

################################################################################################################################

    def consultarLlenadoDeCapa(self, capaParam):
        
        # obtener el tipo de geometria
        tipoGeom = self.diccionarioGeom[capaParam]

        '''
        elif capaParam == 'areas_inscritas':
            stringCapa = 'Polygon?crs=epsg:' + str(QSettings().value('srid')) + '&field=id:string(15)&field=valor:integer(15)&field=descripcion:string(15)&field=clave:string(15)&index=yes'
        '''
        if capaParam == 'predios.num':
            stringCapa = 'Point?crs=epsg:' + str(QSettings().value('srid')) + '&field=numExt:string(50)'
        elif capaParam == 'horizontales.num':
            stringCapa = 'Point?crs=epsg:' + str(QSettings().value('srid')) + '&field=num_ofi:string(50)'
        else:
            headers = {'Content-Type': 'application/json', 'Authorization' : self.obtenerToken()}
            
            stringTabla = self.diccionarioTabla[capaParam]
            urlCapas = 'http://201.165.150.64:8080/busquedasimplewkn/api/thematics/lista/campos/' + stringTabla + '/' + 'false'

            #urlCapas = 'https://thesmartflat.cianet.mx/cartografico/api/busquedasimplewkn/api/thematics/lista/campos/' + stringTabla + '/' + 'false'

            urlCapas = 'http://192.168.0.25:8080/busquedasimplewkn/api/thematics/lista/campos/' + stringTabla + '/' + 'false'

            respuesta = requests.post(urlCapas, headers = headers)
            
            stringCapa = tipoGeom + "?crs=epsg:" + str(QSettings().value('srid'))

            if respuesta.status_code == 200:
                datos = respuesta.json()
                
                for campo in datos:

                    longitud = campo['longitud']

                    name = campo['name']
                    tipo = self.diccionarioTipo[campo['type']]

                    stringCapa += '&field='
                    stringCapa += name + ':'
                    stringCapa += tipo

                    if longitud != None:
                        stringCapa += "("+str(longitud)+")"
                    
                stringCapa += '&index=yes'
                
            else:
            
                print(respuesta.status_code)
           
        nuevaCapa = QgsVectorLayer(stringCapa, capaParam, 'memory')
        
        if capaParam == 'manzana':
            QSettings().setValue('sManzana', stringCapa)
            '''
            QSettings().setValue('xManzana', nuevaCapa.id())
            render = nuevaCapa.renderer()
            symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#F5A9F2', 'width_border':'0.5'})
            render.setSymbol(symbol)
            '''
        
        elif capaParam == 'predios.geom':
            QSettings().setValue('sPredGeom', stringCapa)
            '''
            QSettings().setValue('xPredGeom', nuevaCapa.id())
            render = nuevaCapa.renderer()
            symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#00ff00', 'width_border':'0.5'})
            render.setSymbol(symbol)
            '''

        elif capaParam == 'predios.num':
            QSettings().setValue('sPredNum', stringCapa)
            '''
            QSettings().setValue('xPredNum', nuevaCapa.id())
            props = nuevaCapa.renderer().symbol().symbolLayer(0).properties()
            props['color'] = '#00FF00'
            nuevaCapa.renderer().setSymbol(QgsMarkerSymbol.createSimple(props))
            '''

        elif capaParam == 'construcciones':
            QSettings().setValue('sConst', stringCapa)
            '''
            QSettings().setValue('xConst', nuevaCapa.id())
            road_rules = (
                ('Const_Esp',  'NOT "cve_const_esp" is NULL '),
                ('Construccion', ' "cve_const_esp" is NULL '),
                
            )

            symbolConst = QgsSymbol.defaultSymbol(nuevaCapa.geometryType())
            rendererConst = QgsRuleBasedRenderer(symbolConst)
            fillConst = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#000000', 'width_border':'0.5'})
            fillEsp = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#00FFFF', 'width_border':'0.5'})

            # get the "root" rule
            root_rule = rendererConst.rootRule()
            for label, expression in road_rules:
                # create a clone (i.e. a copy) of the default rule
                rule = root_rule.children()[0].clone()
                # set the label, expression and color
                rule.setLabel(label)
                rule.setFilterExpression(expression)

                if label == "Const_Esp":
                    rule.setSymbol(fillEsp)
                else:
                    rule.setSymbol(fillConst)

                root_rule.appendChild(rule)
            root_rule.removeChildAt(0)
            #apply the renderer to the layer
            nuevaCapa.setRenderer(rendererConst)
            '''

        elif capaParam == 'horizontales.geom':
            QSettings().setValue('sHoriGeom', stringCapa)
            '''
            QSettings().setValue('xHoriGeom', nuevaCapa.id())
            render = nuevaCapa.renderer()
            symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#C68C21', 'width_border':'0.5'})
            render.setSymbol(symbol)
            '''

        
        elif capaParam == 'horizontales.num':
            QSettings().setValue('sHoriNum', stringCapa)
            '''
            QSettings().setValue('xHoriNum', nuevaCapa.id())
            props = nuevaCapa.renderer().symbol().symbolLayer(0).properties()
            props['color'] = '#C68C21'
            nuevaCapa.renderer().setSymbol(QgsMarkerSymbol.createSimple(props))
            '''

        elif capaParam == 'verticales':
            QSettings().setValue('sVert', stringCapa)
            '''
            QSettings().setValue('xVert', nuevaCapa.id())
            render = nuevaCapa.renderer()
            symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#ff9900', 'width_border':'0.5'})
            render.setSymbol(symbol)
            '''
            
        elif capaParam == 'cves_verticales':
            QSettings().setValue('sCvesVert', stringCapa)
            '''
            QSettings().setValue('xCvesVert', nuevaCapa.id())
            props = nuevaCapa.renderer().symbol().symbolLayer(0).properties()
            props['color'] = '#ff9900'
            nuevaCapa.renderer().setSymbol(QgsMarkerSymbol.createSimple(props))
            '''
        '''
        elif capaParam == 'areas_inscritas':
            QSettings().setValue('sAreasInscritas', stringCapa)
            '' '
            QSettings().setValue('xAreasInscritas', nuevaCapa.id())
            render = nuevaCapa.renderer()
            symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#F646F3', 'width_border':'0.5'})
            render.setSymbol(symbol)
            '' '
        '''
        
        #QSettings().setValue('cAreasInscritas', nuevaCapa)
        '''
        QgsProject.instance().addMapLayers([nuevaCapa], False)
        
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup('consulta')
        capaArbol = QgsLayerTreeLayer(nuevaCapa)
        
        group.insertChildNode(0, capaArbol)

        self.etiquetarCapa(capaParam)
        #self.ineditarCapa(capaParam)

        '''

##################################################################################################################

    def cargarWorkstation(self):
        GAzu = QgsVectorLayer('Polygon?crs=epsg:32614&field=clave:string(15)&index=yes', 'Polis Azules', 'memory')
        GVer = QgsVectorLayer('Polygon?crs=epsg:32614&field=clave:string(15)&index=yes', 'Polis Verdes', 'memory')
        GRoj = QgsVectorLayer('Polygon?crs=epsg:32614&field=clave:string(15)&index=yes', 'Polis Rojos', 'memory')
        GAma = QgsVectorLayer('Polygon?crs=epsg:32614&field=clave:string(15)&index=yes', 'Polis Amarillos', 'memory')

        capaManzana = QgsVectorLayer('Polygon?crs=epsg:32614&field=clave:string(15)&index=yes', 'manzana', 'memory')
        capaPredios = QgsVectorLayer('Polygon?crs=epsg:32614&field=clave:string(15)&index=yes', 'predios.geom', 'memory')
        capaConst = QgsVectorLayer('Polygon?crs=epsg:32614&field=clave:string(15)&index=yes', 'construcciones', 'memory')
        capaHorizontalesG = QgsVectorLayer('Polygon?crs=epsg:32614&field=clave:string(15)&index=yes', 'horizontales.geom', 'memory')
        capaVerticalesG = QgsVectorLayer('Polygon?crs=epsg:32614&field=clave:string(15)&index=yes', 'verticales', 'memory')
        capaVerticalesCve = QgsVectorLayer('Point?crs=epsg:32614&field=clave:string(15)&index=yes', 'cves_verticales', 'memory')
        capaHorizontalesnum = QgsVectorLayer('Point?crs=epsg:32614&field=clave:string(15)&index=yes', 'horizontales.num', 'memory')
        capaPrediosNum = QgsVectorLayer('Point?crs=epsg:32614&field=clave:string(15)&index=yes', 'predios.num', 'memory')

        LAzu = QgsVectorLayer('LineString?crs=epsg:32614&field=clave:string(15)&index=yes', 'Lineas Azules', 'memory')
        LVer = QgsVectorLayer('LineString?crs=epsg:32614&field=clave:string(15)&index=yes', 'Lineas Verdes', 'memory')
        LRoj = QgsVectorLayer('LineString?crs=epsg:32614&field=clave:string(15)&index=yes', 'Lineas Rojos', 'memory')
        LAma = QgsVectorLayer('LineString?crs=epsg:32614&field=clave:string(15)&index=yes', 'Lineas Amarillos', 'memory')

        PAzu = QgsVectorLayer('Point?crs=epsg:32614&field=clave:string(15)&index=yes', 'Puntos Azules', 'memory')
        PVer = QgsVectorLayer('Point?crs=epsg:32614&field=clave:string(15)&index=yes', 'Puntos Verdes', 'memory')
        PRoj = QgsVectorLayer('Point?crs=epsg:32614&field=clave:string(15)&index=yes', 'Puntos Rojos', 'memory')
        PAma = QgsVectorLayer('Point?crs=epsg:32614&field=clave:string(15)&index=yes', 'Puntos Amarillos', 'memory')
        
        self.colorearPuntos(PAzu, '0,181,255,255')
        self.colorearPuntos(PVer, '0,237,32,255')
        self.colorearPuntos(PRoj, '255,67,0,255')
        self.colorearPuntos(PAma, '255,255,0,255')
        
        self.colorearPuntos(capaPrediosNum, '0,255,0,255')
        self.colorearPuntos(capaHorizontalesnum, '198,140,33,255')
        self.colorearPuntos(capaVerticalesCve, '255,153,0,255')

        self.colorearLineas(LAzu, QColor.fromRgb(0,181,255))
        self.colorearLineas(LVer, QColor.fromRgb(0,237,32))
        self.colorearLineas(LRoj, QColor.fromRgb(255,67,0))
        self.colorearLineas(LAma, QColor.fromRgb(255,255,0))
        

        self.colorearPolis(GAzu, '0,181,255,255', '0,181,255,127')
        self.colorearPolis(GVer, '0,237,32,255', '0,237,32,127')
        self.colorearPolis(GRoj, '255,67,0,255', '255,67,0,127')
        self.colorearPolis(GAma, '255,255,0,255', '225,255,0,127')
        

        self.colorearPolis(capaManzana, '#F5A9F2', '255,0,0,0')
        self.colorearPolis(capaPredios, '#00ff00', '255,0,0,0')
        self.colorearPolis(capaConst, '#000000', '255,0,0,0')
        self.colorearPolis(capaHorizontalesG, '#C68C21', '255,0,0,0')
        self.colorearPolis(capaVerticalesG, '#ff9900', '255,0,0,0')

        self.agregarCapaArbol(capaVerticalesCve)
        self.agregarCapaArbol(capaVerticalesG)
        self.agregarCapaArbol(capaHorizontalesnum)
        self.agregarCapaArbol(capaHorizontalesG)
        self.agregarCapaArbol(capaConst)
        self.agregarCapaArbol(capaPrediosNum)
        self.agregarCapaArbol(capaPredios)
        self.agregarCapaArbol(capaManzana) #P
        
        
        
        
        
        

        #self.agregarCapaArbol(GAzu) #P
        #self.agregarCapaArbol(GVer)
        #self.agregarCapaArbol(GRoj)
        #self.agregarCapaArbol(GAma)

        self.agregarCapaArbol(LAzu) #P
        #self.agregarCapaArbol(LVer)
        self.agregarCapaArbol(LRoj)
        #self.agregarCapaArbol(LAma)

        #self.agregarCapaArbol(PAzu)
        #self.agregarCapaArbol(PVer)
        #self.agregarCapaArbol(PRoj)
        #self.agregarCapaArbol(PAma)


    def colorearPuntos(self, capa, color):
        props = capa.renderer().symbol().symbolLayer(0).properties()
        props['color'] = color
        capa.renderer().setSymbol(QgsMarkerSymbol.createSimple(props))

    def colorearPolis(self, capa, contorno, relleno):
        render = capa.renderer()
        symbol = QgsFillSymbol.createSimple({'color':relleno, 'color_border':contorno, 'width_border':'0.2'})
        render.setSymbol(symbol)

    def colorearLineas(self, capa, color):
        symbols = capa.renderer().symbols(QgsRenderContext())
        symbol = symbols[0]
        symbol.setColor(color)

    def agregarCapaArbol(self, capa):
        QgsProject.instance().addMapLayer(capa, True)

    def obtenerCapasDeReferencia(self):

        token = self.obtenerToken()
        print('------------------------------------------')

        print(token)

        print('------------------------------------------')

        pagina = None
        itemsPagina = None

        payload = {"nombre": "e_municipio", "epsg": 32614,"bbox": False,"pin": False,"geomWKT": None, "epsgGeomWKT": 32614,"incluirGeom": True,"pagina": pagina,"itemsPagina": itemsPagina}

        payload.update({'constr': True})

        payload = json.dumps(payload)
        headers = {'Content-Type': 'application/json', 'Authorization' : token}

        #response = requests.post('https://thesmartflat.cianet.mx/cartografico/api/busquedasimplewkn/api/busqueda/simple', headers = headers, data = payload)
        response = requests.post('http://192.168.0.25:8080/busquedasimplewkn/api/busqueda/simple', headers = headers, data = payload)

        if response.status_code == 200:
            data = response.content
            data = json.loads(data.decode('utf-8'))
            
            return data

        else:
            print('Error de servidor obtenerRef ----- ', response.text, 'Cargar capas de referencia')

    def pintarMpio(self):

        capaAPintar = QgsProject.instance().mapLayer(QSettings().value('xMunicipio'))

        data = self.obtenerCapasDeReferencia()

        vaciada = False

        srid = QSettings().value('srid')

        if srid is None or srid == 'None':
            srid = '32614'

        inSpatialRef = osr.SpatialReference()
        inSpatialRef.ImportFromEPSG(int(srid))
        outSpatialRef = osr.SpatialReference()
        outSpatialRef.ImportFromEPSG(int(srid))
        coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
        if not bool(data):
            print('ERROR: REF00000000000000000000000000000000000000000000000')
        
        if data['features'] != []:

            varKeys = data['features'][0]['properties']

            keys = list(varKeys.keys())
            properties = []
            geoms = []
            for feature in data['features']:
                geom = feature['geometry']
                
                if geom == None:
                    continue

                property = feature['properties']
                geom = json.dumps(geom)
                geometry = ogr.CreateGeometryFromJson(geom)
                geometry.Transform(coordTrans)
                geoms.append(geometry.ExportToWkt())
                l = []
                for i in range(0, len(keys)):
                    l.append(property[keys[i]])
                properties.append(l)


        nameCapa = 'Municipios'

        # NO es la de calles   
        if data['features'] != []:
            fields = ""
            for k in keys:
                fields = fields + "&field=" + k + ":string(15)"

            uriFigura = 'Polygon'

            uri = str(uriFigura)+"?crs=epsg:" + str(srid) + fields + "&index=yes"
        else:
            uri = self.obtenerCampos(nameCapa)

        # valida si se debe de pintar de nuevo la capa o utilizar la que ya existe
        
        mem_layer = QgsVectorLayer(uri, nameCapa, 'memory')

        render = mem_layer.renderer()
        symbol = QgsFillSymbol.createSimple({'color':'255,0,0,0', 'color_border':'#3579b1', 'width_border':'0.5'})
        render.setSymbol(symbol)

        QSettings().setValue('xMunicipio', mem_layer.id())

        mem_layer.setReadOnly(True)

        if data['features'] != []:
            prov = mem_layer.dataProvider()
            feats = [ QgsFeature() for i in range(len(geoms)) ]
            for i, feat in enumerate(feats):
                feat.setAttributes(properties[i])
                feat.setGeometry(QgsGeometry.fromWkt(geoms[i]))

            prov.addFeatures(feats)
            


        etiquetaField = ""
        esExpresion = False
        colorCapa = QColor(0,0,0)
        
        etiquetaField = 'nombre'
        colorCapa = QColor(53,121,177)

        settings = QgsPalLayerSettings()
        settings.placement = QgsPalLayerSettings.AroundPoint
        settings.fieldName = etiquetaField
        settings.enabled = True
        settings.isExpression = esExpresion
        
        settings.centroidWhole = True

        textFormat = QgsTextFormat()
        textFormat.setSize(8)
        textFormat.setNamedStyle('Bold')
        textFormat.setColor(colorCapa)

        settings.setFormat(textFormat)

        labeling = QgsVectorLayerSimpleLabeling(settings)

        mem_layer.setLabeling(labeling)
        mem_layer.setLabelsEnabled(True)

        mem_layer.triggerRepaint()
        root = QgsProject.instance().layerTreeRoot()
        
        grupo = root.findGroup('edicion')
        if grupo is None:
            root.addGroup('edicion')

            root = QgsProject.instance().layerTreeRoot()
            grupo = root.findGroup('edicion')

        QgsProject.instance().addMapLayers([mem_layer], False)
        
        mzaNL = QgsLayerTreeLayer(mem_layer)

        # se agrega el grupo de referencia en caso de que no se tenga
        grupo.insertChildNode(0, mzaNL)


    def obtenerCampos(self, nombreCapa):

        listaCampos = {}
        listaTipos = {}

        listaCampos['Municipios'] = ['clave', 'cve_cat', 'id', 'nombre']
        listaTipos['Municipios'] = ['string(5)', 'string(30)', 'integer', 'string(100)']

        stringCapa = "Polygon?crs=epsg:" + str(QSettings().value('srid'))

        campos = listaCampos[nombreCapa]
        tipos = listaTipos[nombreCapa]

        for indice in range(0, len(campos)):

            name = campos[indice]
            tipo = tipos[indice]

            stringCapa += '&field='
            stringCapa += name + ':'
            stringCapa += tipo

        stringCapa += '&index=yes'
        
        return stringCapa

startup = Startup()
startup.mostrarConsola()
startup.checarLogin()
#startup.cargarCapas('')
'''
data = startup.obtenerCapasDeReferencia()
print('aqio-------------------------------')
print(data)
print('aqio-------------------------------')
'''
#startup.pintarMpio()
#startup.cargarWorkstation()
#startup.cargarCapas()



