import sys
from PyQt5 import QtCore, QtWidgets, uic

import tela_principal
import tela_cadastro_ingrediente
import tela_gerenciar_ingrediente
import tela_editar_ingrediente
import tela_cadastro_receita

class Controller:

    def __init__(self):
        pass

    def abre_tela_principal(self):
        self.janela_tela_principal = tela_principal.MainWindow()
        self.janela_tela_principal.switch_tela_cadastro_ingrediente.connect(self.abre_tela_cadastro_ingrediente)
        self.janela_tela_principal.switch_tela_cadastro_receita.connect(self.abre_tela_cadastro_receita)
        self.janela_tela_principal.switch_tela_gerenciar_ingrediente.connect(self.abre_tela_gerenciar_ingrediente)
        self.janela_tela_principal.show()

    def abre_tela_cadastro_ingrediente(self):
        self.janela_tela_cadastro_ingrediente = tela_cadastro_ingrediente.MainWindow()
        self.janela_tela_cadastro_ingrediente.show()

    def abre_tela_gerenciar_ingrediente(self):
        self.janela_tela_gerenciar_ingrediente = tela_gerenciar_ingrediente.MainWindow()
        self.janela_tela_gerenciar_ingrediente.switch_tela_editar_ingrediente.connect(self.abre_tela_editar_ingrediente)
        self.janela_tela_gerenciar_ingrediente.show()
        try:
            self.janela_tela_editar_ingrediente.close()
        except:
            pass
    
    def abre_tela_editar_ingrediente(self,codigo,nome,tamanho,unidade,marca):
        self.janela_tela_editar_ingrediente = tela_editar_ingrediente.MainWindow(codigo,nome,tamanho,unidade,marca)
        self.janela_tela_gerenciar_ingrediente.close()
        self.janela_tela_editar_ingrediente.switch_tela_gerenciar_ingrediente.connect(self.abre_tela_gerenciar_ingrediente)
        self.janela_tela_editar_ingrediente.show()

    
    def abre_tela_cadastro_receita(self):
        self.janela_tela_cadastro_receita = tela_cadastro_receita.MainWindow()
        self.janela_tela_cadastro_receita.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.abre_tela_principal()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()