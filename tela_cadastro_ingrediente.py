import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita

qt_tela_inicial = "tela_cadastro_ingrediente.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #CONFIG BOTOES
        self.btn_limpar.pressed.connect(self.limpar)
        self.btn_voltar.pressed.connect(self.fechar_tela)
        self.btn_cad_sair.pressed.connect(self.cadastrar_voltar)
        self.btn_cad_limpar.pressed.connect(self.cadastrar_limpar)
        self.btn_ativa_marca.pressed.connect(self.ativa_marca_nova)

        self.carrega_combo_marcas()
        self.carrega_combo_ingredientes()

        self.combo_nomes.currentIndexChanged.connect(self.combo_ingrediente_to_nome)
    
    def cadastrar_voltar(self):
        nome_ingred = self.txt_nome.text()
        unidade = self.txt_unidade.text()
        tamanho = self.txt_tam_embalagem.text()
        nome_marca = self.txt_marca.text()
        if(self.valida_campos_entradas(nome_ingred, tamanho, unidade, nome_marca)):
            self.cadastrar()
            self.fechar_tela()

    def cadastrar_limpar(self):
        nome_ingred = self.txt_nome.text()
        unidade = self.txt_unidade.text()
        tamanho = self.txt_tam_embalagem.text()

        if(self.txt_marca.text()):
            nome_marca = self.txt_marca.text()
        else:
            nome_marca = str(self.combo_marca.currentText())

        if(self.valida_campos_entradas(nome_ingred, tamanho, unidade, nome_marca)):
            self.cadastrar()
            self.limpar()

    def valida_campos_entradas(self, nome, tamanho, unidade, nome_marca):
        nome = True if(nome.replace(' ','')) else False
        unidade = True if(unidade.replace(' ','')) else False
        nome_marca = True if(nome_marca.replace(' ','')) else False
        try:
            tamanho = float(str(self.txt_tam_embalagem.text()).replace(',','.'))
        except:
            tamanho = False
        tamanho = True if(tamanho) else False

        return nome*tamanho*unidade*nome_marca

    def cadastrar(self):
        nome_ingred = self.txt_nome.text()
        unidade = self.txt_unidade.text()
        nome_marca = self.txt_marca.text()
        tamanho = float(str(self.txt_tam_embalagem.text()).replace(',','.'))
        id_marca = 0

        if(nome_marca.replace(' ','')):
            if(not database_receita.varifica_marca_duplicada(nome_marca)):
                #ADICIONA ESSA NOVA MARCA
                database_receita.insere_marca(nome_marca)
                #SELECIONA O id_marca DA MARCA COM nome = 'nome_marca'
            id_marca = int(database_receita.select_marca_por_nome(nome_marca))
            self.carrega_combo_marcas()
            self.carrega_combo_ingredientes()
            self.txt_marca.setEnabled(False)
            self.btn_ativa_marca.setText('+')
            self.txt_marca.clear()
        else:
            id_marca = int(str(self.combo_marca.currentText()).split(' - ')[0])

        if(not database_receita.varifica_ingrediente_duplicado(nome_ingred, unidade,tamanho,id_marca)):
            database_receita.insere_ingrediente(nome_ingred, unidade, tamanho, id_marca)

    def combo_ingrediente_to_nome(self, item):
        try:
            self.txt_nome.setText(str(self.combo_nomes.currentText()).split(' - ')[0])
            self.txt_tam_embalagem.setText(str(self.combo_nomes.currentText()).split(' - ')[1])
            self.txt_unidade.setText(str(self.combo_nomes.currentText()).split(' - ')[2])
        except:
            self.txt_nome.clear()
            self.txt_tam_embalagem.clear()
            self.txt_unidade.clear()


    def carrega_combo_marcas(self):
        self.combo_marca.clear()
        marcas = database_receita.select_marcas_nomes()
        self.combo_marca.addItems(marcas)
    
    def carrega_combo_ingredientes(self):
        self.combo_nomes.clear()
        nomes_ingredientes = ['Ingredientes ja cadastrados']
        nomes_ingredientes += database_receita.select_ingredientes_nomes()
        self.combo_nomes.addItems(nomes_ingredientes)

    def ativa_marca_nova(self):
        if(self.txt_marca.isEnabled()):
            self.txt_marca.setEnabled(False)
            self.btn_ativa_marca.setText('+')
            self.txt_marca.clear()
        else:
            self.txt_marca.setEnabled(True)
            self.btn_ativa_marca.setText('-')

    def fechar_tela(self):
        self.close()

    def limpar(self):
        self.txt_nome.clear()
        self.txt_tam_embalagem.clear()
        self.txt_unidade.clear()
        self.txt_marca.clear()
        self.txt_marca.setEnabled(False)
        self.carrega_combo_ingredientes()

'''
def main():
    app = QtWidgets.QApplication(sys.argv)
    janela_tela_principal = MainWindow()
    janela_tela_principal.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
'''