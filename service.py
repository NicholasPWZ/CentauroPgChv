import sqlite3
import func
#Função utilizada para inserir os dados dos produtos na table PRODUTOS da database CENTAURO



def inserir(sku,name,seller,cor,tamanho, preco, url, parcela, vezes):
    conn = sqlite3.connect('Centauro_db.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (sku, nome, seller, cor, tamanho, preco, url, vezes_parcela, preco_parcela) VALUES (?,?, ?, ?, ?, ?,?,?,?)"
                   , (f'{sku}', f'{name}',f'{seller}',f'{cor}',f'{tamanho}', f'{preco}', f'{url}', f'{vezes}', f'{parcela}'))
    conn.commit()
    conn.close()

#Funções de busca para atributos diversos
def find_by_sku(sku):
    conn = sqlite3.connect('Centauro_db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM products where sku LIKE '%{sku}%' ")
    #Transformando o retorno do select em linhas para retornar em python
    lines = cursor.fetchall()
    for i in lines:
        print(i)
    conn.commit()
    conn.close()

def find_by_url(text):
    conn = sqlite3.connect('Centauro_db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM products where url LIKE '%{text}%' ")
    #Transformando o retorno do select em linhas para retornar em python
    lines = cursor.fetchall()
    for i in lines:
        print(i)
    conn.commit()
    conn.close()

def find_by_name(text):
    conn = sqlite3.connect('Centauro_db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM products where nome LIKE '%{text}%' ")
    #Transformando o retorno do select em linhas para retornar em python
    lines = cursor.fetchall()
    for i in lines:
        print(i)
    conn.commit()
    conn.close()

def find_by_id(num):
    conn = sqlite3.connect('Centauro_db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM products where id = '{num}' ")
    #Transformando o retorno do select em linhas para retornar em python
    lines = cursor.fetchall()
    for i in lines:
        print(i)
    conn.commit()
    conn.close()

def get_url(num):
    conn = sqlite3.connect('Centauro_db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT url from products p where id = {num}")
    line = cursor.fetchall()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(f"SELECT sku from products p where id = {num}")
    sku = cursor.fetchall()
    cursor.close()
    lista_att = func.att_info(line[0][0], sku[0][0])
    nome,  preco_por, seller, preco_parcela, vezes_parcela = lista_att[0], lista_att[2], lista_att[3], lista_att[4], lista_att[5]
    preco_por, preco_parcela = preco_por.replace(',','.'), preco_parcela.replace(',', '.')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE products SET nome ='{nome}', preco = {float(preco_por)}, seller = '{seller}', vezes_parcela = {vezes_parcela}, preco_parcela = {float(preco_parcela)} WHERE id ={num}")
    conn.commit()
    conn.close()
    


    