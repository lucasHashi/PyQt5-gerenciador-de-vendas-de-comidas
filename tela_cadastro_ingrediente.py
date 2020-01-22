import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita

qt_tela_inicial = "tela_cadastro_ingrediente.ui"
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

        self.carrega_combo_ingredientes()

        self.combo_nomes.currentIndexChanged.connect(self.combo_ingrediente_to_nome)
    
    def cadastrar_voltar(self):
        nome = self.txt_nome.text()
        nome = True if(nome.replace(' ','')) else False
        unidade = self.txt_unidade.text()
        unidade = True if(unidade.replace(' ','')) else False
        
        if(nome*unidade):
            self.cadastrar()
            self.fechar_tela()

    def cadastrar_limpar(self):
        nome = self.txt_nome.text()
        nome = True if(nome.replace(' ','')) else False
        unidade = self.txt_unidade.text()
        unidade = True if(unidade.replace(' ','')) else False
        
        if(nome*unidade):
            self.cadastrar()
            self.limpar()

    def cadastrar(self):
        nome_ingred = self.txt_nome.text()
        unidade = self.txt_unidade.text()

        self.carrega_combo_ingredientes()

        if(not database_receita.verifica_ingrediente_duplicado(nome_ingred)):
            database_receita.insere_ingrediente(nome_ingred, unidade)

    def combo_ingrediente_to_nome(self, item):
        try:
            nome, unidade = str(self.combo_nomes.currentText()).split(' - ')
            self.txt_nome.setText(nome)
            self.txt_unidade.setText(unidade)
        except:
            self.txt_nome.clear()
            self.txt_unidade.clear()
    
    def carrega_combo_ingredientes(self):
        self.combo_nomes.clear()
        
        nomes_ingredientes = ['Ingredientes ja cadastrados']
        lista_ingredientes = database_receita.select_ingredientes_nomes()

        if(lista_ingredientes):
            for item in lista_ingredientes:
                cod, nome, unidade = item.split(' - ')
                nome_item = '{} - {}'.format(nome, unidade)
                nomes_ingredientes.append(nome_item)
        
        self.combo_nomes.addItems(nomes_ingredientes)

    def fechar_tela(self):
        self.close()

    def limpar(self):
        self.txt_nome.clear()
        self.txt_unidade.clear()
        self.carrega_combo_ingredientes()

        

