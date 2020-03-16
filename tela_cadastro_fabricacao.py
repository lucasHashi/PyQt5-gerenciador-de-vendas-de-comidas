import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import database_receita
import pyqt5_aux

#from PyQt5.QtCore import QDate

qt_tela_inicial = "telas/tela_cadastro_fabricacao.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #INICIAR CLIQUES DO BOTOES
        self.btn_iniciar.pressed.connect(self.iniciar_fabricacao)

        self.btn_cancelar.pressed.connect(self.cancelar_ingrediente)

        self.btn_cad_limpar.pressed.connect(self.cadastrar_limpar)
        self.btn_cad_sair.pressed.connect(self.cadastrar_sair)
        self.btn_recomecar.pressed.connect(self.recomecar)
        self.btn_voltar.pressed.connect(self.sair)

        #INICIA ITENS_DA_RECEITA
        #[[id_ingrediente, nome, quantidade, unidade, tam_embalagem, custo_embala, gasto]]
        self.itens_na_receita = []

        #CARREGA RECEITAS
        self.carrega_receitas()

        #QUANDO RECEITA FOR SELECIONADA
        self.combo_receita.currentIndexChanged.connect(self.receita_selecionada)

        #QUANDO INGREDIENTE DA RECEITA FOR DOUBLE-CLICADO
        self.tb_ingredientes.cellDoubleClicked.connect(self.alterar_embalagem_ingrediente)

        #QUANDO UMA EMBALAGEM DIFERENTE FOR DOUBLE-CLICADA
        self.tb_embalagens.cellDoubleClicked.connect(self.embalagem_ingrediente_selecionada)

        #CONFIGURA LARGURA COLUNAS INGREDIENTES DA RECEITA
        header = self.tb_ingredientes.horizontalHeader() 
        self.tb_ingredientes.setHorizontalHeaderLabels(['Codigo', 'Nome', 'Quantidade', 'Unidade', 'Tamanho', 'Preço', 'Gasto'])
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)

        #CONFIGURA LARGURA COLUNAS EMBALAGENS
        header = self.tb_embalagens.horizontalHeader() 
        self.tb_embalagens.setHorizontalHeaderLabels(['Codigo', 'Tamanho', 'Unidade', 'Marca', 'Loja', 'Preço'])
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

        #COLOCA DIA DE HOJE PRO CAMPO DATA
        self.date_data.setDate(QtCore.QDate.currentDate())

    def receita_selecionada(self):
        try:
            _, _, rendimento, unidade = self.combo_receita.currentText().split(' - ')
            self.txt_rendimento.setPlaceholderText(str(rendimento))
            self.txt_unidade_rendimento.setText(unidade)

            self.date_data.setEnabled(True)
            self.txt_rendimento.setEnabled(True)
            self.spin_tempo.setEnabled(True)
            self.btn_iniciar.setEnabled(True)
            self.btn_iniciar.setText('Iniciar')
        except:
            self.txt_rendimento.clear()
            self.txt_unidade_rendimento.clear()

            self.date_data.setEnabled(False)
            self.txt_rendimento.setEnabled(False)
            self.spin_tempo.setEnabled(False)
            self.btn_iniciar.setEnabled(False)

    def iniciar_fabricacao(self):
        if(self.txt_rendimento.isEnabled()):
            self.combo_receita.setEnabled(False)
            self.date_data.setEnabled(False)
            self.txt_rendimento.setEnabled(False)
            self.spin_tempo.setEnabled(False)
            self.btn_iniciar.setText('Editar')

            self.tb_ingredientes.setEnabled(True)
            
            self.inicia_itens_na_receita()
            self.carrega_ingredientes_da_receita()

            #self.atualiza_custo_final()

            self.btn_cad_limpar.setEnabled(True)
            self.btn_cad_sair.setEnabled(True)
            self.btn_recomecar.setEnabled(True)

        else:
            self.combo_receita.setEnabled(True)
            self.date_data.setEnabled(True)
            self.txt_rendimento.setEnabled(True)
            self.spin_tempo.setEnabled(True)
            self.btn_iniciar.setText('Iniciar')

            self.tb_ingredientes.setEnabled(False)

            self.tb_embalagens.setEnabled(False)
            self.btn_cancelar.setEnabled(False)

            self.btn_cad_limpar.setEnabled(False)
            self.btn_cad_sair.setEnabled(False)
            self.btn_recomecar.setEnabled(False)
    
    def carrega_receitas(self):
        self.combo_receita.clear()
        lista_receitas = ['Receitas cadastrados']
        lista_receitas += database_receita.select_receitas_nomes()
        self.combo_receita.addItems(lista_receitas)
    
    def inicia_itens_na_receita(self):
        id_receita = self.combo_receita.currentText().split(' - ')[0]

        #PEGA LISTA DE INGREDIENTES NA RECEITA
        #[[id_ingred, nome, quantidade, unidade]]
        itens_na_receita = database_receita.select_ingredientes_de_receita(id_receita)

        for linha in range(len(itens_na_receita)):
            self.itens_na_receita.append([itens_na_receita[linha][0], itens_na_receita[linha][1], 
                                            itens_na_receita[linha][2], itens_na_receita[linha][3],  
                                            0, 'Selecionar embalagem', 0])
    
    def carrega_ingredientes_da_receita(self):
        self.tb_ingredientes.clearContents()
        pyqt5_aux.carregar_dados_table_widget(self.tb_ingredientes, self.itens_na_receita)
        
        self.atualiza_custo_total()

    def alterar_embalagem_ingrediente(self, linha, coluna):
        self.tb_ingredientes.setEnabled(False)
        self.tb_embalagens.setEnabled(True)
        self.btn_cancelar.setEnabled(True)

        id_ingrediente = self.tb_ingredientes.item(linha, 0).text()
        nome_ingrediente = self.tb_ingredientes.item(linha, 1).text()
        quantidade = self.tb_ingredientes.item(linha, 2).text()
        unidade = self.tb_ingredientes.item(linha, 3).text()

        self.txt_ingrediente.setText(id_ingrediente + ' - ' + nome_ingrediente + ' - ' + quantidade + ' - ' + unidade)

        self.carrega_embalagens()
    
    def carrega_embalagens(self):
        id_ingrediente = self.txt_ingrediente.text().split(' - ')[0]

        lista_embalagens_ingrediente = database_receita.select_loja_embala_por_ingrediente_lista(id_ingrediente)
        
        self.tb_embalagens.clearContents()

        pyqt5_aux.carregar_dados_table_widget(self.tb_embalagens, lista_embalagens_ingrediente)

    def embalagem_ingrediente_selecionada(self, linha, coluna):
        #ADICIONAR A LISTA DE ITENS DA RECEITA [... TAMANHO, CUSTO, GASTO]
        tamanho = self.tb_embalagens.item(linha, 1).text()
        preco = self.tb_embalagens.item(linha, 5).text()

        quantidade = self.txt_ingrediente.text().split(' - ')[2]
        gasto = float(preco)*float(quantidade)/float(tamanho)

        id_ingrediente = self.txt_ingrediente.text().split(' - ')[0]
        for i in range(len(self.itens_na_receita)):
            item = self.itens_na_receita[i]
            if(str(item[0]) == str(id_ingrediente)):
                self.itens_na_receita[i][4] = tamanho
                self.itens_na_receita[i][5] = preco
                self.itens_na_receita[i][6] = gasto
        
        self.carrega_ingredientes_da_receita()

        self.tb_ingredientes.setEnabled(True)

        self.txt_ingrediente.clear()
        self.tb_embalagens.setEnabled(False)
        self.tb_embalagens.clearContents()
        self.btn_cancelar.setEnabled(False)

    def cancelar_ingrediente(self):
        self.txt_ingrediente.clear()

        self.tb_embalagens.clearContents()
        self.tb_embalagens.setEnabled(False)

        self.btn_cancelar.setEnabled(False)

        self.tb_ingredientes.setEnabled(True)
    
    def atualiza_custo_total(self):
        gasto_total = 0
        for item in self.itens_na_receita:
            gasto_total += float(item[6])
        
        self.txt_custo_final.setText(str(gasto_total))

    def cadastrar_limpar(self):
        self.cadastrar()
        self.recomecar()
    
    def cadastrar_sair(self):
        self.cadastrar()
        self.sair()

    def cadastrar(self):
        #TESTAR SE TODOS OS INGREDIENTES FORAM SELECIONADOS
        todos_selecionados = 1
        for item in self.itens_na_receita:
            if(item[6] == 0):
                todos_selecionados = 0
                break
        if(todos_selecionados):
            #PEGAR DADOS PARA INSERIR
            id_receita = self.combo_receita.currentText().split(' - ')[0]
            
            data_dia = str(self.date_data.date().day())
            data_mes = str(self.date_data.date().month())
            data_ano = str(self.date_data.date().year())
            data = '{}-{}-{}'.format(data_ano, data_mes, data_dia)

            rendimento = self.txt_rendimento.text()
            tempo_minutos = self.spin_tempo.value()

            custo_total = float(self.txt_custo_final.text())

            #INSERE DADOS TABELA FABRICACOES
            database_receita.insere_fabricacao(data, custo_total, rendimento, tempo_minutos, id_receita)

            self.recomecar()
    
    def recomecar(self):
        self.itens_na_receita = []

        self.combo_receita.setEnabled(True)
        self.carrega_receitas()

        self.tb_ingredientes.clearContents()
        self.tb_embalagens.clearContents()

        self.txt_rendimento.clear()
        self.txt_unidade_rendimento.clear()

        self.date_data.setEnabled(False)
        self.txt_rendimento.setEnabled(False)
        self.spin_tempo.setEnabled(False)
        self.btn_iniciar.setEnabled(False)
        self.btn_iniciar.setText('Iniciar')

        self.tb_ingredientes.setEnabled(False)

        self.tb_embalagens.setEnabled(False)
        self.btn_cancelar.setEnabled(False)

        self.btn_cad_limpar.setEnabled(False)
        self.btn_cad_sair.setEnabled(False)
        self.btn_recomecar.setEnabled(False)

    def sair(self):
        self.close()





