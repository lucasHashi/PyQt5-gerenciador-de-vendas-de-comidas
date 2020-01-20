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

def insere_ingrediente(nome, unidade):
    nome = nome.lower()
    unidade = unidade.lower()
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO ingredientes(nome, unidade) VALUES(:nome, :unid)', {'nome':nome, 'unid': unidade})

def insere_receita(nome_receita, validade, rendimento, unidade):
    nome_receita = nome_receita.lower()
    unidade = unidade.lower()
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO receitas(nome, rendimento, unidade, validade) VALUES(:nome, :rendi, :unid, :vali)', {'nome':nome_receita, 'rendi': rendimento, 'unid': unidade, 'vali': validade})

        cursor.execute('select last_insert_rowid()')

        ultimo_cod = cursor.fetchone()[0]

        return ultimo_cod

def insere_ingred_receita(cod_receita, cod_ingred, quantidade):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO ingred_receita(quantidade, id_receita_ingred_receita, id_ingrediente_ingred_receita) VALUES(:quant, :receita, :ingred)', {'quant':quantidade, 'receita': cod_receita, 'ingred': cod_ingred})


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

        cursor.execute('SELECT DISTINCT * FROM ingredientes')
        
        lista_ingredientes = cursor.fetchall()
        lista_ingredientes_str = []
        
        for linha in lista_ingredientes:
            ingrediente = '{} - {} - {}'.format(linha[0], linha[1], linha[2])
            lista_ingredientes_str.append(ingrediente)

        return lista_ingredientes_str

def select_ingredientes_lista():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT * FROM ingredientes')
        
        lista_ingredientes = cursor.fetchall()

        return lista_ingredientes

def select_receitas_lista():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT id_receita, nome, validade, rendimento, unidade FROM receitas')
        
        lista_receitas = cursor.fetchall()

        return lista_receitas

def select_ingredientes_de_receita(cod_receita):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        #cod_ingrediente, ingrediente, quantidade, unidade
        cursor.execute('''SELECT i.id_ingrediente, i.nome, ir.quantidade, r.unidade
                            FROM ingredientes i, ingred_receita ir, receitas r
                            WHERE ? = r.id_receita
                            AND r.id_receita = ir.id_receita_ingred_receita
                            AND ir.id_ingrediente_ingred_receita = i.id_ingrediente''', [cod_receita])
        
        lista_ingredientes_receita = cursor.fetchall()

        return lista_ingredientes_receita



def update_ingrediente(cod, nome, unidade):
    nome = nome.lower()
    unidade = unidade.lower()
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('UPDATE ingredientes SET nome = ?, unidade = ? WHERE id_ingrediente = ?', [nome, unidade, cod])

def update_receita(cod_receita, validade, rendimento, unidade):
    unidade = unidade.lower()
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('UPDATE receita SET validade = ?, rendimento = ?, unidade = ? WHERE id_receita = ?', [validade, rendimento, unidade, cod_receita])



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

def varifica_ingrediente_duplicado(nome):
    nome = nome.lower()
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT * FROM ingredientes WHERE nome = :nome', {'nome': nome})
        
        ingrediente_duplicado = cursor.fetchone()

        return True if(ingrediente_duplicado) else False


def cod_ultimo_insert():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('select last_insert_rowid()')

        ultimo_cod = cursor.fetchone()[0]

        return ultimo_cod


def zerar_receita(cod_receita):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('DELETE FROM ingred_receita WHERE id_receita_ingred_receita = :cod', {'cod': cod_receita})


#print(select_marcas_nomes())
#print(varifica_ingrediente_duplicado('Chocolate', 'g', 150, 2))