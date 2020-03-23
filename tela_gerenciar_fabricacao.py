import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita
from datetime import date, datetime

qt_tela_inicial = "telas/tela_gerenciar_fabricacao.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #CONFIG BOTOES
        self.btn_cancelar.pressed.connect(self.cancelar_edicao)
        self.btn_voltar.pressed.connect(self.fechar_tela)
        self.btn_editar.pressed.connect(self.editar)
        self.btn_excluir.pressed.connect(self.excluir_item)

        self.combo_status.currentIndexChanged.connect(self.carrega_fabricacoes)

        self.list_fabricacoes.itemDoubleClicked.connect(self.iniciar_edicao)
        

    def iniciar_edicao(self, item):
        item = item.text()
        id_fabricacao, data, _ = item.split(' - ')

        self.list_fabricacoes.setEnabled(False)

        data_fabricacao = datetime.strptime(data, '%Y/%m/%d')
        self.date_data.setDate(data_fabricacao)

        rendimento, unidade, tempo = database_receita.select_fabricacao_por_id(id_fabricacao)

        self.txt_rendimento.setPlaceholderText(rendimento)
        self.txt_rendimento.setText(rendimento)
        self.txt_rendimento.setEnabled(True)
        self.txt_unidade.setPlaceholderText(unidade)
        self.txt_unidade.setText(unidade)
        self.txt_unidade.setEnabled(True)

        self.spin_tempo.setValue(int(tempo))
        self.spin_tempo.setEnabled(True)

        self.btn_editar.setEnabled(True)
        self.btn_excluir.setEnabled(True)
        self.btn_cancelar.setEnabled(True)
    
    def cancelar_edicao(self):
        self.list_fabricacoes.setEnabled(True)

        data_hoje = str(date.today())
        data_hoje = QtCore.QDate.fromString(data_hoje, 'yyyy-MM-dd')
        self.date_data.setDate(data_hoje)

        self.txt_rendimento.clear()
        self.txt_rendimento.setPlaceholderText('')
        self.txt_rendimento.setEnabled(False)
        self.txt_unidade.clear()
        self.spin_tempo.setValue(0)
        self.spin_tempo.setEnabled(False)

        self.btn_editar.setEnabled(False)
        self.btn_excluir.setEnabled(False)
        self.btn_cancelar.setEnabled(False)


    def editar(self):
        id_ingrediente = str(self.combo_ingrediente.currentText()).split(' - ')[0]
        id_embalagem = str(self.list_embalagens.selectedItems()[0].text()).split(' - ')[0]

        tamanho = self.txt_tamanho.text()
        nome_marca = self.txt_marca.text()

        id_marca = database_receita.select_marca_por_nome(nome_marca)

        if(not database_receita.verifica_embalagem_duplicada(tamanho, id_ingrediente, id_marca)):
            database_receita.update_embalagem(id_embalagem, id_marca, tamanho)

        self.limpar()

    def combo_ingrediente_selecionado(self, item):
        try:
            codigo, _, unidade = str(self.combo_ingrediente.currentText()).split(' - ')
            self.txt_unidade.setText(unidade)
            self.carrega_embalagens(codigo)
        except:
            self.txt_unidade.clear()
    
    def carrega_embalagens(self, id_ingrediente):
        #COD - MARCA - TAMANHO - UNIDADE
        self.list_embalagens.clear()
        lista_embalagens = database_receita.select_embalagens_nomes_por_ingrediente(id_ingrediente)

        self.list_embalagens.addItems(lista_embalagens)

    def carrega_fabricacoes(self, indice):
        self.list_fabricacoes.clear()

        status = self.combo_status.itemText(indice).split(' - ')[0]
        if(status == 0):
            lista_fabricacoes = database_receita.select_fabricacoes_vendidas()
            lista_fabricacoes = database_receita.select_fabricacoes_por_lista_ids(lista_fabricacoes)
        elif(status == 1):
            lista_fabricacoes = database_receita.select_fabricacoes_ids()
            lista_fabricacoes = database_receita.select_fabricacoes_por_lista_ids(lista_fabricacoes)
        else:
            lista_fabricacoes_vendidas = database_receita.select_fabricacoes_vendidas()
            lista_fabricacoes_todas = database_receita.select_fabricacoes_ids()
            lista_fabricacoes_nao = []
            for fabri in lista_fabricacoes_vendidas:
                if(not fabri in lista_fabricacoes_todas):
                    lista_fabricacoes_nao.append(fabri)
            
            lista_fabricacoes = database_receita.select_fabricacoes_por_lista_ids(lista_fabricacoes_nao)
        
        print(lista_fabricacoes)
        self.list_fabricacoes.addItems(lista_fabricacoes)

    def fechar_tela(self):
        self.close()

    def limpar(self):
        self.list_embalagens.clear()

        self.cancelar_edicao()
    
    def excluir_item(self):
        try:
            item_selec = self.list_embalagens.selectedItems()[0].text()
            cod = item_selec.split(' - ')[0]

            database_receita.delete_embalagem(cod)
            
            self.carrega_tb_dados()
            self.cancelar_edicao()
            self.limpar()
        except:
            self.cancelar_edicao()
            self.limpar()

        

