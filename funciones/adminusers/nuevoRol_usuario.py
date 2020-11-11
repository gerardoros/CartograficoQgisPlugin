
import os, requests, json

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from qgis.PyQt.QtWidgets import QAction, QTableWidgetItem
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'nuevoRol.ui'))

class nuevoRol_usuario(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, CFG = None, UTI = None, parent=None, nuevo = False):
        """Constructor."""
        super(nuevoRol_usuario, self).__init__(parent, \
            flags=Qt.WindowCloseButtonHint)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        # -- informacion cargada
        self.cargada = False
        self.CFG = CFG
        self.UTI = UTI
        self._seleccionados = []
        self.nuevo = nuevo
        self.headers = {'Content-Type': 'application/json'}
        self.roles = []
        self.setupUi(self)

    def showEvent(self, event):

        if self.cargada:
            return

        # -- Eventos
        self.btnAceptar.clicked.connect(self.event_aceptar)
        self.btnCancelar.clicked.connect(self.event_cancelar)
        self.twDefinir.hideColumn(1)
        self.traerOperaciones()

        # -- Iniciarlizaciones

        self.cargada = True

    # --- E V E N T O S   Dialog ---

    # -- aceptar el cambio la fusion de fracciones
    def event_aceptar(self):

        texto = self.leRol.text()
        if texto == '':
            self.createAlert('Defina un nombre para el nuevo Rol')
            return

        data = self.consumeWSGeneral(url_cons = self.CFG.url_AU_insertAuthority + texto)

        if data:
            self.editarOperaciones()
            self.accept()

    # -- cancelar la fusion de fracciones
    def event_cancelar(self):
        self.reject()


    def traerOperaciones(self):
        #self.createAlert("Si conecto", QMessageBox().Information, "Si se hizo")
        self.twDefinir.clearContents()
        self.twDefinir.setRowCount(0)
        dev = 'h'

        #print('---------------')
        #print(rol.text())
        #print(self.CFG.url_AU_getAllRole + rol.text())
        #print('---------------')
        

        self.roles = self.consumeWSGeneral_2(url_cons = self.CFG.url_AU_getAllRole + dev )
        #print(self.roles)
        if not self.roles:
             return

                # mostrar usuarios en tabla
        self.twDefinir.setRowCount(len(self.roles))
        for x in range(0, len(self.roles)):
            

           
            check = QTableWidgetItem(self.roles[x]['nombre'])

            #check = QTableWidgetItem(self.roles[x]['asignado'])
            check.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if self.roles[x]['asignado'] == False:
                check.setCheckState(QtCore.Qt.Unchecked)
            else:
                check.setCheckState(QtCore.Qt.Checked)

            #self.twDefinir.setItem(x,0,check)
            
            self.twDefinir.setItem(x, 0, check)
            self.twDefinir.setItem(x, 1, QtWidgets.QTableWidgetItem(str(self.roles[x]['id'])))


    def editarOperaciones(self):

        if self.twDefinir.rowCount() > 0:

            texto = self.leRol.text()
            
            # obtenemos el numero total de registros en el qtablewidget
            allRows = self.twDefinir.rowCount()

            # inicializamos variable (lista) donde se agregan el texto de los registros activos por check
            self._seleccionados = []

            # se itera los registros del qtablewidget
            for row in range(0, allRows):

                # se obtiene el item segun la iteracion
                # el registro (row) en la posicion 0 (columna 0) 
                # en este ejmplo solo se cuenta con una columna por eso la posicion 0
                item = self.twDefinir.item(row, 0)
                item3 = self.twDefinir.item(row, 1)

                # se verifica que el checkbox este seleccionado
                if item.checkState() == 2: # True
                    self._seleccionados.append(item3.text())

            
            envio = {}
            envio['permisos'] = self._seleccionados
            envio['rol'] = texto
            resp = self.guardarOperacion(nuevo = self.nuevo, url = (self.CFG.url_AU_actualizarOperaciones), envio = envio)

            if resp == 'OK':
                self.createAlert('Operaciones Asignadas Correctamente', QMessageBox().Information)
            else:
                return
            
            #self.dlg.accept()       
            print(envio)  

    def guardarOperacion(self, nuevo = False, url = '', envio = {}):
        data = ""
        
        # envio - el objeto de tipo dict, es el json que se va a guardar
        # se debe hacer la conversion para que sea aceptado por el servicio web
        jsonEnv = json.dumps(envio)
        
        try:
            # header para obtener el token
            self.headers['Authorization'] = self.UTI.obtenerToken()

            if nuevo:
                response = requests.put(url, headers = self.headers, data = jsonEnv)
           

                # ejemplo con put, url, header y body o datos a enviar
               

        except requests.exceptions.RequestException as e:
            self.createAlert("Error de servidor, 'guardarOperacion()' '" + str(e) + "'", QMessageBox().Critical, "Error de servidor")
            return str(e)

        if response.status_code == 403:
            self.createAlert('Sin Permisos para ejecutar la accion', QMessageBox().Critical, "Operaciones")
            return None
           
        elif response.status_code >= 300:
            self.createAlert('Error en peticion "guardarOperacion()":\n' + response.text, QMessageBox().Critical, "Error de servidor")
            return response.text

        return 'OK'
     
    # --- E V E N T O S   Dialog ---

    # --- M E T O D O S   Dialog ---

    # - Crea una alerta para ser mostrada como ventana de advertencia
    def createAlert(self, mensaje, icono = QMessageBox().Critical, titulo = 'Usuarios'):
        #Create QMessageBox
        self.msg = QMessageBox()
        #Add message
        self.msg.setText(mensaje)
        #Add icon of critical error
        self.msg.setIcon(icono)
        #Add tittle
        self.msg.setWindowTitle(titulo)
        #Show of message dialog
        self.msg.show()
         # Run the dialog event loop
        result = self.msg.exec_()

    # --- M E T O D O S   Dialog ---

    # --- S E R V I C I O S   W E B  ---

    # - consume ws para informacion de catalogos
    def consumeWSGeneral_2(self, url_cons = ""):

        url = url_cons
        data = ""

        try:
            self.headers['Authorization'] = self.UTI.obtenerToken()
            response = requests.get(url, headers = self.headers)
        except requests.exceptions.RequestException as e:
            self.createAlert("Error de servidor, 'consumeWSGeneral()'" + str(e) + "'", QMessageBox().Critical, "Error de servidor")
            return

        if response.status_code == 200:
            data = response.content
                   
        else:
            self.createAlert('Error en peticion "consumeWSGeneral()":\n' + response.text, QMessageBox().Critical, "Error de servidor")
            return

        return json.loads(data)
    def consumeWSGeneral(self, url_cons = ""):

        url = url_cons
        data = ""

        try:
            self.headers['Authorization'] = self.UTI.obtenerToken()
            response = requests.post(url, headers = self.headers)
        except requests.exceptions.RequestException as e:
            self.createAlert("Error de servidor, 'consumeWSGeneral()' '" + str(e) + "'", QMessageBox().Critical, "Error de servidor")
            return

        if response.status_code == 200 or response.status_code == 201:
            data = response.content

        elif response.status_code == 202:
            self.createAlert(response.text, QMessageBox().Critical, "Usuarios")
            return None
           
        elif response.status_code == 403:
            self.createAlert('Sin Permisos para ejecutar la accion', QMessageBox().Critical, "Usuarios")
            return None
           
        else:
            self.createAlert('Error en peticion "consumeWSGeneral()":\n' + response.text, QMessageBox().Critical, "Error de servidor")
            return

        return 'OK'

    # --- S E R V I C I O S   W E B   CIERRA ---