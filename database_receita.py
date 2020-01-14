import sqlite3

nome_database = 'db_receitas'

#FUNC BASE PARA ADICIONAR COISAS
def insere_TABELA(entradas):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO tabela(dados) VALUES(:dados)', {'dados':entradas})

def insere_loja(nomeLoja):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO lojas(nome) VALUES(:nome)', {'nome':nomeLoja})

def insere_marca(nome):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO marcas(nome) VALUES(:nome)', {'nome':nome})

def insere_ingrediente(nome, unidade, tamanho, id_marca):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO ingredientes(nome, unidade, tam_embalagem, id_marca_ingredientes) VALUES(:nome, :unidade, :tam, :marca)', {'nome':nome, 'unidade': unidade, 'tam': tamanho, 'marca': id_marca})


def select_lojas_nomes():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT id_loja, nome FROM lojas')
        
        lista_lojas = cursor.fetchall()
        lista_lojas_str = []
        
        for linha in lista_lojas:
            loja = '{} - {}'.format(linha[0], linha[1])
            lista_lojas_str.append(loja)

        return lista_lojas_str

def select_marcas_nomes():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT id_marca, nome FROM marcas')
        
        lista_marcas = cursor.fetchall()
        lista_marcas_str = []
        
        for linha in lista_marcas:
            marca = '{} - {}'.format(linha[0], linha[1])
            lista_marcas_str.append(marca)

        return lista_marcas_str

def select_marca_por_nome(nomeMarca):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT id_marca FROM marcas WHERE nome = :nome', {'nome': nomeMarca})
        
        id_marca = cursor.fetchall()[0][0]

        return id_marca

#print(select_marcas_nomes())