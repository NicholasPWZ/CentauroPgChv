import sqlite3

#Função utilizada para inserir os dados dos produtos na table PRODUTOS da database CENTAURO

def inserir(sku,name,seller,cor,tamanho, preco,url):
    conn = sqlite3.connect('Centauro_db.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (sku, name, seller, cor, tamanho, preco, url) VALUES (?,?, ?, ?, ?, ?,?)", (f'{sku}', f'{name}',f'{seller}',f'{cor}',f'{tamanho}', f'{preco}', f'{url}'))
    conn.commit()
    conn.close()
