import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita

#from PyQt5.QtCore import QDate

qt_tela_inicial = "tela_resumo_geral.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #BOTAO SAIR
        self.btn_sair.pressed.connect(self.fechar_tela)

        #CARREGA RECEITAS
        self.carrega_receitas()
        #CARREGA LOJAS
        self.carrega_lojas()
        #CARREGA LUGARES VENDA
        self.carrega_lugares_venda()

        #CARREGA RESULTADO RECEITA
        self.carrega_resultado_receita()

        #CARREGA RESULTADO GERAL
        self.carrega_resultado_geral()

        #CARREGA FABRICACOES
        self.carrega_fabricacoes()

        #CONFIGURA LARGURA COLUNAS INGREDIENTES DA RECEITA
        header = self.tb_resultado_receita.horizontalHeader() 
        self.tb_resultado_receita.setHorizontalHeaderLabels(['Receita', 'Vezes feita', 'Num. pacotes', 'Gastos', 'Ganhos', 'Lucro'])
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

        #CONFIGURA LARGURA COLUNAS INGREDIENTES DA RECEITA
        header = self.tb_fabricacoes.horizontalHeader() 
        self.tb_fabricacoes.setHorizontalHeaderLabels(['Data', 'Receita'])
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
    
    def carrega_resultado_geral(self):
        gasto_total = database_receita.select_gastos_totais()
        self.lbl_valor_investimento.setText('R${}'.format(gasto_total))

        self.lbl_valor_retorno.setText('R${}'.format(self.valor_retorno))

        lucro = self.valor_retorno - gasto_total
        self.lbl_valor_lucro.setText('R${}'.format(lucro))
    
    def carrega_receitas(self):
        self.list_receitas.clear()
        lista_receitas = database_receita.select_receitas_nomes()

        self.list_receitas.addItems(lista_receitas)
    
    def carrega_lojas(self):
        self.list_lojas.clear()
        lista_lojas = database_receita.select_lojas_nomes()

        self.list_lojas.addItems(lista_lojas)
    
    def carrega_lugares_venda(self):
        self.list_lugares_venda.clear()
        lista_locais = database_receita.select_locais_nomes()

        self.list_lugares_venda.addItems(lista_locais)
    
    def carrega_resultado_receita(self):
        self.tb_resultado_receita.clearContents()

        #RETORNO
        #[[nome receita, vezes feita, n pacotes, gastos, ganhos, lucro], ...]
        resultados_receitas = database_receita.select_resultados_rececitas()

        self.valor_retorno = 0
        for item in resultados_receitas:
            self.valor_retorno += float(item[4])
        
        #CARREGAR DADOS NA TABELA
        self.tb_resultado_receita.setRowCount(0)
        for linha in range(len(resultados_receitas)):
            self.tb_resultado_receita.insertRow(linha)
            for coluna in range(len(resultados_receitas[0])):
                self.tb_resultado_receita.setItem(linha,coluna, QtWidgets.QTableWidgetItem(str(resultados_receitas[linha][coluna])))
    
    def carrega_fabricacoes(self):
        fabricacoes_nao_vendidas = database_receita.select_fabricacoes_nao_vendidas_lista()

        #CARREGAR DADOS NA TABELA
        self.tb_fabricacoes.setRowCount(0)
        for linha in range(len(fabricacoes_nao_vendidas)):
            self.tb_fabricacoes.insertRow(linha)
            for coluna in range(len(fabricacoes_nao_vendidas[0])):
                self.tb_fabricacoes.setItem(linha,coluna, QtWidgets.QTableWidgetItem(str(fabricacoes_nao_vendidas[linha][coluna])))

    def fechar_tela(self):
        self.close()