
import os

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSettings
from qgis.utils import iface

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'estatusClaves_dialog_base.ui'))

class EstatusClavesDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None, pluginV=None, tipo = '', claveActual = '', claveFiltro = '', referencia = False):
        """Constructor."""
        super(EstatusClavesDialog, self).__init__(parent, \
            flags=Qt.WindowCloseButtonHint)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        
        self.tipo = tipo
        self.claveActual = claveActual
        self.claveFiltro = claveFiltro
        self.referencia = referencia
        self.setupUi(self)

########################################################################

    def showEvent(self, event):

        # eventos
        self.botonConfirmar.clicked.connect(self.event_aceptar)
        self.botonCancelar.clicked.connect(self.event_cancelar)
        self.leClaveAnterior.setText(self.claveActual)

########################################################################

    def closeEvent(self, evnt):
        pass
        #if not self.pluginV.posibleCerrar:
        #evnt.ignore()

##########################################################################

    # -- E V E N T O S   C O N T R O L A D O S -- #

    # -- aceptar el cambio la fusion de fracciones
    def event_aceptar(self):

        estatus = self.comboManzana.currentText()
        clave = self.claveActual
        m = {}
        m['clave'] = clave
        m['claveFiltro'] = self.claveFiltro
        m['estatus'] = estatus
        m['tipo'] = self.tipo

        # se obtiene la lista de las claves cambiadas por estatus de uso
        lista = QSettings().value('clavesEstatusRef' if self.referencia else 'clavesEstatus')
        if not lista:
            lista = []

        lista.append(m)

        # se almacena la lista de claves
        QSettings().setValue('clavesEstatusRef' if self.referencia else 'clavesEstatus', lista)
        self.accept()

    # -- aceptar el cambio la fusion de fracciones
    def event_cancelar(self):
        self.reject()

    # -- E V E N T O S   C O N T R O L A D O S   C E R R A R -- #