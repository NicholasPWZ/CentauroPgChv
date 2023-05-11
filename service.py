import sqlite3

# # Conectando ao banco de dados ou criando um novo se não existir
# conn = sqlite3.connect('exemplo.db')

# # Criando uma tabela
# conn.execute('''CREATE TABLE IF NOT EXISTS usuarios
#                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 nome TEXT NOT NULL,
#                 email TEXT NOT NULL);''')

# # Inserindo dados na tabela
# conn.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", ('João', 'joao@email.com'))

# # Selecionando dados
# cursor = conn.execute("SELECT * FROM usuarios")
# for row in cursor:
#     print(row)

# # Fechando a conexão com o banco de dados
# conn.close()



def inserir(sku,name,seller,cor,tamanho):
    conn = sqlite3.connect('Centauro_db.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (sku, name, seller, cor, tamanho) VALUES (?, ?, ?, ?, ?)", (f'{sku}', f'{name}',f'{seller}',f'{cor}',f'{tamanho}'))
    conn.commit()
    conn.close()
