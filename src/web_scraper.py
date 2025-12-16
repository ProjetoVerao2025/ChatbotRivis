from bs4 import BeautifulSoup #bibioteca para filtrar o texto do site
from src.config import config
import requests #biblioteca para pegar o texto do site
import json
import os
import re

'''Trata os casos de input no estilo: BANANA (RA/RS/HS) | LARANJA (RU), retorna l=BANANA e r=LARANJA'''
def splitter(sobremesa_str):
    uma_sobremesa = False
    
    if "|" not in sobremesa_str:
        uma_sobremesa = True

    restaurantes = ["RA", "RS", "HC", "RU"]
    sobremesas = sobremesa_str.split("|")

    if len(sobremesas) == 1 or uma_sobremesa == True:
        # So tem uma sobremesa pra todo mundo
        s = {r:sobremesas[0] for r in restaurantes}
        return s
    
    s = {r:"" for r in restaurantes}
    # Tem mais de uma ebaa
    for sob in sobremesas:
        for r in restaurantes:
            if r in sob.split("(")[1]:
                s[r] = sob.split("(")[0].strip() # Tirando os restaurantes da string
    return s #retorno do tipo: {'RA': 'BANANA', 'RS': 'BANANA', 'HC': 'GOIABADA', 'RU': 'LARANJA'}

#link do site a ser utilizado
# ...index.php?d=2025-12-01

#retrieves data from a web server.
page = requests.get(config.url_cardapio) 

#html do site "print(soup.prettify()"
soup = BeautifulSoup(page.text, 'html.parser') 

#soup.find (acha a primeira instancia de um objeto html), possibilita o .text
#soup.find_all (acha toda as instancias daquele tipo de objeto html)
#soup.find_all('div', class_ = '') para buscas especificas com base na classe

#cardapio = soup.find_all('div', class_ = "menu-item")
#print(cardapio)

dias_da_semana = soup.find_all('a', class_ = "page-scroll")

dias = {}
for link in dias_da_semana:
    href = link.get('href')
    dia_nome = link.text.strip()
    if href:
        dias[f'{dia_nome}'] = href

'''retorna um dicionario de dicionarios de dias (Segunda, Terca, Quarta...) de dicionarios de almoco e janta (proteina:, suco:...) de dicionarios de restaurantes (RA, RS, HC e RU) com o menu do dia'''
def get_week_menu(dias):
    week = {}
    for key, value in dias.items():
        url = f'{config.url_cardapio}/index.php{value}'
        dia = {} 

        pagina_atual = requests.get(url)
        soup = BeautifulSoup(pagina_atual.text, 'html.parser')

        #[0] = str com o nome da proteina 
        proteina = soup.find_all('div', class_ = "menu-item-name")
        tmp = 0
        for p in proteina:
            p = p.text.strip()
            if (tmp == 0):
                HC = RS = RA = RU = {}
                lunch = {'HC':HC,'RS':RS,'RA':RA,'RU':RU}
                dia['almoco'] = lunch
                # lunch['proteina'] = f'{p.text.strip()}'
                for restaurante,proteina in splitter(p).items():
                    lunch[f'{restaurante}']['proteina'] = proteina
            elif (tmp == 2):
                HC = RS = RA = RU = {}
                dinner = {'HC':HC,'RS':RS,'RA':RA,'RU':RU}
                dia['jantar'] = dinner
                # dinner['proteina'] = f'{p.text.strip()}'
                for restaurante,proteina in splitter(p).items():
                    dinner[f'{restaurante}']['proteina'] = proteina
            tmp += 1

        #[0] = padroes ('arroz e feijao'), [1] = especial, [2] = salada, [3] = sobremesa (output especial), [4] = refresco
        acompanhamentos = soup.find_all('div', class_ = "menu-item-description")
        aux = 0
        for list in acompanhamentos:
            if (aux == 1 or aux == 3):
                aux += 1
                continue
            index = 0 
            for a in list:
                if (aux == 0):
                    dic = lunch
                else:
                    dic = dinner
                if (a.text.strip() != ''):
                    output = f'{a.text.strip()}'
                    if (index == 0):
                        for restaurante, carb in splitter(output).items():
                            dic[f'{restaurante}']['carboidrato'] = carb
                    elif (index == 1):
                        for restaurante, guar in splitter(output).items():
                            dic[f'{restaurante}']['guarnicao'] = guar
                    elif (index == 2):
                        for restaurante, salad in splitter(output).items():
                            dic[f'{restaurante}']['salada'] = salad
                    elif (index == 3):
                        for restaurante, sobremesa in splitter(output).items():
                            dic[f'{restaurante}']['sobremesa'] = sobremesa
                    elif (index == 4):
                        for restaurante, suco in splitter(output).items():
                            dic[f'{restaurante}']['suco'] = suco
                    index += 1
            aux += 1
        week[f'{value[3:]}'] = dia
    return week

'''funcao que chama a funcao de web_scrapping e salva seu output em "weekly'''
def save_weekly_data():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_raiz = os.path.dirname(diretorio_atual)
    caminho_arquivo = os.path.join(diretorio_raiz, config.week_meals_file)

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(get_week_menu(dias), f, indent = 4, ensure_ascii = False)
        
if __name__ == "__main__":
    save_weekly_data()
