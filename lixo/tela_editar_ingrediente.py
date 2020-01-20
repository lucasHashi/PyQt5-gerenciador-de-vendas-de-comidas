import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita

qt_tela_inicial = "tela_editar_ingrediente.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    switch_tela_gerenciar_ingrediente = QtCore.pyqtSignal()

    def __init__(self,cod,nome,tamanho,unidade,marca):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        
        #CONFIG BOTOES
        self.btn_limpar.pressed.connect(self.limpar)
        self.btn_voltar.pressed.connect(self.fechar_tela)
        self.btn_editar.pressed.connect(self.editar_voltar)

        self.txt_codigo.setText(str(cod))
        self.txt_nome.setText(nome)
        self.txt_tam_embalagem.setText(str(tamanho))
        self.txt_unidade.setText(unidade)
        self.txt_marca.setText(marca)
        
        self.txt_nome.setPlaceholderText(nome)
        self.txt_tam_embalagem.setPlaceholderText(str(tamanho))
        self.txt_unidade.setPlaceholderText(unidade)
        self.txt_marca.setPlaceholderText(marca)

        
        self.carrega_combo_marcas()
        
        
    
    def editar_voltar(self):
        self.editar()
        self.fechar_tela()

    def editar(self):
        cod = self.txt_codigo.text()
        nome_ingred = self.txt_nome.text()
        unidade = self.txt_unidade.text()
        tamanho = float(str(self.txt_tam_embalagem.text()).replace(',','.'))
        nomeMarca = self.txt_marca.text()

        if(nomeMarca.replace(' ','')):
            #ADICIONA ESSA NOVA MARCA
            database_receita.insere_marca(nomeMarca)
            #SELECIONA O id_marca DA MARCA COM nome = 'nomeMarca'
            id_marca = int(database_receita.select_marca_por_nome(nomeMarca))
            self.carrega_combo_marcas()
        else:
            id_marca = int(str(self.combo_marca.currentText()).split(' - ')[0])

        if(not database_receita.varifica_ingrediente_duplicado(nome_ingred, unidade,tamanho,id_marca)):
            database_receita.update_ingrediente(cod, nome_ingred, unidade, tamanho, id_marca)

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
        self.switch_tela_gerenciar_ingrediente.emit()

    def limpar(self):
        self.txt_nome.clear()
        self.txt_tam_embalagem.clear()
        self.txt_unidade.clear()
        self.txt_marca.clear()
        self.txt_marca.setEnabled(False)
