import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita

qt_tela_inicial = "tela_gerenciar_loja_embala.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    switch_tela_cadastro_loja_embala = QtCore.pyqtSignal()

    def __init__(self, id_loja_embala, id_embalagem, tamanho, unidade, marca, id_loja, nome_loja, preco, ingrediente):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #CONFIG BOTOES
        self.btn_limpar.pressed.connect(self.limpar)
        self.btn_voltar.pressed.connect(self.fechar_tela)
        self.btn_editar.pressed.connect(self.editar)

        #VALORES
        self.txt_id_loja_embala.setText(str(id_loja_embala))
        self.txt_ingrediente.setText(ingrediente)

        self.txt_id_embalagem.setText(str(id_embalagem))
        self.txt_tamanho.setText(str(tamanho))
        self.txt_unidade.setText(unidade)

        self.txt_id_loja.setText(str(id_loja))
        self.txt_nome_loja.setText(nome_loja)

        self.double_preco.setValue(float(preco))
        self.preco_antigo = float(preco)

    def editar(self):
        if(not self.double_preco.value() == self.preco_antigo):
            database_receita.update_loja_embala(int(self.txt_id_loja_embala.text()), self.double_preco.value())
        self.fechar_tela()

    def fechar_tela(self):
        self.switch_tela_cadastro_loja_embala.emit()

    def limpar(self):
        self.txt_nome.clear()
        self.txt_unidade.clear()
        self.carrega_combo_ingredientes()