from bs4 import BeautifulSoup as bs
import func
import service

#Solicitando a url da página chave
url = input('Insira a página chave da Centauro(#1 é a variável): ')
#Solicitando a quantidade de páginas a serem adicionadas
qtd = input('Informe a quantidade de páginas: ')
qtd = int(qtd) + 1
url_separada = url.split('#1')

#Adicionando o número das páginas até o numero informado, e após isso inserindo cada tupla presente na lista dentro do banco de dados
for i in range(qtd):
    url_formatada = f'{url_separada[0]}{i}{url_separada[1]}'
    lista_data = func.get_produto(func.pg_chave(url_formatada))
    for r in lista_data:
        sku,name,seller,cor,tamanho,preco, url = r
        service.inserir(sku,name,seller,cor,tamanho,preco, url)
    







