import sys
from PyQt5 import QtCore, QtWidgets, uic

import tela_principal
import tela_cadastro_ingrediente

class Controller:

    def __init__(self):
        pass

    def abre_tela_principal(self):
        self.janela_tela_principal = tela_principal.MainWindow()
        self.janela_tela_principal.switch_tela_cadastro_ingrediente.connect(self.abre_tela_cadastro_ingrediente)
        self.janela_tela_principal.show()

    def abre_tela_cadastro_ingrediente(self):
        self.janela_tela_cadastro_ingrediente = tela_cadastro_ingrediente.MainWindow()
        self.janela_tela_cadastro_ingrediente.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.abre_tela_principal()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()