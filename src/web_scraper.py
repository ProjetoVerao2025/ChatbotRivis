from bs4 import BeautifulSoup #bibioteca para filtrar o texto do site
import requests #biblioteca para pegar o texto do site
import json
import os

#link do site a ser utilizado
url = 'https://sistemas.prefeitura.unicamp.br/apps/cardapio/index.php' # ...index.php?d=2025-12-01

#retrieves data from a web server.
page = requests.get(url) 

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

'''retorna um dicionario de dicionarios de dias (Segunda, Terca, Quarta...) de dicionarios de almoco e janta (proteina:, suco:...)'''
def get_week_menu(dias):
    week = {}
    for key, value in dias.items():
        dia_da_semana = key
        url = f'https://sistemas.prefeitura.unicamp.br/apps/cardapio/index.php{value}'
        dia = {} 

        pagina_atual = requests.get(url)
        soup = BeautifulSoup(pagina_atual.text, 'html.parser')

        #[0] = str com o nome da proteina 
        proteina = soup.find_all('div', class_ = "menu-item-name")
        tmp = 0
        for p in proteina:
            if (tmp == 0):
                lunch = {}
                dia['almoco'] = lunch
                lunch['proteina'] = f'{p.text.strip()}'
            elif (tmp == 2):
                dinner = {}
                dia['jantar'] = dinner
                dinner['proteina'] = f'{p.text.strip()}'
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
                        dic['carboidrato'] = output
                    elif (index == 1):
                        dic['guarnicao'] = output
                    elif (index == 2):
                        dic['salada'] = output
                    elif (index == 3):
                        sobremesas = {}
                        first_half = ''
                        second_half = ''
                        fh = True
                        for w in output:
                            if (w == '\n'):
                                break
                            if (w == '|'):
                                fh = False
                                continue
                            if (fh):
                                if (w != ' '):
                                    first_half += w
                            else:
                                if (w != ' '):
                                    second_half += w
                        sobremesa_RU = ''
                        for l in second_half:
                            if (l == '('):
                                break
                            sobremesa_RU += l
                        sobremesas['RU'] = sobremesa_RU
                        sobremesa_demais = ''
                        for k in first_half:
                            if (k == '('):
                                break
                            sobremesa_demais += k
                        sobremesas['RA'] = sobremesas['HC'] = sobremesas['RS'] = sobremesa_demais
                        if (second_half == ''):
                            sobremesas['RU'] = sobremesas['RA']
                        dic['sobremesa'] = sobremesas
                    elif (index == 4):
                        dic['suco'] = output
                    index += 1
            aux += 1
        week[f'{dia_da_semana}'] = dia
    return week

def save_weekly_data(void):
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_raiz = os.path.dirname(diretorio_atual)
    caminho_arquivo = os.path.join(diretorio_raiz, 'weekly-data.json')

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(get_week_menu(dias), f, indent = 4, ensure_ascii = False)