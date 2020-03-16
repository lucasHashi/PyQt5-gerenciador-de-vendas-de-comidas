import sys
from PyQt5 import QtCore, QtWidgets, uic
import pyqt5_aux
def carregar_dados_table_widget(tabela, lista):
    tabela.setRowCount(0)
    for linha in range(len(lista)):
        tabela.insertRow(linha)
        for coluna in range(len(lista[0])):
            tabela.setItem(linha,coluna, QtWidgets.QTableWidgetItem(str(lista[linha][coluna])))