import sqlite3
import os

nome_database = 'db_receitas'

def criar_tabelas():
    os.remove(nome_database+'.db')
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        #CRIAR TABELAS
        #TABELA LOJAS
        cursor.execute('''
            CREATE TABLE lojas (
                id_loja INTEGER PRIMARY KEY,
                nome TEXT
            )''')
        
        #TABELA MARCAS
        cursor.execute('''
            CREATE TABLE marcas (
                id_marca INTEGER PRIMARY KEY,
                nome TEXT
            )''')

        #TABELA INGREDIENTES
        cursor.execute('''
            CREATE TABLE ingredientes (
                id_ingrediente INTEGER PRIMARY KEY,
                nome TEXT,
                unidade TEXT,
                tam_embalagem REAL,
                id_marca_ingredientes INTEGER,
                FOREIGN KEY (id_marca_ingredientes) REFERENCES marcas (id_marca)
            )''')
        
        #TABELA INGRED_LOJA
        cursor.execute('''
            CREATE TABLE ingred_loja (
                id_ingred_loja INTEGER PRIMARY KEY,
                preco REAL,
                data TEXT,
                ativo INTEGER,
                mais_recente INTEGER,
                id_ingrediente_ingred_loja INTEGER,
                id_loja_ingred_loja INTEGER,
                FOREIGN KEY (id_loja_ingred_loja) REFERENCES lojas (id_lojas),
                FOREIGN KEY (id_ingrediente_ingred_loja) REFERENCES ingredientes (id_ingrediente)
            )''')

        #TABELA RECEITAS
        cursor.execute('''
            CREATE TABLE receitas (
                id_receita INTEGER PRIMARY KEY,
                nome TEXT,
                rendimento REAL,
                unidade REAL,
                validade TEXT
            )''')

        #TABELA INGRED_RECEITA
        cursor.execute('''
            CREATE TABLE ingred_receita (
                id_ingred_receita INTEGER PRIMARY KEY,
                quantidade REAL,
                id_receita_ingred_receita INTEGER,
                id_ingrediente_ingred_receita INTEGER,
                FOREIGN KEY (id_receita_ingred_receita) REFERENCES receitas (id_receita),
                FOREIGN KEY (id_ingrediente_ingred_receita) REFERENCES ingredientes (id_ingrediente)
            )''')

        #TABELA FABRICACOES
        cursor.execute('''
            CREATE TABLE fabricacoes (
                id_fabricacao INTEGER PRIMARY KEY,
                data TEXT,
                rendimento REAL,
                tempo_minutos INTEGER,
                id_receita_fabricacoes INTEGER,
                FOREIGN KEY (id_receita_fabricacoes) REFERENCES receitas (id_receita)
            )''')

        #TABELA VENDAS
        cursor.execute('''
            CREATE TABLE vendas (
                id_venda INTEGER PRIMARY KEY,
                data TEXT,
                local TEXT,
                pacote_preco REAL,
                pacote_tam REAL,
                quant_pacotes INTEGER,
                id_fabricacao_vendas INTEGER,
                FOREIGN KEY (id_fabricacao_vendas) REFERENCES fabricacoes (id_fabricacao)
            )''')

criar_tabelas()