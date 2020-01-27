import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita

qt_tela_inicial = "tela_cadastro_loja_embala.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    switch_tela_gerenciar_loja_embala = QtCore.pyqtSignal(int, int, float, str, str, int, str, float, str)

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #CONFIG BOTOES
        self.btn_cadastrar.pressed.connect(self.cadastrar_loja_embala)
        self.btn_limpar.pressed.connect(self.limpar_loja_embala)

        self.btn_ativa_loja.pressed.connect(self.ativar_loja)

        self.btn_sair.pressed.connect(self.fechar_tela)

        #CARREGAR COMBO INGREDIENTES
        self.carrega_ingredientes()

        #QUANDO UM INGREDIENTE FOR SELECIONADO NA COMBO
        self.combo_ingrediente.currentIndexChanged.connect(self.ingrediente_selecionado)

        #QUANDO UMA EMBALAGEM FOR DOUBLE-CLICADA
        self.list_embalagens.itemDoubleClicked.connect(self.embalagem_selecionada)
    
        #QUANDO SELECIONAR UMA LOJA, COLOCAR NO TXT_LOJA
        self.carrega_lojas()
        self.combo_loja.currentIndexChanged.connect(self.loja_selecionada)

        #QUANDO UM CADASTRADO FOR DOUBLE-CLICADO
        self.tb_loja_embala_cadastrados.cellDoubleClicked.connect(self.loja_embala_selecionado)

        #ATUALIZA A TABLE LOJA_EMBALA
        #self.carrega_loja_embala()

        header = self.tb_loja_embala_cadastrados.horizontalHeader() 
        self.tb_loja_embala_cadastrados.setHorizontalHeaderLabels(['Codigo', 'Tamanho', 'Unidade', 'Marca', 'Loja', 'Preço'])
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
    
    def carrega_loja_embala(self, id_ingrediente):
        lista_dados = database_receita.select_loja_embala_por_ingrediente_lista(id_ingrediente)
        
        self.tb_loja_embala_cadastrados.setRowCount(0)
        for linha in range(len(lista_dados)):
            self.tb_loja_embala_cadastrados.insertRow(linha)
            for coluna in range(len(lista_dados[0])):
                self.tb_loja_embala_cadastrados.setItem(linha,coluna, QtWidgets.QTableWidgetItem(str(lista_dados[linha][coluna])))

    def embalagem_selecionada(self, item):
        self.combo_loja.setEnabled(True)
        self.btn_ativa_loja.setEnabled(True)
        
        self.btn_cadastrar.setEnabled(True)
        self.btn_limpar.setEnabled(True)

        self.double_preco.setEnabled(True)

        self.txt_embalagem.setText(str(item.text()))

    def loja_selecionada(self, item):
        try:
            _, nome = str(self.combo_loja.currentText()).split(' - ')
            
            self.txt_loja.setText(nome)
        except:
            self.txt_loja.clear()

    def ingrediente_selecionado(self, item):
        try:
            id_ingrediente = str(self.combo_ingrediente.currentText()).split(' - ')[0]
            self.carrega_embalagens(id_ingrediente)
            self.list_embalagens.setEnabled(True)
            self.carrega_loja_embala(id_ingrediente)
        except:
            self.list_embalagens.setEnabled(False)

    def carrega_ingredientes(self):
        lista_ingredientes = ['Ingredientes cadastrados']
        lista_ingredientes += database_receita.select_ingredientes_nomes()
        self.combo_ingrediente.addItems(lista_ingredientes)

    def cadastrar_loja_embala(self):
        try:
            id_loja, nome_loja = self.combo_loja.currentText().split(' - ')
        except ValueError:
            id_loja, nome_loja = 0, self.txt_loja.text()
        #CADASTRA LOJA SE FOR NOVA
        if(self.txt_loja.isEnabled()):
            id_loja = database_receita.insere_loja(nome_loja)

        #PEGAR OS DADOS: ID_LOJA, ID_EMBALAGEM, PRECO
        id_embalagem = int(str(self.txt_embalagem.text()).split(' - ')[0])
        preco = self.double_preco.value()

        #CADASTRA LOJA_EMBALA
        database_receita.insere_loja_embala(preco, id_loja, id_embalagem)

        #ATUALIZA A TABLE LOJA_EMBALA
        id_ingrediente = self.combo_ingrediente.currentText().split(' - ')[0]
        self.carrega_loja_embala(id_ingrediente)

        #LIMPA: LOJA, PRECO, TXT_EMBALAGEM
        self.txt_loja.clear()
        self.txt_loja.setEnabled(False)
        self.btn_ativa_loja.setText('+')
        self.btn_ativa_loja.setEnabled(False)
        self.carrega_lojas()

        self.double_preco.clear()
        self.double_preco.setEnabled(False)

        self.txt_embalagem.clear()

        #DESATIVA BOTOES: CADASTRAR, LIMPAR
        self.btn_cadastrar.setEnabled(False)
        self.btn_limpar.setEnabled(False)

    def carrega_embalagens(self, id_ingrediente):
        self.list_embalagens.clear()
        lista_embalagens = database_receita.select_embalagens_por_ingrediente_nomes(id_ingrediente)
        
        self.list_embalagens.addItems(lista_embalagens)
    
    def carrega_lojas(self):
        self.combo_loja.clear()
        lista_lojas = ['Lojas cadastradas']
        lista_lojas += database_receita.select_lojas_nomes()
        self.combo_loja.addItems(lista_lojas)

    def ativar_loja(self):
        if(self.txt_loja.isEnabled()):
            self.txt_loja.clear()
            self.txt_loja.setEnabled(False)
            self.btn_ativa_loja.setText('+')
            self.combo_loja.setEnabled(True)
        else:
            self.txt_loja.setEnabled(True)
            self.btn_ativa_loja.setText('-')
            self.combo_loja.setEnabled(False)

    
    def limpar_loja_embala(self):
        #LIMPA: LOJA, PRECO, TXT_EMBALAGEM
        self.txt_loja.clear()
        self.txt_loja.setEnabled(False)
        self.btn_ativa_loja.setText('+')
        self.btn_ativa_loja.setEnabled(False)
        self.carrega_lojas()

        self.double_preco.clear()
        self.double_preco.setEnabled(False)

    
    def loja_embala_selecionado(self, linha, coluna):
        id_loja_embala = self.tb_loja_embala_cadastrados.item(linha, 0).text()
        
        _, _, id_loja, id_embalagem = database_receita.select_loja_embala_por_id(id_loja_embala)

        tamanho = self.tb_loja_embala_cadastrados.item(linha, 1).text()
        unidade = self.tb_loja_embala_cadastrados.item(linha, 2).text()
        marca = self.tb_loja_embala_cadastrados.item(linha, 3).text()

        nome_loja = self.tb_loja_embala_cadastrados.item(linha, 4).text()

        preco = self.tb_loja_embala_cadastrados.item(linha, 5).text()

        ingrediente = self.combo_ingrediente.currentText().split(' - ')[1]

        print(id_loja_embala, id_embalagem, tamanho, unidade, marca, id_loja, nome_loja, preco, ingrediente)

        self.switch_tela_gerenciar_loja_embala.emit(int(id_loja_embala), int(id_embalagem), float(tamanho), unidade, marca, int(id_loja), nome_loja, float(preco), ingrediente)

    def fechar_tela(self):
        self.close()



