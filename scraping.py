import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

lista_produtos = []

def buscar_page():
    response = requests.get(f'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1&page=1')
    HTML = response.content
    site = BeautifulSoup(HTML, 'html.parser')

    pages = site.find('div', attrs={'class':'content content__margin'})
    proximo = site.findAll('a', attrs={'class':'andes-pagination__link'})
    proximo = proximo[-2]

    return proximo.text



for i in range(1, int(buscar_page())+1):

    response = requests.get(f'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1&page={i}')
    HTML = response.content
    site = BeautifulSoup(HTML, 'html.parser')

    produtos = site.findAll('div', attrs={'promotion-item__description'})

    for produto in produtos:
        titulo = produto.find('p', attrs={'class':'promotion-item__title'})
        titulo = titulo.text
        preco = produto.find('span', attrs={'class': 'promotion-item__price'})
        preco = preco.text

        if not '.' in preco:
            if len(preco) >= 7 and len(preco) < 8:
                preco = f'R${preco[2:5]},{preco[5:7]}'
            elif len(preco) >= 8 and len(preco) < 9:
                preco = f'R${preco[2:6]},{preco[6:8]}'
        
        lista_produtos.append([titulo, preco])

df = pd.DataFrame(lista_produtos, columns=['Produto', 'Preço'])
table = df.to_dict('records')

with open('produtos.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(table, indent=4)
    jp.write(js)