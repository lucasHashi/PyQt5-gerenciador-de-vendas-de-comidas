import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita

#from PyQt5.QtCore import QDate

qt_tela_inicial = "telas/tela_cadastro_venda.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        #CARREGAR COMBO LOCAIS
        self.carrega_locais()

        #CLIQUE BOTAO ATIVAR LOCAL
        self.btn_ativa_local.pressed.connect(self.ativa_local)

        #CARREGAR COMBO RECEITAS
        self.carrega_receitas()

        #QUANDO UMA RECEITA FOR SELECIONADA
        self.combo_receita.currentIndexChanged.connect(self.receita_selecionada)

        #QUANDO UMA FABRICACAO FOR SELECIONADA
        self.combo_fabricacao.currentIndexChanged.connect(self.fabricacao_selecionada)

        #QUANDO ALTERAR TAMANHO DO PACOTE
        self.txt_tam_pacote.editingFinished.connect(self.tamanho_pacote_alterado)

        #QUANDO ALTERAR O PRECO DO PACOTE
        self.double_preco_pacote.valueChanged.connect(self.preco_pacote_alterado)

        #CLIQUE DAS BOTOES DE BAIXO
        self.btn_recomecar.pressed.connect(self.recomecar)
        self.btn_voltar.pressed.connect(self.fechar_tela)
        self.btn_cad_sair.pressed.connect(self.cadastrar_voltar)
        self.btn_cad_limpar.pressed.connect(self.cadastrar_limpar)

        #COLOCA DIA DE HOJE PRO CAMPO DATA
        self.date_data.setDate(QtCore.QDate.currentDate())

    def carrega_locais(self):
        self.combo_local.clear()
        lista_locais = ['Locais cadastrados']
        lista_locais += database_receita.select_locais_nomes()
        self.combo_local.addItems(lista_locais)

    def carrega_receitas(self):
        self.combo_receita.clear()
        lista_receitas = database_receita.select_receitas_lista()
        nomes_receitas = ['Receitas cadastradas']

        for cod, nome, _, _, _ in lista_receitas:
            nomes_receitas.append('{} - {}'.format(cod, nome))
        
        self.combo_receita.addItems(nomes_receitas)

    def receita_selecionada(self):
        #ATIVA O COMBO FABRICACOES
        self.combo_fabricacao.setEnabled(True)

        #CARREGA COMBO FABRICACOES COM A RECEITA ESCOLHIDA
        self.carrega_fabricacoes()

    def carrega_fabricacoes(self):
        self.combo_fabricacao.clear()
        lista_fabricacoes = ['Fabricações']

        id_receita = self.combo_receita.currentText().split(' - ')[0]
        lista_fabricacoes += database_receita.select_fabricacoes_nao_vendidas_nomes(id_receita)

        self.combo_fabricacao.addItems(lista_fabricacoes)

    def fabricacao_selecionada(self, index):
        if(index > 0):
            #ATIVA SEGUNDA ETAPA
            #ATIVA TAMANHO PACOTE
            self.txt_tam_pacote.setEnabled(True)

            #PUXA OS DADOS SOBRE A FABRICACAO
            id_fabricacao = self.combo_fabricacao.itemText(index).split(' - ')[0]
            
            try:
                #CUSTO TOTAL, RENDIMENTO, UNIDADE RECEITA, TEMPO GASTO
                custo, tempo, rendimento, unidade = database_receita.select_dados_fabricacao(id_fabricacao)

                #ADICIONA OS CAMPOS DESATIVADOS
                self.double_custo_total.setValue(float(custo))
                self.txt_rendimento.setText(str(rendimento))
                self.txt_rendimento_unidade.setText(unidade)
                self.txt_tempo_gasto.setText(str(tempo))

                self.txt_tam_pacote_unidade.setText(unidade)
                self.txt_resto_unidade.setText(unidade)

                self.txt_tam_pacote.setFocus()
            except ValueError:
                self.combo_fabricacao.clear()
                self.combo_fabricacao.addItems(['Fabricações'])
        else:
            self.txt_tam_pacote.setEnabled(False)

            self.double_custo_total.clear()
            self.txt_rendimento.clear()
            self.txt_rendimento_unidade.clear()
            self.txt_tempo_gasto.clear()

            self.txt_tam_pacote_unidade.clear()
            self.txt_resto_unidade.clear()
    
    def tamanho_pacote_alterado(self):
        try:
            tamanho = float(self.txt_tam_pacote.text())
            rendimento = float(self.txt_rendimento.text())

            n_pacotes = rendimento//tamanho
            resto = rendimento%tamanho

            self.txt_quant_pacotes.setText(str(n_pacotes))
            self.txt_resto_pacotes.setText(str(resto))

            custo_total = float(self.double_custo_total.value())
            custo_por_pacote = custo_total/n_pacotes
            self.double_custo_pacote.setValue(custo_por_pacote)

            self.double_preco_lucro1.setValue(float(custo_por_pacote*2))
            self.double_preco_lucro2.setValue(float(custo_por_pacote*3))
            self.double_preco_lucro3.setValue(float(custo_por_pacote*4))

            self.double_preco_pacote.setEnabled(True)
        except Exception:
            self.txt_quant_pacotes.setText(str(0))
            self.txt_resto_pacotes.setText(str(0))

            self.double_custo_pacote.setValue(0)

            self.double_preco_lucro1.setValue(0)
            self.double_preco_lucro2.setValue(0)
            self.double_preco_lucro3.setValue(0)

            self.double_preco_pacote.setEnabled(False)

    def preco_pacote_alterado(self, preco_pacote):
        if(preco_pacote > 0):
            retorno = preco_pacote * float(self.txt_quant_pacotes.text())
            lucro = retorno - self.double_custo_total.value()
            lucro_por_pacote = preco_pacote - self.double_custo_pacote.value()

            self.double_retorno.setValue(retorno)
            self.double_lucro.setValue(lucro)
            self.double_lucro_pacote.setValue(lucro_por_pacote)
        else:
            self.double_retorno.setValue(0)
            self.double_lucro.setValue(0)
            self.double_lucro_pacote.setValue(0)
    
    def ativa_local(self):
        if(self.txt_local.isEnabled()):
            self.txt_local.setEnabled(False)
            self.btn_ativa_local.setText('+')
            self.combo_local.setEnabled(True)
        else:
            self.txt_local.setEnabled(True)
            self.btn_ativa_local.setText('-')
            self.combo_local.setEnabled(False)
    
    def cadastrar_voltar(self):
        self.cadastrar()
        self.fechar_tela()

    def cadastrar_limpar(self):
        self.cadastrar()
        self.recomecar()
    
    def cadastrar(self):
        #PAGA OS DADOS
        #ID_FABRICACAO, DATA, LOCAL, RETORNO, QUANT_PACOTES, TAMANHO PACOTE, PRECO PACOTE
        id_fabricacao = self.combo_fabricacao.currentText().split(' - ')[0]
        
        data_dia = str(self.date_data.date().day())
        data_mes = str(self.date_data.date().month())
        data_ano = str(self.date_data.date().year())
        data = '{}-{}-{}'.format(data_ano, data_mes, data_dia)

        local = ''
        if(self.txt_local.isEnabled()):
            local = self.txt_local.text()
        else:
            local = self.combo_local.currentText()
        
        retorno = self.double_retorno.value()
        n_pacotes = int(float(self.txt_quant_pacotes.text()))
        tam_pacotes = float(self.txt_tam_pacote.text())
        preco_pacote = self.double_preco_pacote.value()

        database_receita.insere_venda(data, local, retorno, tam_pacotes, preco_pacote, n_pacotes, id_fabricacao)

    def recomecar(self):
        self.txt_local.clear()
        self.txt_local.setEnabled(False)
        self.btn_ativa_local.setText('+')
        self.combo_local.setEnabled(True)
        self.carrega_locais()

        self.carrega_receitas()
        self.combo_fabricacao.clear()
        self.combo_fabricacao.addItems(['Fabricações'])
        self.combo_fabricacao.setEnabled(False)
        self.double_custo_total.setValue(0)
        self.txt_rendimento.clear()
        self.txt_rendimento_unidade.clear()
        self.txt_tempo_gasto.clear()

        self.txt_tam_pacote.clear()
        self.txt_tam_pacote.setEnabled(False)
        self.txt_tam_pacote_unidade.clear()
        self.txt_quant_pacotes.clear()
        self.txt_resto_pacotes.clear()
        self.txt_resto_unidade.clear()
        self.double_custo_pacote.setValue(0)
        self.double_preco_lucro1.setValue(0)
        self.double_preco_lucro2.setValue(0)
        self.double_preco_lucro3.setValue(0)

        self.double_preco_pacote.setValue(0)
        self.double_preco_pacote.setEnabled(False)
        self.double_retorno.setValue(0)
        self.double_lucro.setValue(0)
        self.double_lucro_pacote.setValue(0)

    def fechar_tela(self):
        self.close()

