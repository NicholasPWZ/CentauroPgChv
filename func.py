from bs4 import BeautifulSoup as bs
import requests

def get_produto(slug):
    lista_retorno = []
    for a in slug:
        url = f'https://apigateway.centauro.com.br/ecommerce/v4.3/produtos?codigoModelo={a}'
        json = requests.get(url).json()
        dados_ofertas = {}
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
                dados_ofertas[sku]['url'] = f'https://www.centauro.com.br/{a}'
                dados_ofertas[sku]['nome'], dados_ofertas[sku]['tamanho'], dados_ofertas[sku]['cor'], dados_ofertas[sku]['disponibilidade'] = nome_produto, tamanho, cor, disponibilidade 

        lista_precos = json['precos']
        for i in lista_precos:
            sku, preco_de, preco_por = i['sku'], i['valorDe'], i['valor']
            
            try:
                seller = i['nomeSeller']
            except:
                seller = '-'
            try:
                vezes_parcela, preco_parcela = i['numeroDeParcelas'], i['quantidadePorParcela']
            except:
                pass
            try:
                validar = dados_ofertas[sku]
            except:
                continue
            dados_ofertas[sku]['precoDe'], dados_ofertas[sku]['precoPor'], dados_ofertas[sku]['vendidoPor'], dados_ofertas[sku]['vezesParcela'], dados_ofertas[sku]['precoParcela'] = preco_de, preco_por, seller, vezes_parcela, preco_parcela

        for i in dados_ofertas:
            nome, cor, tamanho = dados_ofertas[i]['nome'], dados_ofertas[i]['cor'], dados_ofertas[i]['tamanho'] 
            try:
                seller ,preco_de, preco_por, vezes_parcela, preco_parcela = dados_ofertas[i]['vendidoPor'] , dados_ofertas[i]['precoDe'],dados_ofertas[i]['precoPor'], dados_ofertas[i]['vezesParcela'], dados_ofertas[i]['precoParcela']
            except:
                seller ,preco_de, preco_por, vezes_parcela, preco_parcela = 'SEM ESTOQUE', '-',  '-',  '-', '-'
            
            
            lista_retorno.append((sku ,nome, seller, cor, tamanho, preco_por ,dados_ofertas[i]["url"]))
            

def pg_chave(url):
    json = requests.get(url).json()
    lista_pagina = json['products']
    lista_slug = []
    for i in lista_pagina:
        url_inteira = i['url']
        url_formatada = url_inteira.split('?')[0]
        slug = url_formatada.replace('//www.centauro.com.br', '')
        lista_slug.append(slug)
    return lista_slug    

    