
import os, requests, json

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'cambioClave.ui'))

class cambioClave_Usuario(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, CFG = None, UTI = None, usuario = None, parent=None, nuevo = False):
        """Constructor."""
        super(cambioClave_Usuario, self).__init__(parent, \
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
        self.usuario = usuario
        self.nuevo = nuevo

        self.headers = {'Content-Type': 'application/json'}

        self.setupUi(self)

    def showEvent(self, event):

        if self.cargada:
            return

        # -- Eventos
        self.btnAceptar.clicked.connect(self.event_aceptar)
        self.btnCancelar.clicked.connect(self.event_cancelar)

        # -- Iniciarlizaciones
        us = ''

        if self.usuario:
            us = (self.usuario['firstName'] if self.usuario['firstName'] else '') + ' ' + (self.usuario['lastName'] if self.usuario['lastName'] else '')

        self.lbDatoUsuario.setText(us.strip())


        # sin edicion en la tabla (QTableWidget)
        self.cargada = True

    # --- E V E N T O S   Dialog ---

    # -- aceptar el cambio la fusion de fracciones
    def event_aceptar(self):
        texto = self.leRol.text()
        texto_2 = self.leRol_2.text()
        if texto == texto_2:
            if texto == '':
                self.createAlert('Llene los campos.')
                return

           
            resp = self.cambiarContraseña(nuevo = self.nuevo, url = (self.CFG.url_AU_actualizarContrasena), texto = self.leRol.text())
            #print(envio)
            if resp == 'OK':
                self.createAlert('Contraseña actualizada con exito', QMessageBox().Information)
                self.accept()
            else:
                return
        else:
             self.createAlert('Las conraseñas no coinciden.') 

    # -- cancelar la fusion de fracciones
    def event_cancelar(self):
        self.reject() 

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
    def cambiarContraseña(self, nuevo = False, url = '', texto = ''):
        data = ""
        
        # envio - el objeto de tipo dict, es el json que se va a guardar
        # se debe hacer la conversion para que sea aceptado por el servicio web
        
        print(data)
        try:
            # header para obtener el token
            self.headers['Authorization'] = self.UTI.obtenerToken()

            if nuevo:
                response = requests.post(url, headers = self.headers, data = texto)
           

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

    def consumeWSGeneral(self, url_cons = ""):

        url = url_cons
        data = ""

        try:
            self.headers['Authorization'] = self.UTI.obtenerToken()
            response = requests.get(url, headers = self.headers)
        except requests.exceptions.RequestException as e:
            self.createAlert("Error de servidor, 'consumeWSGeneral()' '" + str(e) + "'", QMessageBox().Critical, "Error de servidor")
            return

        if response.status_code == 200:
            data = response.content
            
        elif response.status_code == 403:
            self.createAlert('Sin Permisos para ejecutar la accion', QMessageBox().Critical, "Usuarios")
            return None
           
        else:
            self.createAlert('Error en peticion "consumeWSGeneral()":\n' + response.text, QMessageBox().Critical, "Error de servidor")
            return

        return json.loads(data)

    # --- S E R V I C I O S   W E B   CIERRA ---