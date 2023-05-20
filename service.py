import sqlite3

#Função utilizada para inserir os dados dos produtos na table PRODUTOS da database CENTAURO

def inserir(sku,name,seller,cor,tamanho, preco, url, parcela, vezes):
    conn = sqlite3.connect('Centauro_db.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (sku, name, seller, cor, tamanho, preco, url, parcela, vezes) VALUES (?,?, ?, ?, ?, ?,?,?,?)"
                   , (f'{sku}', f'{name}',f'{seller}',f'{cor}',f'{tamanho}', f'{preco}', f'{url}', f'{parcela}', f'{vezes}'))
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
    cursor.execute(f"SELECT * FROM products where name LIKE '%{text}%' ")
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