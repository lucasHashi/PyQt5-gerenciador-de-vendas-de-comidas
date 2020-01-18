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

        self.btn_editar.clicked.connect(self.abrir_tela_editar)
        self.btn_excluir.clicked.connect(self.excluir_item)
        self.btn_cancelar.clicked.connect(self.fechar)

        self.tb_dados.itemDoubleClicked.connect(self.abrir_tela_editar)

        self.carrega_tb_dados()

        header = self.tb_dados.horizontalHeader() 
        self.tb_dados.setHorizontalHeaderLabels(['Codigo', 'Nome', 'Tamanho', 'Unidade', 'Marca'])     
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

    def excluir_item(self):
        item = self.tb_dados.currentItem()
        linha_selec = item.row()
        cod = self.tb_dados.item(linha_selec, 0).text()

        database_receita.delete_ingrediente(cod)
        
        self.carrega_tb_dados()

    def abrir_tela_editar(self, item):
        try:
            linha_selec = item.row()
        except:
            item = self.tb_dados.currentItem()
            linha_selec = item.row()
        finally:
            cod = self.tb_dados.item(linha_selec, 0).text()
            nome = self.tb_dados.item(linha_selec, 1).text()
            tamanho = float(self.tb_dados.item(linha_selec, 2).text())
            unidade = self.tb_dados.item(linha_selec, 3).text()
            marca = self.tb_dados.item(linha_selec, 4).text()

            self.switch_tela_editar_ingrediente.emit(cod,nome,tamanho,unidade,marca)
    
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