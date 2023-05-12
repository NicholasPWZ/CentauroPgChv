from bs4 import BeautifulSoup as bs
import requests

#Função que recebe a url de página chave da Centauro
def pg_chave(url):
    #Utilizando lib Requests para capturar o código json da página
    json = requests.get(url).json()
    lista_pagina = json['products']
    #Criando a lista que armazenará a parte final da url de cada produto encontrado na página
    lista_slug = []
    #Iterando pela lista de produtos e capturando a chave 'url' de onde será extraído o código cliente utilizado na API para captura dos dados
    for i in lista_pagina:
        url_inteira = i['url']
        url_formatada = url_inteira.split('?')[0]
        slug = url_formatada.replace('//www.centauro.com.br', '')
        #Adicionando o código cliente ou 'SLUG' a lista e após isso retornando ela para utilização futura
        lista_slug.append(slug)
    return lista_slug    


#Função que recebe o 'SLUG' capturado anteriormente na página chave e utiliza um de cada vez para capturar os dados dos produtos
def get_produto(slug):
    #Criando a lista que irá retornar as informações dos produtos
    lista_retorno = []
    #Iteração da lista que foi retornada na função anterior de páginas chave
    for a in slug:
        url = f'https://apigateway.centauro.com.br/ecommerce/v4.3/produtos?codigoModelo={a}'
        json = requests.get(url).json()
        #Criando o dicionário que irá armazenar temporáriamente os dados dos produtos através de código SKU
        dados_ofertas = {}
        #Criando variáveis e atribuindo valores que estão presentes no json da página do produto
        try:
            nome_produto = json['informacoes']['nome']
        except:
            continue
        lista_cores = json['disponibilidade']['cores']
        for p in lista_cores:
            cor = p['nomeCor']
            lista_tamanhos = p['todosTamanhos']
            for x in lista_tamanhos:
                tamanho, sku, disponibilidade = x['tamanho'], x['sku'], x['stiuacao']
                dados_ofertas[sku] = {}
                dados_ofertas[sku]['url'] = f'https://www.centauro.com.br{a}'
                dados_ofertas[sku]['nome'], dados_ofertas[sku]['tamanho'], dados_ofertas[sku]['cor'], dados_ofertas[sku]['disponibilidade'] = nome_produto, tamanho, cor, disponibilidade 

        lista_precos = json['precos']
        for i in lista_precos:
            sku2, preco_de, preco_por = i['sku'], i['valorDe'], i['valor']
            
            try:
                seller = i['nomeSeller']
            except:
                seller = 'CENTAURO'
            try:
                vezes_parcela, preco_parcela = i['numeroDeParcelas'], i['quantidadePorParcela']
            except:
                pass
            #Validando de a chave é existente
            try:
                validar = dados_ofertas[sku]
            except:
                continue
            dados_ofertas[sku2]['precoDe'], dados_ofertas[sku2]['precoPor'], dados_ofertas[sku2]['vendidoPor'], dados_ofertas[sku2]['vezesParcela'], dados_ofertas[sku2]['precoParcela'] = preco_de, preco_por, seller, vezes_parcela, preco_parcela

        for i in dados_ofertas:
            nome, cor, tamanho = dados_ofertas[i]['nome'], dados_ofertas[i]['cor'], dados_ofertas[i]['tamanho'] 
            try:
                seller ,preco_de, preco_por, vezes_parcela, preco_parcela = dados_ofertas[i]['vendidoPor'] , dados_ofertas[i]['precoDe'],dados_ofertas[i]['precoPor'], dados_ofertas[i]['vezesParcela'], dados_ofertas[i]['precoParcela']
            except:
                seller ,preco_de, preco_por, vezes_parcela, preco_parcela = 'SEM ESTOQUE', '-',  '-',  '-', '-'
            
            #Inserindo os dados de uma variação específica dentro de uma lista em formato de tupla.
            lista_retorno.append((sku ,nome, seller, cor, tamanho, preco_por, dados_ofertas[i]["url"]))
    #Retornando as informações dos produtos e de suas variações      
    return lista_retorno




    