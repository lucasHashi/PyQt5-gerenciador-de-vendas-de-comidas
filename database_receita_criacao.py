import sqlite3
import os

nome_database = 'db_receitas'

def criar_tabelas():
    os.remove(nome_database+'.db')
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        #CRIAR TABELAS
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
                unidade TEXT
            )''')

        #TABELA EMBALAGENS
        cursor.execute('''
            CREATE TABLE embalagens (
                id_embalagem INTEGER PRIMARY KEY,
                tamanho REAL,
                id_ingrediente_embalagens INTEGER,
                id_marca_embalagens INTEGER,
                FOREIGN KEY (id_ingrediente_embalagens) REFERENCES ingredientes (id_ingrediente),
                FOREIGN KEY (id_marca_embalagens) REFERENCES marcas (id_marca)
            )''')

        #TABELA LOJAS
        cursor.execute('''
            CREATE TABLE lojas (
                id_loja INTEGER PRIMARY KEY,
                nome TEXT
            )''')
        
        #TABELA LOJA_EMBALA
        cursor.execute('''
            CREATE TABLE loja_embala (
                id_loja_embala INTEGER PRIMARY KEY,
                preco REAL,
                id_loja_loja_embala INTEGER,
                id_embalagem_loja_embala INTEGER,
                FOREIGN KEY (id_loja_loja_embala) REFERENCES lojas (id_lojas),
                FOREIGN KEY (id_embalagem_loja_embala) REFERENCES emabalagens (id_embalagem)
            )''')

        #TABELA COMPRAS
        cursor.execute('''
            CREATE TABLE compras (
                id_compra INTEGER PRIMARY KEY,
                data TEXT
            )''')
        
        #TABELA COMP_LOJA_EMBALA
        cursor.execute('''
            CREATE TABLE comp_loja_embala (
                id_comp_loja_embala INTEGER PRIMARY KEY,
                preco REAL,
                quantidade REAL,
                id_compra_comp_loja_embala INTEGER,
                id_loja_embala_comp_loja_embala INTEGER,
                FOREIGN KEY (id_compra_comp_loja_embala) REFERENCES compras (id_compra),
                FOREIGN KEY (id_loja_embala_comp_loja_embala) REFERENCES loja_embala (id_loja_embala)
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
                custo_total REAL,
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
                retorno REAL DEFAULT 0,
                pacote_preco REAL DEFAULT 0,
                pacote_tam REAL DEFAULT 0,
                quant_pacotes INTEGER DEFAULT 0,
                id_fabricacao_vendas INTEGER,
                FOREIGN KEY (id_fabricacao_vendas) REFERENCES fabricacoes (id_fabricacao)
            )''')

criar_tabelas()