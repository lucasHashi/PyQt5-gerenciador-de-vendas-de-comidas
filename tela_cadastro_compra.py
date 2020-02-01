import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita

qt_tela_inicial = "tela_cadastro_compra.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
    
        #INICIA LISTA DE COMPRA
        #LISTA COM LISTAS = [id_loja_embala, ingred, marca, tamanho, unidade, preco, quantidade, custo_final]
        self.lista_compra = []

        #CONFIG BOTOES
        self.btn_adicionar.pressed.connect(self.adicionar_produto)
        self.btn_remover.pressed.connect(self.remover_produto)
        self.btn_iniciar.pressed.connect(self.iniciar_compra)

        self.btn_recomecar.pressed.connect(self.recomecar)
        self.btn_voltar.pressed.connect(self.fechar_tela)
        self.btn_cad_sair.pressed.connect(self.cadastrar_voltar)
        self.btn_cad_limpar.pressed.connect(self.cadastrar_limpar)

        #CARREGAR LOJAS
        self.carrega_combo_lojas()

        #CARREGAR INGREDIENTES
        #self.carrega_combo_ingredientes()

        #QUANDO UM INGREDIENTE FOR SELECIONADO
        self.combo_ingrediente.currentIndexChanged.connect(self.combo_ingrediente_selecionado)

        #CARREGAR EMBALAGENS
        #self.carrega_embalagens()

        #QUANDO UM ITEM FOR DOUBLE-CLICADO
        self.list_embalagens.itemDoubleClicked.connect(self.embalagem_selecionada)

        header = self.tb_produtos.horizontalHeader() 
        self.tb_produtos.setHorizontalHeaderLabels(['Codigo', 'Ingrediente', 'Marca', 'Tamanho', 'Unidade', 'Preço', 'Quantidade', 'Gasto'])
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
    
    def combo_ingrediente_selecionado(self):
        if(not self.combo_ingrediente.currentText() == 'Ingredientes cadastrados'):
            self.carrega_embalagens()
            self.list_embalagens.setEnabled(True)
        else:
            self.list_embalagens.clear()
            self.list_embalagens.setEnabled(False)

    def carrega_embalagens(self):
        self.list_embalagens.clear()
        id_loja = self.combo_loja.currentText().split(' - ')[0]
        id_ingrediente = self.combo_ingrediente.currentText().split(' - ')[0]
        lista_embalagens = database_receita.select_loja_embala_por_ingrediente_loja_nomes(id_loja, id_ingrediente)

        #LISTA TODOS OS CODIGOS DE PRODUTOS JA ADICIONADOS A RECEITA
        codigos_loja_embala = []
        for item in self.lista_compra:
            cod = item[0]
            codigos_loja_embala.append(cod)

        #VERIFICAR SE JA NAO ESTA ADICIONADO A RECEITA
        embalagens_nao_usadas = []
        for item in lista_embalagens:
            cod_embalagem = item.split(' - ')[0]
            if(not cod_embalagem in codigos_loja_embala):
                embalagens_nao_usadas.append(item)
        
        self.list_embalagens.addItems(embalagens_nao_usadas)

    def carrega_produtos_compra(self):
        if(self.lista_compra):
            self.tb_produtos.setRowCount(0)
            for linha in range(len(self.lista_compra)):
                self.tb_produtos.insertRow(linha)
                for coluna in range(len(self.lista_compra[0])):
                    self.tb_produtos.setItem(linha,coluna, QtWidgets.QTableWidgetItem(str(self.lista_compra[linha][coluna])))
        else:
            self.tb_produtos.clear()

    def adicionar_produto(self):
        if(str(self.txt_produto.text()) and int(self.spin_quantidade.value()) > 0):
            #ADICIONAR PRODUTO NA TABELA
            marca, tamanho, unidade, preco, id_loja_embala, _ = str(self.txt_produto.text()).split(' - ')
            quantidade = self.spin_quantidade.value()
            ingred = self.combo_ingrediente.currentText().split(' - ')[1]

            self.lista_compra.append([id_loja_embala, ingred, marca, tamanho, unidade, preco, quantidade, str(int(quantidade)*float(preco))])
            self.carrega_produtos_compra()
            self.carrega_embalagens()

            self.spin_quantidade.setEnabled(False)

            self.txt_produto.clear()
            self.spin_quantidade.setValue(0)
        else:
            pass
    
    def embalagem_selecionada(self, item):
        id_loja_embala, id_marca, marca, tamanho, unidade, preco = str(item.text()).split(' - ')

        self.spin_quantidade.setEnabled(True)

        self.txt_produto.setText(marca+' - '+tamanho+' - '+unidade+' - '+preco+' - '+id_loja_embala+' - '+id_marca)
    
    def remover_produto(self):
        #CASO TENHA UMA LINHA SELECIONADA
        try:
            #PEGAR O CODIGO DO ITEM SELECIONADO
            item = self.tb_produtos.currentItem()
            linha_selec = item.row()
            cod_selecionado = self.tb_produtos.item(linha_selec, 0).text()

            #REMOVER DA LISTA receita PELO CODIGO DA EMBALAGEM
            for i in range(len(self.lista_compra)):
                item = self.lista_compra[i]
                cod = item[0]
                if(cod == cod_selecionado):
                    self.lista_compra.pop(i)
                    break
            
            self.carrega_produtos_compra()
            self.carrega_embalagens()

            self.txt_quantidade.setEnabled(False)

            self.txt_produto.clear()
            self.txt_quantidade.setValue(0)
        except:
            print('erro aqui')
            pass

    def cadastrar_voltar(self):
        if(self.lista_compra):
            self.cadastrar()
            self.fechar_tela()

    def cadastrar_limpar(self):
        if(self.lista_compra):
            self.cadastrar()
            self.recomecar()

    def cadastrar(self):
        data_dia = str(self.date_data.date().day())
        data_mes = str(self.date_data.date().month())
        data_ano = str(self.date_data.date().year())

        #ADICIONAR RECEITA
        id_compra = database_receita.insere_compra('{}-{}-{}'.format(data_ano, data_mes, data_dia))

        #PARA CADA PRODUTO EM lista_compra
        for id_loja_embala, _, _, _, _, preco, quantidade, _ in self.lista_compra:
            #ADICIONAR INGRED NA TABELA DE LIGACAO COM O cod_receita
            database_receita.insere_comp_loja_embala(preco, quantidade, id_compra, id_loja_embala)
    
    def carrega_combo_lojas(self):
        self.combo_loja.clear()
        lojas = ['Lojas cadastradas']
        lojas += database_receita.select_lojas_nomes()
        self.combo_loja.addItems(lojas)
    
    def carrega_combo_ingredientes(self):
        self.combo_ingrediente.clear()
        ingredientes = ['Ingredientes cadastrados']
        id_loja = self.combo_loja.currentText().split(' - ')[0]
        ingredientes += database_receita.select_ingredientes_de_loja(id_loja)
        self.combo_ingrediente.addItems(ingredientes)

    def fechar_tela(self):
        self.close()

    def iniciar_compra(self):
        if(self.date_data.isEnabled() and not self.combo_loja.currentText() == 'Lojas cadastradas'):
            self.ativar_compra()
            self.btn_iniciar.setText('Editar')
        else:
            self.desativar_compra()
            self.btn_iniciar.setText('Iniciar')

    def ativar_compra(self):
        self.date_data.setEnabled(False)
        self.combo_loja.setEnabled(False)

        self.btn_adicionar.setEnabled(True)
        self.btn_remover.setEnabled(True)

        self.combo_ingrediente.setEnabled(True)
        self.carrega_combo_ingredientes()
        self.spin_quantidade.setEnabled(True)

        self.list_embalagens.setEnabled(True)
        self.tb_produtos.setEnabled(True)
    
    def desativar_compra(self):
        self.date_data.setEnabled(True)
        self.combo_loja.setEnabled(True)

        self.btn_adicionar.setEnabled(False)
        self.btn_remover.setEnabled(False)

        self.combo_ingrediente.setEnabled(False)
        self.combo_ingrediente.clear()
        self.spin_quantidade.setEnabled(False)

        self.list_embalagens.setEnabled(False)
        self.list_embalagens.clear()
        self.tb_produtos.setEnabled(False)

    def recomecar(self):
        self.date_data.clear()

        self.txt_produto.clear()
        self.spin_quantidade.clear()

        self.lista_compra = []
        self.tb_produtos.clear()
        
        self.desativar_compra()

        self.carrega_embalagens()
