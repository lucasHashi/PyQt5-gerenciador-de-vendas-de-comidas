import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

qt_tela_inicial = "tela_principal.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    switch_tela_cadastro_ingrediente = QtCore.pyqtSignal()
    switch_tela_gerenciar_ingrediente = QtCore.pyqtSignal()
    
    switch_tela_cadastro_receita = QtCore.pyqtSignal()
    switch_tela_gerenciar_receita = QtCore.pyqtSignal()
    
    switch_tela_cadastro_fabricacoes = QtCore.pyqtSignal()
    switch_tela_gerenciar_fabricacoes = QtCore.pyqtSignal()
    
    switch_tela_cadastro_embalagens = QtCore.pyqtSignal()
    switch_tela_gerenciar_embalagens = QtCore.pyqtSignal()
    
    switch_tela_cadastro_compras = QtCore.pyqtSignal()
    switch_tela_gerenciar_compras = QtCore.pyqtSignal()
    
    switch_tela_gerenciar_marcas = QtCore.pyqtSignal()
    switch_tela_gerenciar_lojas = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #CONFIG BOTOES
        self.btn_ingredientes_adicionar.pressed.connect(lambda: self.abrir_tela_adicionar('ingredientes'))
        self.btn_ingredientes_gerenciar.pressed.connect(lambda: self.abrir_tela_gerenciar('ingredientes'))

        self.btn_receitas_adicionar.pressed.connect(lambda: self.abrir_tela_adicionar('receitas'))
        self.btn_receitas_gerenciar.pressed.connect(lambda: self.abrir_tela_gerenciar('receitas'))

        self.btn_fabricacoes_adicionar.pressed.connect(lambda: self.abrir_tela_adicionar('fabricacoes'))
        self.btn_fabricacoes_gerenciar.pressed.connect(lambda: self.abrir_tela_gerenciar('fabricacoes'))

        self.btn_vendas_adicionar.pressed.connect(lambda: self.abrir_tela_adicionar('vendas'))
        self.btn_vendas_gerenciar.pressed.connect(lambda: self.abrir_tela_gerenciar('vendas'))

        self.btn_embalagens_adicionar.pressed.connect(lambda: self.abrir_tela_adicionar('embalagens'))
        self.btn_embalagens_gerenciar.pressed.connect(lambda: self.abrir_tela_gerenciar('embalagens'))

        self.btn_compras_adicionar.pressed.connect(lambda: self.abrir_tela_adicionar('compras'))
        self.btn_compras_gerenciar.pressed.connect(lambda: self.abrir_tela_gerenciar('compras'))
        
        self.btn_marcas_gerenciar.pressed.connect(lambda: self.abrir_tela_gerenciar('marcas'))
        self.btn_lojas_gerenciar.pressed.connect(lambda: self.abrir_tela_gerenciar('lojas'))

    def abrir_tela_adicionar(self, nomeTela):
        if(nomeTela == 'ingredientes'):
            self.switch_tela_cadastro_ingrediente.emit()
        elif(nomeTela == 'receitas'):
            self.switch_tela_cadastro_receita.emit()
        elif(nomeTela == 'fabricacoes'):
            self.switch_tela_cadastro_fabricacoes.emit()
        elif(nomeTela == 'vendas'):
            self.switch_tela_cadastro_vendas.emit()
        elif(nomeTela == 'embalagens'):
            self.switch_tela_cadastro_embalagens.emit()
        elif(nomeTela == 'compras'):
            self.switch_tela_cadastro_compras.emit()
        else:
            print('TROCAR PARA TELA ADICIONAR',str(nomeTela))
    
    def abrir_tela_gerenciar(self, nomeTela):
        if(nomeTela == 'ingredientes'):
            self.switch_tela_gerenciar_ingrediente.emit()
        elif(nomeTela == 'receitas'):
            self.switch_tela_gerenciar_receita.emit()
        elif(nomeTela == 'fabricacoes'):
            self.switch_tela_gerenciar_fabricacoes.emit()
        elif(nomeTela == 'vendas'):
            self.switch_tela_gerenciar_vendas.emit()
        elif(nomeTela == 'embalagens'):
            self.switch_tela_gerenciar_embalagens.emit()
        elif(nomeTela == 'compras'):
            self.switch_tela_gerenciar_compras.emit()
        elif(nomeTela == 'marcas'):
            self.switch_tela_gerenciar_marcas.emit()
        elif(nomeTela == 'lojas'):
            self.switch_tela_gerenciar_lojas.emit()
        else:
            print('TROCAR PARA TELA GERENCIAR',str(nomeTela))