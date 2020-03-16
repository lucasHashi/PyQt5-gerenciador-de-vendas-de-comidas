import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita
import pyqt5_aux

qt_tela_inicial = "telas/tela_cadastro_receita.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        #INICIA RECEITA
        #LISTA COM LISTAS = [id_ingrediente, nome, quantidade, unidade]
        self.receita = []

        #CONFIG BOTOES
        self.btn_adicionar.pressed.connect(self.adicionar_ingrediente)
        self.btn_remover.pressed.connect(self.remover_ingrediente)
        self.btn_iniciar.pressed.connect(self.iniciar_receita)

        self.btn_recomecar.pressed.connect(self.recomecar)
        self.btn_voltar.pressed.connect(self.fechar_tela)
        self.btn_cad_sair.pressed.connect(self.cadastrar_voltar)
        self.btn_cad_limpar.pressed.connect(self.cadastrar_limpar)

        #CARREGAR INGREDIENTES
        self.carrega_ingredientes()

        #QUANDO UM ITEM FOR DOUBLE-CLICADO
        self.list_ingredientes.itemDoubleClicked.connect(self.ingrediente_selecionado)

        #CONFIGURA LARGURA COLUNAS INGREDIENTES DA RECEITA
        header = self.tb_ingredientes.horizontalHeader() 
        self.tb_ingredientes.setHorizontalHeaderLabels(['Codigo', 'Nome', 'Quantidade', 'Unidade'])
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
    
    def carrega_ingredientes(self):
        self.list_ingredientes.clear()
        lista_ingredientes = database_receita.select_ingredientes_nomes()

        #LISTA TODOS OS CODIGOS DE INGREDIENTES JA ADICIONADOS A RECEITA
        codigos_ingredientes = []
        for item in self.receita:
            cod = item[0]
            codigos_ingredientes.append(cod)

        #VERIFICAR SE JA NAO ESTA ADICIONADO A RECEITA
        ingredientes_nao_usados = []
        for item in lista_ingredientes:
            cod_ingred = item.split(' - ')[0]
            if(not cod_ingred in codigos_ingredientes):
                ingredientes_nao_usados.append(item)
        
        self.list_ingredientes.addItems(ingredientes_nao_usados)

    def carrega_ingredientes_receita(self):
        if(self.receita):
            pyqt5_aux.carregar_dados_table_widget(self.tb_ingredientes, self.receita)
        else:
            self.tb_ingredientes.clearContents()

    def adicionar_ingrediente(self):
        if(str(self.txt_ingrediente.text()) and str(self.txt_quantidade.text())):
            #ADICIONAR INGREDIENTE NA TABELA
            codigo, ingrediente = str(self.txt_ingrediente.text()).split(' - ')
            quantidade = self.txt_quantidade.text()
            unidade = self.txt_unidade_ingred.text()

            self.receita.append([codigo, ingrediente, quantidade, unidade])
            self.carrega_ingredientes_receita()
            self.carrega_ingredientes()

            self.txt_quantidade.setEnabled(False)

            self.txt_ingrediente.clear()
            self.txt_quantidade.clear()
            self.txt_unidade_ingred.clear()
        else:
            pass
    
    def ingrediente_selecionado(self, item):
        cod, nome, unidade = str(item.text()).split(' - ')

        self.txt_quantidade.setEnabled(True)

        self.txt_ingrediente.setText(cod+' - '+nome)
        self.txt_unidade_ingred.setText(unidade)
    
    def remover_ingrediente(self):
        #CASO TENHA UMA LINHA SELECIONADA
        try:
            #PEGAR O CODIGO DO ITEM SELECIONADO
            item = self.tb_ingredientes.currentItem()
            linha_selec = item.row()
            cod_selecionado = self.tb_ingredientes.item(linha_selec, 0).text()

            #REMOVER DA LISTA receita PELO CODIGO DO INGREDIENTE
            for i in range(len(self.receita)):
                item = self.receita[i]
                cod = item[0]
                if(cod == cod_selecionado):
                    self.receita.pop(i)
                    break
            
            self.carrega_ingredientes_receita()
            self.carrega_ingredientes()

            self.txt_quantidade.setEnabled(False)

            self.txt_ingrediente.clear()
            self.txt_quantidade.clear()
            self.txt_unidade_ingred.clear()
        except:
            pass

    def cadastrar_voltar(self):
        self.cadastrar()
        self.fechar_tela()

    def cadastrar_limpar(self):
        self.cadastrar()
        self.recomecar()

    def cadastrar(self):
        if(self.receita):
            nome_receita = self.txt_nome.text()
            validade = self.spin_validade.value()
            rendimento = self.txt_rendimento.text()
            unidade_receita = self.txt_unidade_receita.text()

            #ADICIONAR RECEITA
            cod_receita = database_receita.insere_receita(nome_receita, validade, rendimento, unidade_receita)
            #PEGAR O CODIGO DA ULTIMA RECEITA ADICIONADA
            #cod_receita = database_receita.cod_ultimo_insert()

            #PARA CADA INGRED EM receita
            for cod_ingred, nome_ingred, quantidade, unidade_ingred in self.receita:
                #ADICIONAR INGRED NA TABELA DE LIGACAO COM O cod_receita
                database_receita.insere_ingred_receita(cod_receita, cod_ingred, quantidade)

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
        self.txt_unidade_receita.setEnabled(False)
        self.spin_validade.setEnabled(False)

        self.btn_adicionar.setEnabled(True)
        self.btn_remover.setEnabled(True)

        #self.txt_ingrediente.setEnabled(True)
        #self.txt_quantidade.setEnabled(True)
        #self.txt_unidade_ingred.setEnabled(True)

        self.list_ingredientes.setEnabled(True)
        self.tb_ingredientes.setEnabled(True)
    
    def desativar_receita(self):
        self.txt_nome.setEnabled(True)
        self.txt_rendimento.setEnabled(True)
        self.txt_unidade_receita.setEnabled(True)
        self.spin_validade.setEnabled(True)

        self.btn_adicionar.setEnabled(False)
        self.btn_remover.setEnabled(False)

        #self.txt_ingrediente.setEnabled(False)
        #self.txt_quantidade.setEnabled(False)
        #self.txt_unidade_ingred.setEnabled(False)

        self.list_ingredientes.setEnabled(False)
        self.tb_ingredientes.setEnabled(False)

    def recomecar(self):
        self.txt_nome.clear()
        self.txt_rendimento.clear()
        self.txt_unidade_receita.clear()

        self.txt_ingrediente.clear()
        self.txt_quantidade.clear()
        self.txt_unidade_ingred.clear()

        self.receita = []
        self.tb_ingredientes.clearContents()
        
        self.desativar_receita()

        self.carrega_ingredientes()
