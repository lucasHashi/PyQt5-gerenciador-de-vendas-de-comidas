import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita

qt_tela_inicial = "tela_cadastro_marca.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    switch_tela_cadastro_ingrediente = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #CONFIG BOTOES
        self.btn_cadastrar.pressed.connect(self.cadastrar_marca)
        self.btn_voltar.pressed.connect(self.fechar_tela)
    
    def cadastrar_marca(self):
        nomeMarca = str(self.txt_nome.text())
        database_receita.insere_marca(nomeMarca)
        self.fechar_tela()
    
    def fechar_tela(self):
        self.switch_tela_cadastro_ingrediente.emit()