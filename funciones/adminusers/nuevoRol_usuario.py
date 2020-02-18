
import os, requests, json

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'nuevoRol.ui'))

class nuevoRol_usuario(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, CFG = None, UTI = None, parent=None):
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

        self.headers = {'Content-Type': 'application/json'}

        self.setupUi(self)

    def showEvent(self, event):

        if self.cargada:
            return

        # -- Eventos
        self.btnAceptar.clicked.connect(self.event_aceptar)
        self.btnCancelar.clicked.connect(self.event_cancelar)

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
            self.accept()

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
    def consumeWSGeneral(self, url_cons = ""):

        url = url_cons
        data = ""

        try:
            self.headers['Authorization'] = self.UTI.obtenerToken()
            response = requests.post(url, headers = self.headers)
        except requests.exceptions.RequestException as e:
            self.createAlert("Error de servidor--, 'consumeWSGeneral()' '" + str(e) + "'", QMessageBox().Critical, "Error de servidor")
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