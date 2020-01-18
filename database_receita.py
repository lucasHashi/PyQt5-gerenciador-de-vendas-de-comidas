import sqlite3

nome_database = 'db_receitas'

#FUNC BASE PARA ADICIONAR COISAS
def insere_TABELA(entradas):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO tabela(dados) VALUES(:dados)', {'dados':entradas})

def insere_loja(nome_loja):
    nome_loja = nome_loja.lower()
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO lojas(nome) VALUES(:nome)', {'nome':nome_loja})

def insere_marca(nome):
    nome = nome.lower()
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO marcas(nome) VALUES(:nome)', {'nome':nome})

def insere_ingrediente(nome, unidade, tamanho, id_marca):
    nome = nome.lower()
    unidade = unidade.lower()
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
    nomeMarca = nomeMarca.lower()
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT id_marca FROM marcas WHERE nome = :nome', {'nome': nomeMarca})
        
        id_marca = cursor.fetchall()[0][0]

        return id_marca

def select_ingredientes_nomes():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT DISTINCT nome, tam_embalagem, unidade FROM ingredientes')
        
        lista_ingredientes = cursor.fetchall()
        lista_ingredientes_str = []
        
        for linha in lista_ingredientes:
            ingrediente = '{} - {} - {}'.format(linha[0], linha[1],linha[2])
            lista_ingredientes_str.append(ingrediente)

        return lista_ingredientes_str

def select_ingredientes_lista():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT i.id_ingrediente, i.nome, i.tam_embalagem, i.unidade, m.nome FROM ingredientes i, marcas m WHERE i.id_marca_ingredientes = m.id_marca')
        
        lista_ingredientes = cursor.fetchall()

        return lista_ingredientes

def update_ingrediente(cod, nome, unidade, tamanho, id_marca):
    nome = nome.lower()
    unidade = unidade.lower()
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('UPDATE ingredientes SET nome = :nome, unidade = :unidade, tam_embalagem = :tamanho, id_marca_ingredientes = :marca WHERE id_ingrediente = :cod', [nome, unidade, tamanho, id_marca, cod])
        

def delete_ingrediente(cod):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('DELETE FROM ingredientes WHERE id_ingrediente = ?', [cod])


def varifica_marca_duplicada(nome):
    nome = nome.lower()
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT * FROM marcas WHERE nome = :nome', {'nome': nome})
        
        marca_duplicada = cursor.fetchone()

        return True if(marca_duplicada) else False

def varifica_ingrediente_duplicado(nome, unidade, tamanho, id_marca):
    nome = nome.lower()
    unidade = unidade.lower()
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT * FROM ingredientes WHERE nome = :nome AND unidade = :unidade AND tam_embalagem = :tamanho AND id_marca_ingredientes = :marca', {'nome': nome,'unidade': unidade,'tamanho': tamanho,'marca': id_marca})
        
        ingrediente_duplicado = cursor.fetchone()

        return True if(ingrediente_duplicado) else False



#print(select_marcas_nomes())
#print(varifica_ingrediente_duplicado('Chocolate', 'g', 150, 2))