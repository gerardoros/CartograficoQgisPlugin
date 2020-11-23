
import os, requests, json

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from .nuevoRol_usuario import nuevoRol_usuario

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'agregarRoles.ui'))

class agregarRoles_usuario(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, nuevalista = [], CFG = None, UTI = None, parent=None):
        """Constructor."""
        super(agregarRoles_usuario, self).__init__(parent, \
            flags=Qt.WindowCloseButtonHint)
        # Set up the user interface from Designer.l
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        # -- informacion cargada
        self.cargada = False

        self._seleccionados = []
        
        self.CFG = CFG
        self.UTI = UTI
        self.nuevalista = nuevalista

        self.headers = {'Content-Type': 'application/json'}

        self.setupUi(self)

    def showEvent(self, event):

        if self.cargada:
            return

        # -- Eventos
        self.btnNuevoRol.clicked.connect(self.event_nuevo)
        self.btnAceptar.clicked.connect(self.event_aceptar)
        self.btnCancelar.clicked.connect(self.event_cancelar)

        self.leBusqueda.textChanged.connect(self.event_textChangedLbBusqueda)

        # -- Iniciarlizaciones
        self.cargaRoles(nuevalista = self.nuevalista)

        # sin edicion en la tabla (QTableWidget)
        self.twRoles.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.twRoles.setColumnWidth(1,269)

        self.cargada = True

    # --- E V E N T O S   Dialog ---

    # - boton presionado dentro de la lista
    def event_currentPositionButtonPressed(self):

        clickme = QtWidgets.qApp.focusWidget()
        # or button = self.sender()
        index = self.twRoles.indexAt(clickme.pos())

        if index.isValid():
            self.twRoles.removeRow(index.row())



    # -- aceptar el cambio la fusion de fracciones
    def event_aceptar(self):

        # se valida si hay registros en el qtablewidget
        if self.twRoles.rowCount() > 0:


            # obtenemos el numero total de registros en el qtablewidget
            allRows = self.twRoles.rowCount()

            # inicializamos variable (lista) donde se agregan el texto de los registros activos por check
            self._seleccionados = []

            # se itera los registros del qtablewidget
            for row in range(0, allRows):

                # se obtiene el item segun la iteracion
                # el registro (row) en la posicion 0 (columna 0) 
                # en este ejmplo solo se cuenta con una columna por eso la posicion 0
                item = self.twRoles.item(row, 0)
                item2 = self.twRoles.item(row, 1)

                # se verifica que el checkbox este seleccionado
                if item.checkState() == 2: # True

                    m = {}
                    m['rol'] = item.text()
                    m['opreaciones'] = item2.text()

                    self._seleccionados.append(m)

        self.accept()

    # -- cancelar la fusion de fracciones
    def event_cancelar(self):
        print('cancelar')
        self.reject()

    # -- abre formulario para agregar nuevo rol
    def event_nuevo(self):
        obj = nuevoRol_usuario(CFG = self.CFG, UTI = self.UTI, nuevo = True)
        respuesta = obj.exec()

        # regresa un 0 o un 1
        # 0 = RECHAZADO = CANCELAR
        # 1 = ACEPTADO  = ACEPTAR
        if respuesta == 0:
            return
            
        # actualiza los roles
        self.actualizaRoles()

    # - cambio de texto para realizar busquedas
    def event_textChangedLbBusqueda(self, texto):
        
        for row in range(0,self.twRoles.rowCount()):
            self.twRoles.showRow(row)

        if texto == '':
            return
        items = self.twRoles.findItems(texto, Qt.MatchContains)

        ocultar = True
        rowCount = self.twRoles.rowCount()
        for row in range(0, rowCount):
            ocultar = True
            for item in items:

                if row == item.row():
                    ocultar = False
                    break

            if ocultar:
                self.twRoles.hideRow(row)


    def actualizaRoles(self):

        # consultar los roles
        roles = self.consumeWSGeneral(url_cons = self.CFG.url_AU_getAllAuthorities)

        if not roles:
            return

        self.limpiaTabla()
        self.cargaRoles(roles = roles)

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

    def cargaRoles(self, nuevalista = []):

        # llena la tabla de roles
        self.twRoles.setRowCount(len(nuevalista))
        for i in range(0, len(nuevalista)):
            
            btnRol = QtWidgets.QPushButton('Quitar')
            btnRol.setStyleSheet('''QPushButton{
                                background : rgb(174, 116, 0);
                                color : rgb(255, 255, 255);
                                font-weight: bold;
                                }
                                QPushButton::disabled {
                                background : rgb(187, 129, 13);
                                color : rgb(245,245,245);
                                border: 1px solid #adb2b5;
                                }''')

            check = QtWidgets.QTableWidgetItem(nuevalista[i]['rol'])
            check.setCheckState(QtCore.Qt.Unchecked)

            self.twRoles.setItem(i, 0, check)
            self.twRoles.setItem(i, 1, QtWidgets.QTableWidgetItem(nuevalista[i]['operaciones']))
            #self.twRoles.setCellWidget(i, 1, btnRol)

            #btnRol.clicked.connect(self.event_currentPositionButtonPressed)

    def limpiaTabla(self):

        # limpiar qTableWidget
        self.twRoles.clearContents()
        self.twRoles.setRowCount(0)
            
        for row in range(0, self.twRoles.rowCount()):        
            self.twRoles.removeRow(row) 

    # --- M E T O D O S   Dialog ---

    # --- S E R V I C I O S   W E B  ---

    # - consume ws para informacion de catalogos
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