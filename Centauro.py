from bs4 import BeautifulSoup as bs
import requests

#solicitando a url para captura dos dados
url = input('Informe a url da API da centauro que você deseja realizar a captura dos dados: ')
json = requests.get(url).json()

#definindo os caminhos principais para onde vamos entrar e capturar as informações
dispo = json['disponibilidade']
precos = json['precos']
nome = dispo['nome']
cores = dispo['cores']
dicionario = { }

#capturando o nome da cor e uma lista com as informações do SKU das ofertas
for i in cores:
    nomeCor = i['nomeCor']  
    iteraSeller = i['tamanhosDisponiveis']
    for p in iteraSeller: 
        sku = p['sku']  
        dicionario[sku] = {}
        dicionario[sku] = p
        dicionario[sku]['cor'] = nomeCor
        dicionario[sku]['nome'] = nome
#capturando o preço e adicionando a chave do respectivo sku
for p in precos:
    skup = p['sku']
    dicionario[skup]['valor'] = p

#Usuario decide se quer procurar por uma oferta específica ou se quer dados de todas as ofertas
flag = input('Deseja procurar por um SKU específico? (S ou N): ')
if flag.lower() == 's':
    flag = True
else:
    flag = False
while flag:
    id = input('Informe o SKU: ')

    informacao = input('Informe a informação a ser buscada sobre esse produto\nPreço -> (valor)\nParcelamento -> (parcelamento)\nSeller -> (nomeSeller)\nSituação -> (situacao)\nCor -> (cor)\nTudo\n->: ')

#informando o que for solicitado pelo usuário, utilizando os dados que ja foram capturados e estão alocados no dicionário que foi criado
    try:
        if informacao.lower() == 'parcelamento':
            lista_parcela = dicionario[id]['valor']['parcelamentos']
            size_parcela = len(lista_parcela) - 1
            print(dicionario[id]['valor']['parcelamentos'][size_parcela]['quantidade'])    
            print(dicionario[id]['valor']['parcelamentos'][size_parcela]['valor'])
        elif informacao.lower() == 'valor':
            print(dicionario[id]['valor'][informacao])
        elif informacao.lower() == 'tudo':
            print(dicionario[id])
        else:
            try:
                print(dicionario[id][informacao])
            except:
                if informacao == 'nomeSeller' and id[0] == '9':
                    print('Centauro')
                else:
                    print('Informe a informação a ser capturada corretamente')
#Forçando um erro da aplicação caso o SKU informado for inválido.
        dicionario[id]
    except:
#Imprimindo todas as chaves do dicionário(SKUs) para o usuário realizar uma consulta.        
        print('Escolha uma chave correta:', *dicionario)

#Fornecendo os principais dados para o usuário de todas as ofertas desse produto.

for i in dicionario:
    print(dicionario[i]['nome'], dicionario[i]['tamanho'],dicionario[i]['cor'], dicionario[i]['sku'], dicionario[i]['nomeSeller'], dicionario[i]['valor']['valorPadrao'] )


