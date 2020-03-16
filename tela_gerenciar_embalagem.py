import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita

qt_tela_inicial = "telas/tela_gerenciar_embalagem.ui"
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

        self.carrega_combo_ingredientes()

        self.combo_ingrediente.currentIndexChanged.connect(self.combo_ingrediente_selecionado)

        self.list_embalagens.itemDoubleClicked.connect(self.iniciar_edicao)

    def iniciar_edicao(self, item):
        item = item.text()
        _, marca, tamanho, unidade = item.split(' - ')

        self.combo_ingrediente.setEnabled(False)
        self.list_embalagens.setEnabled(False)

        self.txt_marca.setEnabled(True)
        self.txt_marca.setPlaceholderText(str(marca))
        self.txt_marca.setText(str(marca))

        self.txt_tamanho.setPlaceholderText(str(tamanho))
        self.txt_tamanho.setText(str(tamanho))
        self.txt_tamanho.setEnabled(True)

        self.txt_unidade.setText(str(unidade))

        self.btn_cancelar.setEnabled(True)
    
    def cancelar_edicao(self):
        self.combo_ingrediente.setEnabled(True)
        self.list_embalagens.setEnabled(True)

        self.txt_marca.setEnabled(False)
        self.txt_marca.setPlaceholderText('')
        self.txt_marca.setText('')

        self.txt_tamanho.setPlaceholderText('')
        self.txt_tamanho.setText('')
        self.txt_tamanho.setEnabled(False)

        self.txt_unidade.setText('')

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

    def carrega_combo_ingredientes(self):
        self.combo_ingrediente.clear()
        
        nomes_ingredientes = ['Ingredientes ja cadastrados']
        nomes_ingredientes += database_receita.select_ingredientes_nomes()
        
        self.combo_ingrediente.addItems(nomes_ingredientes)

    def fechar_tela(self):
        self.close()

    def limpar(self):
        self.carrega_combo_ingredientes()
        self.list_embalagens.clear()

        self.cancelar_edicao()
    
    def excluir_item(self):
        try:
            item_selec = self.list_embalagens.selectedItems()[0]
            cod = item_selec.text().split(' - ')[0]

            database_receita.delete_embalagem(cod)
            
            self.carrega_tb_dados()
        except:
            pass

        

