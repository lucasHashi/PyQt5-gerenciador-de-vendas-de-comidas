import sys
from PyQt5 import QtCore, QtWidgets, uic

import tela_principal
import tela_cadastro_ingrediente
import tela_gerenciar_ingrediente

import tela_cadastro_receita
import tela_gerenciar_receita


import tela_cadastro_embalagem
#import tela_gerenciar_embalagem

'''
import tela_cadastro_compra
import tela_gerenciar_compra

import tela_cadastro_fabricacao
import tela_gerenciar_fabricacao

import tela_cadastro_venda
import tela_gerenciar_venda

import tela_gerenciar_marca
import tela_gerenciar_loja
'''

class Controller:

    def __init__(self):
        pass

    def abre_tela_principal(self):
        self.janela_tela_principal = tela_principal.MainWindow()
        self.janela_tela_principal.switch_tela_cadastro_ingrediente.connect(self.abre_tela_cadastro_ingrediente)
        self.janela_tela_principal.switch_tela_cadastro_receita.connect(self.abre_tela_cadastro_receita)
        self.janela_tela_principal.switch_tela_cadastro_embalagens.connect(self.abre_tela_cadastro_embalagens)

        self.janela_tela_principal.switch_tela_gerenciar_ingrediente.connect(self.abre_tela_gerenciar_ingrediente)
        self.janela_tela_principal.switch_tela_gerenciar_receita.connect(self.abre_tela_gerenciar_receita)
        self.janela_tela_principal.show()

    def abre_tela_cadastro_ingrediente(self):
        self.janela_tela_cadastro_ingrediente = tela_cadastro_ingrediente.MainWindow()
        self.janela_tela_cadastro_ingrediente.show()

    def abre_tela_gerenciar_ingrediente(self):
        self.janela_tela_gerenciar_ingrediente = tela_gerenciar_ingrediente.MainWindow()
        self.janela_tela_gerenciar_ingrediente.show()
    
    def abre_tela_cadastro_receita(self):
        self.janela_tela_cadastro_receita = tela_cadastro_receita.MainWindow()
        self.janela_tela_cadastro_receita.show()
    
    def abre_tela_gerenciar_receita(self):
        self.janela_tela_gerenciar_receita = tela_gerenciar_receita.MainWindow()
        self.janela_tela_gerenciar_receita.show()
    
    def abre_tela_cadastro_embalagens(self):
        self.janela_tela_cadastro_embalagens = tela_cadastro_embalagem.MainWindow()
        self.janela_tela_cadastro_embalagens.show()
    
    def abre_tela_gerenciar_embalagens(self):
        self.janela_tela_gerenciar_embalagens = tela_gerenciar_embalagem.MainWindow()
        self.janela_tela_gerenciar_embalagens.show()
    
    def abre_tela_cadastro_compras(self):
        self.janela_tela_cadastro_compras = tela_cadastro_compra.MainWindow()
        self.janela_tela_cadastro_compras.show()
    
    def abre_tela_gerenciar_compras(self):
        self.janela_tela_gerenciar_compras = tela_gerenciar_compra.MainWindow()
        self.janela_tela_gerenciar_compras.show()
    
    def abre_tela_cadastro_fabricacoes(self):
        self.janela_tela_cadastro_fabricacoes = tela_cadastro_fabricacao.MainWindow()
        self.janela_tela_cadastro_fabricacoes.show()
    
    def abre_tela_gerenciar_fabricacoes(self):
        self.janela_tela_gerenciar_fabricacoes = tela_gerenciar_fabricacao.MainWindow()
        self.janela_tela_gerenciar_fabricacoes.show()
    
    def abre_tela_cadastro_vendas(self):
        self.janela_tela_cadastro_vendas = tela_cadastro_venda.MainWindow()
        self.janela_tela_cadastro_vendas.show()
    
    def abre_tela_gerenciar_vendas(self):
        self.janela_tela_gerenciar_vendas = tela_gerenciar_venda.MainWindow()
        self.janela_tela_gerenciar_vendas.show()
    
    def abre_tela_gerenciar_marcas(self):
        self.janela_tela_gerenciar_marcas = tela_gerenciar_marca.MainWindow()
        self.janela_tela_gerenciar_marcas.show()
    
    def abre_tela_gerenciar_lojas(self):
        self.janela_tela_gerenciar_lojas = tela_gerenciar_loja.MainWindow()
        self.janela_tela_gerenciar_lojas.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.abre_tela_principal()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()