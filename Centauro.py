from bs4 import BeautifulSoup as bs
import func
import service


url = input('Insira a página chave da Centauro(#1 é a variável): ')
qtd = input('Informe a quantidade de páginas: ')
qtd = int(qtd) + 1
url_separada = url.split('#1')

for i in range(qtd):
    url_formatada = f'{url_separada[0]}{i}{url_separada[1]}'
    lista_data = func.get_produto(func.pg_chave(url_formatada))
    sku,name,seller,cor,tamanho = lista_data[0], lista_data[1], lista_data[2], lista_data[3], lista_data[4]
    service.inserir(sku,name,seller,cor,tamanho)
    







