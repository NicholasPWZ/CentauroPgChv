from bs4 import BeautifulSoup as bs
import func
import service


#Função para adicionar página chave na Centauro
def adc_pg_chv():
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
            sku,name,seller,cor,tamanho,preco, url, parcela, vezes = r
            service.inserir(sku,name,seller,cor,tamanho,preco, url, parcela, vezes)

#Função para procurar um produto através de algum atributo
def find_by():
    select = input('Selecione por qual atributo deseja procurar:\n1 - Por SKU\n2 - Por Nome\n3 - Por URL\n4 - Por ID: ')
    if select == '1':
        text = input('Informe o SKU a ser procurado: ')
        service.find_by_sku(text)
    elif select == '2':
        text = input('Informe o Nome a ser procurado: ')
        service.find_by_name(text)
    elif select == '3':
        text = input('Informe a URL a ser procurada: ')
        service.find_by_url(text)
    elif select == '4':
        text = input('Informe o ID a ser procurado: ')
        service.find_by_id(text)

def atualizar_produto():
    id_prod = input("Informe o id do produto: ")
    service.get_url(id_prod)

#Menu roda até que o usuário decida quando parar
while True:
    action = input('Selecione oq deseja fazer:\n1 - Adicionar pagina chave\n2 - Procurar por um produto especifico\n3 - Atualizar informação por ID\n4 - Finalizar programa: ')
    if action == '1':
        adc_pg_chv()
    elif action == '2':
        find_by()
    elif action == '3':
        atualizar_produto()
    elif action == '4':
        break



