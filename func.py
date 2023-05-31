from bs4 import BeautifulSoup as bs
import requests
import service

header = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGlnYXRld2F5LmRjLnNibmV0Iiwic3ViIjoid3d3LmNlbnRhdXJvLmNvbS5iciIsImlhdCI6MTUxNjIzOTAyMiwiY2xpZW50X2lkIjoiZTU3Nzk3ZDYtN2Y3Mi00MzMwLWJjOTItOTM3MWRiNjI0YjQ5In0.Mc2PpOJwltFymE3He95TpGTBPDAbhmxNw-cJEsYTghnGefWwhyiD--EopZquF2uH0bdF7K95SkK5RNaZ05Mh3ShuTbqPtD8D7kSr_zQO80nAyIHleLwQzrqrn5GF9piwVSt7YfVDWxj8rNA5HlXQpdTuu0vEUjHQk4hpapB8MtmE1qg9-bymyhD4Hm7x2XHMa-4AtPxhBotPBUwQKWNTbh3OUbCAETknA2tnwfFCSSS3nXot6Icuwx3hvtnkFTk3XitjPwLZ8xTlIJ5Uyk8MjjdG-poMFHKLrdvF7YzhAHUoNn-9Y91jIaYrSA_hDjgb-1y25Jw7UR_lO5F3ceSimg",
    "if-modified-since": "Fri, 19 May 2023 14:09:17 GMT",
    "origin": "https://www.centauro.com.br",
    "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

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
        try:
            json = requests.get(url).json()
        except:
            continue
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
                validar = dados_ofertas[sku2]
            except:
                continue
            dados_ofertas[sku2]['precoDe'], dados_ofertas[sku2]['precoPor'], dados_ofertas[sku2]['vendidoPor'], dados_ofertas[sku2]['vezesParcela'], dados_ofertas[sku2]['precoParcela'] = preco_de, preco_por, seller, vezes_parcela, preco_parcela

        for i in dados_ofertas:
            sku, nome, cor, tamanho =i, dados_ofertas[i]['nome'], dados_ofertas[i]['cor'], dados_ofertas[i]['tamanho'] 
            try:
                seller ,preco_de, preco_por, vezes_parcela, preco_parcela = dados_ofertas[i]['vendidoPor'] , dados_ofertas[i]['precoDe'],dados_ofertas[i]['precoPor'], dados_ofertas[i]['vezesParcela'], dados_ofertas[i]['precoParcela']
            except:
                seller ,preco_de, preco_por, vezes_parcela, preco_parcela = '-', '-',  '-',  '-', '-'
            
            #Inserindo os dados de uma variação específica dentro de uma lista em formato de tupla.
            lista_retorno.append((sku ,nome, seller, cor, tamanho, preco_por,dados_ofertas[i]["url"], preco_parcela, vezes_parcela))
    #Retornando as informações dos produtos e de suas variações      
    return lista_retorno

def att_info(url, sku):
    url = url.replace('https://www.centauro.com.br', '')
    link = f'https://apigateway.centauro.com.br/ecommerce/v4.3/produtos?codigoModelo={url}'
    json = requests.get(link).json()
    nome = json['informacoes']['nome']
    lista_precos = json['precos']
    for i in lista_precos:
        if i['sku'] == sku:
            try:
                preco_de, preco_por = i['valorDe'], i['valor']
            except:
                preco_de, preco_por = '-', i['valor']
            try:
                seller = i['nomeSeller']
            except:
                seller = 'CENTAURO'
            try:
                vezes_parcela, preco_parcela = i['numeroDeParcelas'], i['quantidadePorParcela']
            except:
                 vezes_parcela, preco_parcela = '-', '-'
            break
        else:
           preco_de, preco_por, seller, preco_parcela, vezes_parcela = '0,00', '0,00', '-', '0,00', '0'
    return nome, preco_por, seller, preco_parcela, vezes_parcela



    