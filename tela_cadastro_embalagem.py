import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita

qt_tela_inicial = "tela_cadastro_embalagem.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #CONFIG BOTOES
        self.btn_limpar.pressed.connect(self.limpar)
        self.btn_voltar.pressed.connect(self.fechar_tela)
        self.btn_cad_sair.pressed.connect(self.cadastrar_voltar)
        self.btn_cad_limpar.pressed.connect(self.cadastrar_limpar)

        self.btn_ativa_marca.pressed.connect(self.ativa_marca)

        self.carrega_combo_ingredientes()

        self.carrega_combo_marcas()

        self.combo_ingrediente.currentIndexChanged.connect(self.combo_ingrediente_selecionado)
    
    def cadastrar_voltar(self):
        tamanho = self.txt_tamanho.text()
        tamanho = True if(tamanho.replace(' ','')) else False
        
        if(tamanho):
            self.cadastrar()
            self.fechar_tela()

    def cadastrar_limpar(self):
        tamanho = self.txt_tamanho.text()
        tamanho = True if(tamanho.replace(' ','')) else False
        
        if(tamanho):
            self.cadastrar()
            self.limpar()

    def cadastrar(self):
        id_marca = 0
        nome_marca = ''

        if(self.txt_marca.isEnabled()):
            nome_marca = self.txt_marca.text()
            if(not database_receita.verifica_marca_duplicada(nome_marca)):
                id_marca = database_receita.insere_marca(nome_marca)
        else:
            id_marca, nome_marca = str(self.combo_marca.currentText()).split(' - ')

        id_ingrediente = str(self.combo_ingrediente.currentText()).split(' - ')[0]
        tamanho = self.txt_tamanho.text()

        if(not database_receita.verifica_embalagem_duplicada(tamanho, id_ingrediente, id_marca)):
            database_receita.insere_embalagem(tamanho, id_ingrediente, id_marca)

    def ativa_marca(self):
        if(self.txt_marca.isEnabled()):
            self.txt_marca.setEnabled(False)
            self.txt_marca.clear()
            self.combo_marca.setEnabled(True)
            self.btn_ativa_marca.setText('+')
        else:
            self.txt_marca.setEnabled(True)
            self.combo_marca.setEnabled(False)
            self.btn_ativa_marca.setText('-')

    def combo_ingrediente_selecionado(self, item):
        try:
            id_ingrediente, nome, unidade = str(self.combo_ingrediente.currentText()).split(' - ')
            self.txt_unidade.setText(unidade)
        except:
            self.txt_unidade.clear()
    
    def carrega_combo_ingredientes(self):
        self.combo_ingrediente.clear()
        
        nomes_ingredientes = ['Ingredientes ja cadastrados']
        nomes_ingredientes += database_receita.select_ingredientes_nomes()
        
        self.combo_ingrediente.addItems(nomes_ingredientes)
    
    def carrega_combo_marcas(self):
        self.combo_marca.clear()
        
        nomes_marcas = ['Marcas ja cadastradas']
        nomes_marcas += database_receita.select_marcas_nomes()
        
        self.combo_marca.addItems(nomes_marcas)

    def fechar_tela(self):
        self.close()

    def limpar(self):
        self.txt_marca.setEnabled(False)
        self.txt_marca.clear()
        self.combo_marca.setEnabled(True)
        self.btn_ativa_marca.setText('+')
        self.txt_tamanho.clear()
        self.txt_unidade.clear()
        self.carrega_combo_ingredientes()
        self.carrega_combo_marcas()

        

