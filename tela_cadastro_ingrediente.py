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
        self.btn_ativa_marca.pressed.connect(self.ativa_marca_nova)

        self.carrega_combo_marcas()
    
    def cadastrar_voltar(self):
        self.cadastrar()
        self.fechar_tela()

    def cadastrar_limpar(self):
        self.cadastrar()
        self.limpar()

    def cadastrar(self):
        nomeIngred = self.txt_nome.text()
        unidade = self.txt_unidade.text()
        tamanho = float(self.txt_tam_embalagem.text())
        nomeMarca = self.txt_marca.text()

        if(nomeMarca.replace(' ','')):
            #ADICIONA ESSA NOVA MARCA
            database_receita.insere_marca(nomeMarca)
            #SELECIONA O id_marca DA MARCA COM nome = 'nomeMarca'
            id_marca = int(database_receita.select_marca_por_nome(nomeMarca))
            self.carrega_combo_marcas()
        else:
            id_marca = int(str(self.combo_marca.currentText()).split(' - ')[0])

        database_receita.insere_ingrediente(nomeIngred, unidade, tamanho, id_marca)

    def carrega_combo_marcas(self):
        self.combo_marca.clear()
        marcas = database_receita.select_marcas_nomes()
        self.combo_marca.addItems(marcas)

    def ativa_marca_nova(self):
        if(self.txt_marca.isEnabled()):
            self.txt_marca.setEnabled(False)
            self.btn_ativa_marca.setText('+')
            self.txt_marca.clear()
        else:
            self.txt_marca.setEnabled(True)
            self.btn_ativa_marca.setText('-')

    def fechar_tela(self):
        self.close()

    def limpar(self):
        self.txt_nome.clear()
        self.txt_tam_embalagem.clear()
        self.txt_unidade.clear()
        self.txt_marca.clear()
