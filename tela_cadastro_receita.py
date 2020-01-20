import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita

qt_tela_inicial = "tela_cadastro_receita.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        self.receita_ativa = False
        self.id_receita_atual = 0

        #CONFIG BOTOES
        self.btn_adicionar.pressed.connect(self.adicionar_ingrediente)
        self.btn_remover.pressed.connect(self.remover_ingrediente)
        self.btn_iniciar.pressed.connect(self.iniciar_receita)

        self.btn_recomecar.pressed.connect(self.recomecar)
        self.btn_voltar.pressed.connect(self.fechar_tela)
        self.btn_cad_sair.pressed.connect(self.cadastrar_voltar)
        self.btn_cad_limpar.pressed.connect(self.cadastrar_limpar)

        #CARREGAR INGREDIENTES
        lista_ingredientes = database_receita.select_ingredientes_nomes()
        self.list_ingredientes.addItems(lista_ingredientes)

        #QUANDO UM ITEM FOR DOUBLE-CLICADO
        self.list_ingredientes.itemDoubleClicked.connect(self.ingrediente_selecionado)
    
    def adicionar_ingrediente(self):
        if(str(self.txt_ingrediente.text()) and str(self.txt_quantidade.text())):
            #ADICIONAR INGREDIENTE NA TABELA
            ingrediente, quantidade, unidade = str(self.txt_ingrediente.text()).split(' - ')
        else:
            pass
    
    def ingrediente_selecionado(self, item):
        self.txt_ingrediente.setText(str(item.text()))
    
    def remover_ingrediente(self):
        pass

    def cadastrar_voltar(self):
        self.cadastrar()
        self.fechar_tela()

    def cadastrar_limpar(self):
        self.cadastrar()
        self.limpar()

    def cadastrar(self):
        nomeIngred = self.txt_nome.text()
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

        database_receita.insere_ingrediente(nomeIngred, unidade, tamanho, id_marca)

    def carrega_combo_marcas(self):
        self.combo_marca.clear()
        marcas = database_receita.select_marcas_nomes()
        self.combo_marca.addItems(marcas)

    def fechar_tela(self):
        self.close()

    def iniciar_receita(self):
        if(self.txt_nome.isEnabled()):
            self.ativar_receita()
            self.btn_iniciar.setText('Editar')
        else:
            self.desativar_receita()
            self.btn_iniciar.setText('Iniciar')

    def ativar_receita(self):
        self.txt_nome.setEnabled(False)
        self.txt_rendimento.setEnabled(False)
        self.txt_unidade.setEnabled(False)
        self.spin_validade.setEnabled(False)

        self.btn_adicionar.setEnabled(True)
        self.btn_remover.setEnabled(True)

        self.txt_ingrediente.setEnabled(True)
        self.txt_quantidade.setEnabled(True)

        self.list_ingredientes.setEnabled(True)
        self.tb_ingredientes.setEnabled(True)
    
    def desativar_receita(self):
        self.txt_nome.setEnabled(True)
        self.txt_rendimento.setEnabled(True)
        self.txt_unidade.setEnabled(True)
        self.spin_validade.setEnabled(True)

        self.btn_adicionar.setEnabled(False)
        self.btn_remover.setEnabled(False)

        self.txt_ingrediente.setEnabled(False)
        self.txt_quantidade.setEnabled(False)

        self.list_ingredientes.setEnabled(False)
        self.tb_ingredientes.setEnabled(False)

    def recomecar(self):
        self.txt_nome.clear()
        self.txt_rendimento.clear()
        self.txt_unidade.clear()

        self.txt_ingrediente.clear()
        self.txt_quantidade.clear()
        
        self.desativar_receita()
