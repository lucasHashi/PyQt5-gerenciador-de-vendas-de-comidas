import sys
from PyQt5 import QtCore, QtWidgets, uic
import database_receita

qt_tela1 = "tela_gerenciar_ingrediente.ui"
Ui_MainWindow_tela1, QtBaseClass_tela1 = uic.loadUiType(qt_tela1)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow_tela1):

    switch_tela_editar_ingrediente = QtCore.pyqtSignal(str, str, float, str, str)

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow_tela1.__init__(self)
        self.setupUi(self)

        self.btn_editar.clicked.connect(self.ativar_edicao)
        self.btn_excluir.clicked.connect(self.excluir_item)
        self.btn_voltar.clicked.connect(self.fechar)

        self.btn_salvar.clicked.connect(self.editar)
        self.btn_cancelar.clicked.connect(self.cancelar_edicao)

        self.tb_dados.itemDoubleClicked.connect(self.ativar_edicao)

        self.carrega_tb_dados()

        header = self.tb_dados.horizontalHeader() 
        self.tb_dados.setHorizontalHeaderLabels(['Codigo', 'Nome'])
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

    def editar(self):
        cod = self.txt_codigo.text()
        nome_ingred = self.txt_nome.text()

        if(not database_receita.varifica_ingrediente_duplicado(nome_ingred)):
            database_receita.update_ingrediente(cod, nome_ingred)
        
        self.carrega_tb_dados()
        self.cancelar_edicao()

    def excluir_item(self):
        if(self.tb_dados.rowCount() > 0):
            item = self.tb_dados.currentItem()
            try:
                linha_selec = item.row()
                cod = self.tb_dados.item(linha_selec, 0).text()

                database_receita.delete_ingrediente(cod)
                
                self.carrega_tb_dados()
            except:
                pass

    def ativar_edicao(self, item):
        if(self.tb_dados.rowCount() > 0):
            try:
                linha_selec = item.row()
            except:
                item = self.tb_dados.currentItem()
                linha_selec = item.row()
            finally:
                cod = self.tb_dados.item(linha_selec, 0).text()
                nome = self.tb_dados.item(linha_selec, 1).text()

                self.txt_codigo.setText(str(cod))
                self.txt_nome.setText(nome)
                self.txt_nome.setPlaceholderText(nome)

                self.tb_dados.setEnabled(False)
                self.btn_editar.setEnabled(False)
                self.btn_excluir.setEnabled(False)
                self.btn_voltar.setEnabled(False)

                self.txt_nome.setEnabled(True)
                self.btn_salvar.setEnabled(True)
                self.btn_cancelar.setEnabled(True)
    
    def cancelar_edicao(self):
        self.txt_codigo.clear()
        self.txt_nome.clear()
        self.txt_nome.setPlaceholderText('')

        self.tb_dados.setEnabled(True)
        self.btn_editar.setEnabled(True)
        self.btn_excluir.setEnabled(True)
        self.btn_voltar.setEnabled(True)

        self.txt_nome.setEnabled(False)
        self.btn_salvar.setEnabled(False)
        self.btn_cancelar.setEnabled(False)
    
    def carrega_tb_dados(self):
        lista_dados = database_receita.select_ingredientes_lista()
        
        self.tb_dados.setRowCount(0)
        for linha in range(len(lista_dados)):
            self.tb_dados.insertRow(linha)
            for coluna in range(len(lista_dados[0])):
                self.tb_dados.setItem(linha,coluna, QtWidgets.QTableWidgetItem(str(lista_dados[linha][coluna])))
    
    def limpar(self):
        self.txt_nome.clear()
        self.txt_comida.clear()
    
    def fechar(self):
        self.close()