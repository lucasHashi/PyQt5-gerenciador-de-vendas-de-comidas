import sqlite3

nome_database = 'db_receitas'


#INSERT_TABLE
def insere_ingrediente(nome, unidade):
    nome = nome.lower()
    unidade = unidade.lower()
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO ingredientes(nome, unidade) VALUES(:nome, :unid)',
                        {'nome':nome, 'unid': unidade})

        cursor.execute('select last_insert_rowid()')
        ultimo_id = cursor.fetchone()[0]

        return ultimo_id

def insere_receita(nome, validade, rendimento, unidade):
    nome = nome.lower()
    unidade = unidade.lower()
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO receitas(nome, rendimento, unidade, validade) VALUES(:nome, :rendi, :unid, :vali)',
                        {'nome':nome, 'rendi': rendimento, 'unid': unidade, 'vali': validade})

        cursor.execute('select last_insert_rowid()')
        ultimo_id = cursor.fetchone()[0]

        return ultimo_id

def insere_ingred_receita(id_receita, id_ingred, quantidade):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('''INSERT INTO ingred_receita(quantidade, id_receita_ingred_receita, id_ingrediente_ingred_receita) 
                            VALUES(:quant, :receita, :ingred)''',
                            {'quant':quantidade, 'receita': id_receita, 'ingred': id_ingred})

        cursor.execute('select last_insert_rowid()')
        ultimo_id = cursor.fetchone()[0]

        return ultimo_id

def insere_embalagem(tamanho, id_ingrediente, id_marca):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('''INSERT INTO embalagens(tamanho, id_ingrediente_embalagens, id_marca_embalagens) 
                            VALUES(:tamanho,:ingred,:marca)''',
                            {'tamanho':tamanho, 'ingred':id_ingrediente, 'marca':id_marca})

        cursor.execute('select last_insert_rowid()')
        ultimo_id = cursor.fetchone()[0]

        return ultimo_id

def insere_loja_embala(preco, id_loja, id_embalagem):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('''INSERT INTO loja_embala(preco, id_loja_loja_embala, id_embalagem_loja_embala) 
                            VALUES(:preco, :loja, :embalagem)''',
                            {'preco':preco, 'loja':id_loja, 'embalagem':id_embalagem})

        cursor.execute('select last_insert_rowid()')
        ultimo_id = cursor.fetchone()[0]

        return ultimo_id

def insere_comp_loja_embala(preco, quantidade, id_compra, id_loja_embalagem):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('''INSERT INTO comp_loja_embala(preco, quantidade, id_compra_comp_loja_embala, id_loja_embala_comp_loja_embala) 
                            VALUES(:preco, :quant, :compra, :loja_embala)''',
                            {'preco':preco, 'quant': quantidade, 'compra':id_compra, 'loja_embala':id_loja_embalagem})

        cursor.execute('select last_insert_rowid()')
        ultimo_id = cursor.fetchone()[0]

        return ultimo_id

def insere_fabricacao(data, custo_total, rendimento, tempo, id_receita):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('''INSERT INTO fabricacoes(data, custo_total, rendimento, tempo_minutos, id_receita_fabricacoes) 
                            VALUES(:data, :custo_total, :rendimento, :tempo, :receita)''',
                            {'data':data, 'custo_total': custo_total, 'rendimento':rendimento, 'tempo':tempo, 'receita': id_receita})

        cursor.execute('select last_insert_rowid()')
        ultimo_id = cursor.fetchone()[0]

        return ultimo_id

def insere_venda(data, local, retorno, pacote_tamanho, pacote_preco, quant_pacotes, id_fabricacao):
    local = local.lower()

    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('''INSERT INTO vendas(data, local, pacote_preco, pacote_tam, quant_pacotes, id_fabricacao_vendas) 
                            VALUES(:data, :local, :pacote_preco, :pacote_tam, :quant_pacotes, :fabricacao)''',
                            {'data':data, 'local': local, 'pacote_preco':pacote_preco, 'pacote_tam':pacote_tamanho,
                                'quant_pacotes': quant_pacotes, 'fabricacao': id_fabricacao})

        cursor.execute('select last_insert_rowid()')
        ultimo_id = cursor.fetchone()[0]

        return ultimo_id

def insere_compra(data):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO compras(data) VALUES(:data)', {'data':data})

        cursor.execute('select last_insert_rowid()')
        ultimo_id = cursor.fetchone()[0]

        return ultimo_id

def insere_marca(nome):
    nome = nome.lower()
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO marcas(nome) VALUES(:nome)', {'nome':nome})

        cursor.execute('select last_insert_rowid()')
        ultimo_id = cursor.fetchone()[0]

        return ultimo_id

def insere_loja(nome):
    nome = nome.lower()
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('INSERT INTO lojas(nome) VALUES(:nome)', {'nome':nome})

        cursor.execute('select last_insert_rowid()')
        ultimo_id = cursor.fetchone()[0]

        return ultimo_id

#SELECT_TABLE_NOMES
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

def select_receitas_nomes():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT DISTINCT id_receita, nome, rendimento, unidade FROM receitas')
        
        lista_receitas = cursor.fetchall()
        lista_receitas_str = []
        
        for linha in lista_receitas:
            receita = '{} - {} - {} - {}'.format(linha[0], linha[1], linha[2], linha[3])
            lista_receitas_str.append(receita)

        return lista_receitas_str

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

def select_fabricacoes_nao_vendidas_nomes(id_receita):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('''SELECT DISTINCT f.id_fabricacao, f.data
                            FROM fabricacoes f, receitas r
                            WHERE NOT id_fabricacao IN 
                            (SELECT id_fabricacao_vendas FROM vendas) 
                            AND f.id_receita_fabricacoes = r.id_receita 
                            AND r.id_receita = :id_receita
                            ''',
                            {'id_receita': id_receita})
        
        lista_fabricacoes = cursor.fetchall()
        lista_fabricacoes_str = []
        
        for linha in lista_fabricacoes:
            fabricacao = '{} - {}'.format(linha[0], linha[1])
            lista_fabricacoes_str.append(fabricacao)

        return lista_fabricacoes_str

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

def select_locais_nomes():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT DISTINCT local FROM vendas')
        
        lista_locais = cursor.fetchall()
        lista_locais_str = []
        
        for linha in lista_locais:
            lista_locais_str.append(str(linha[0]))

        return lista_locais_str

#SELECT_TABLE_LISTA
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

def select_loja_embala_lista():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('''SELECT le.id_loja_embala, e.tamanho, 
                            i.unidade, m.nome, l.nome, le.preco 
                            FROM marcas m, ingredientes i, lojas l,
                            embalagens e, loja_embala le
                            WHERE le.id_embalagem_loja_embala = e.id_embalagem AND 
                            e.id_marca_embalagens = m.id_marca AND 
                            e.id_ingrediente_embalagens = i.id_ingrediente AND 
                            le.id_loja_loja_embala = l.id_loja
                            ''')
        
        lista_loja_embala = cursor.fetchall()

        return lista_loja_embala

def select_lojas_lista():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT id_loja, nome FROM lojas')
        
        lista_lojas = cursor.fetchall()

        return lista_lojas

def select_fabricacoes_nao_vendidas_lista():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('''SELECT f.data, r.nome 
                            FROM fabricacoes f, receitas r 
                            WHERE f.id_receita_fabricacoes = r.id_receita AND 
                            NOT id_fabricacao IN 
                            (SELECT id_fabricacao_vendas 
                                FROM vendas)
                            ''')
        
        lista_nao_vendidas = cursor.fetchall()

        return lista_nao_vendidas


#UPDATE_TABLE
def update_ingrediente(id_ingrediente, nome, unidade):
    nome = nome.lower()
    unidade = unidade.lower()
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('UPDATE ingredientes SET nome = ?, unidade = ? WHERE id_ingrediente = ?', [nome, unidade, id_ingrediente])

def update_receita(id_receita, validade, rendimento, unidade):
    unidade = unidade.lower()
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('UPDATE receitas SET validade = ?, rendimento = ?, unidade = ? WHERE id_receita = ?', [validade, rendimento, unidade, id_receita])

def update_loja_embala(id_loja_embala, preco):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('UPDATE loja_embala SET preco = ? WHERE id_loja_embala = ?', [preco, id_loja_embala])

def update_loja(id_loja, nome):
    nome = nome.lower()
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('UPDATE lojas SET nome = ? WHERE id_loja = ?', [nome, id_loja])


#DELETE_TABLE
def delete_ingrediente(id_ingrediente):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('DELETE FROM ingredientes WHERE id_ingrediente = ?', [id_ingrediente])


#VERIFICA_TABLE_DUPLICADA/O
def verifica_ingrediente_duplicado(nome):
    nome = nome.lower()
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT * FROM ingredientes WHERE nome = :nome', {'nome': nome})
        
        ingrediente_duplicado = cursor.fetchone()

        return True if(ingrediente_duplicado) else False

def verifica_embalagem_duplicada(tamanho, id_ingrediente, id_marca):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('''SELECT * FROM embalagens WHERE tamanho = :tamanho AND 
                        id_ingrediente_embalagens = :ingred AND id_marca_embalagens = :marca''',
                        {'tamanho': tamanho, 'ingred': id_ingrediente, 'marca': id_marca})
        
        ingrediente_duplicado = cursor.fetchone()

        return True if(ingrediente_duplicado) else False

def verifica_marca_duplicada(nome):
    nome = nome.lower()
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT * FROM marcas WHERE nome = :nome', {'nome': nome})
        
        marca_duplicada = cursor.fetchone()

        return True if(marca_duplicada) else False

def verifica_loja_duplicada(nome):
    nome = nome.lower()
    
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT * FROM lojas WHERE nome = :nome', {'nome': nome})
        
        loja_duplicado = cursor.fetchone()

        return True if(loja_duplicado) else False



#FUNCOES ESPECIFICAS

def select_ingredientes_de_receita(id_receita):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        #id_ingrediente, ingrediente, quantidade, unidade
        cursor.execute('''SELECT i.id_ingrediente, i.nome, ir.quantidade, i.unidade
                            FROM ingredientes i, ingred_receita ir, receitas r
                            WHERE ? = r.id_receita
                            AND r.id_receita = ir.id_receita_ingred_receita
                            AND ir.id_ingrediente_ingred_receita = i.id_ingrediente''', [id_receita])
        
        lista_ingredientes_receita = cursor.fetchall()

        return lista_ingredientes_receita

def select_ingredientes_de_loja(id_loja):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        #id_ingrediente, ingrediente, quantidade, unidade
        cursor.execute('''SELECT DISTINCT i.id_ingrediente, i.nome, i.unidade
                            FROM ingredientes i, lojas l, loja_embala le, embalagens e
                            WHERE ? = l.id_loja AND 
                            l.id_loja = le.id_loja_loja_embala AND 
                            le.id_embalagem_loja_embala = e.id_embalagem AND 
                            e.id_ingrediente_embalagens = i.id_ingrediente
                            ''', 
                            [id_loja])
        
        lista_ingredientes_receita = cursor.fetchall()
        lista_ingredientes_str = []
        
        for linha in lista_ingredientes_receita:
            ingred = '{} - {} - {}'.format(linha[0], linha[1], linha[2])
            lista_ingredientes_str.append(ingred)

        return lista_ingredientes_str


def zerar_receita(id_receita):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('DELETE FROM ingred_receita WHERE id_receita_ingred_receita = :id', {'id': id_receita})

def select_loja_embala_por_id(id_loja_embala):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT * FROM loja_embala WHERE id_loja_embala = :id', {'id': id_loja_embala})
        
        loja_embala = cursor.fetchall()[0]

        return loja_embala

def select_loja_embala_por_ingrediente_lista(id_ingrediente):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('''SELECT le.id_loja_embala, e.tamanho, 
                            i.unidade, m.nome, l.nome, le.preco 
                            FROM marcas m, ingredientes i, lojas l,
                            embalagens e, loja_embala le
                            WHERE le.id_embalagem_loja_embala = e.id_embalagem AND 
                            e.id_marca_embalagens = m.id_marca AND 
                            e.id_ingrediente_embalagens = i.id_ingrediente AND 
                            i.id_ingrediente = :id_ingred AND 
                            le.id_loja_loja_embala = l.id_loja
                            ''',
                            {'id_ingred': id_ingrediente})
        
        lista_loja_embala = cursor.fetchall()

        return lista_loja_embala


def select_marca_por_nome(nomeMarca):
    nomeMarca = nomeMarca.lower()
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT id_marca FROM marcas WHERE nome = :nome', {'nome': nomeMarca})
        
        id_marca = cursor.fetchall()[0][0]

        return id_marca

def select_loja_embala_por_ingrediente_loja_nomes(id_loja, id_ingrediente):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('''SELECT le.id_loja_embala, e.id_marca_embalagens, 
                            m.nome, e.tamanho, i.unidade, le.preco
                            FROM loja_embala le, marcas m, ingredientes i, embalagens e 
                            WHERE i.id_ingrediente = :id_ingred 
                            AND e.id_ingrediente_embalagens = i.id_ingrediente 
                            AND e.id_marca_embalagens = m.id_marca 
                            AND le.id_embalagem_loja_embala = e.id_embalagem
                            AND le.id_loja_loja_embala = :id_loja''',
                            {'id_ingred': id_ingrediente, 'id_loja': id_loja})
        
        lista_embalagens = cursor.fetchall()
        lista_embalagens_str = []
        
        for linha in lista_embalagens:
            embalagem = '{} - {} - {} - {} - {} - {}'.format(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5])
            lista_embalagens_str.append(embalagem)

        return lista_embalagens_str

def select_embalagens_por_ingrediente_nomes(id_ingrediente):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('''SELECT e.id_embalagem, e.tamanho,
                            i.unidade, m.nome 
                            FROM embalagens e, marcas m, ingredientes i
                            WHERE e.id_ingrediente_embalagens = :id_ingred AND
                            e.id_ingrediente_embalagens = i.id_ingrediente AND
                            e.id_marca_embalagens = m.id_marca''',
                            {'id_ingred': id_ingrediente})
        
        lista_embalagens = cursor.fetchall()
        lista_embalagens_str = []
        
        for linha in lista_embalagens:
            embalagem = '{} - {} - {} - {}'.format(linha[0], linha[1], linha[2], linha[3])
            lista_embalagens_str.append(embalagem)

        return lista_embalagens_str


def select_dados_fabricacao(id_fabricacao):
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('''SELECT f.custo_total, f.tempo_minutos, 
                            f.rendimento, r.unidade 
                            FROM fabricacoes f, receitas r
                            WHERE f.id_fabricacao == :id_fabrica AND 
                            f.id_receita_fabricacoes = r.id_receita
                            ''',
                            {'id_fabrica': id_fabricacao})
        
        dados_fabricacao = cursor.fetchone()

        return dados_fabricacao

def select_fabricacoes_vendidas():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('''SELECT id_fabricacao_vendas
                            FROM vendas''')
        
        lista_id_fabricacoes = cursor.fetchall()

        lista_ids = []
        for item in lista_id_fabricacoes:
            lista_ids.append(str(item[0]))
        
        return lista_ids

def select_resultados_rececitas():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT DISTINCT id_receita, nome FROM receitas')
        
        lista_receitas = cursor.fetchall()

        dict_receitas = {}
        for linha in lista_receitas:
            cod = linha[0]
            nome = linha[1]

            dict_receitas[str(cod)] = {'nome': nome, 'vezes': 0, 'pacotes': 0, 'gastos': 0, 'ganhos': 0, 'lucro': 0}

        cursor.execute('''SELECT f.id_receita_fabricacoes, f.custo_total, v.quant_pacotes, v.retorno 
                            FROM fabricacoes f, vendas v 
                            WHERE f.id_fabricacao = v.id_fabricacao_vendas''')
        
        lista_fabricacoes = cursor.fetchall()

        for cod, custo_total, quant_pacotes, retorno in lista_fabricacoes:
            dict_receitas[str(cod)]['vezes'] += 1
            dict_receitas[str(cod)]['gastos'] += custo_total
            dict_receitas[str(cod)]['pacotes'] += quant_pacotes
            dict_receitas[str(cod)]['ganhos'] += retorno
            dict_receitas[str(cod)]['lucro'] = float(dict_receitas[str(cod)]['ganhos']) - float(dict_receitas[str(cod)]['gastos'])
        
        list_resultados = []
        for cod in dict_receitas:
            receita = dict_receitas[cod]
            resultado = []
            resultado.append(receita['nome'])
            resultado.append(receita['vezes'])
            resultado.append(receita['pacotes'])
            resultado.append(receita['gastos'])
            resultado.append(receita['ganhos'])
            resultado.append(receita['lucro'])
            list_resultados.append(resultado)
        
        return list_resultados

def select_gastos_totais():
    with sqlite3.connect(nome_database+'.db') as conexao:
        cursor = conexao.cursor()

        cursor.execute('SELECT id_comp_loja_embala, preco, quantidade FROM comp_loja_embala')

        lista_gastos = cursor.fetchall()

        gasto_total = 0
        for _, preco, quant in lista_gastos:
            gasto_total += float(preco) * float(quant)
        
        return gasto_total




















