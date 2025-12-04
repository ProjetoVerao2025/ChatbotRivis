from bs4 import BeautifulSoup #bibioteca para filtrar o texto do site
import requests #biblioteca para pegar o texto do site

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

week = {} #RETORNO (ESSE CODIGO DEVE SER UMA FUNCAO) DEVE SER UMA DICIONARIO DE DICIONARIOS EM QUE CADA DICT = 1 DIA

#loop para cada dia da semana!!!!!!!!!!!! (NAO IMPLEMENTADO + INTEGRACAO COM O SCHEDULE)


dias_da_semana = soup.find_all('a', class_ = "page-scroll")

dias = {}
for link in dias_da_semana:
    href = link.get('href')
    dia_nome = link.text.strip()
    if href:
        dias[f'{dia_nome}'] = href

#URL = url (varivel existente) + final = dias[Segunda] por ex. PASSAR COMO PARAMETRO PARA A FUNC ABAIXO + WEEK

dia = {} #O PROGRAMA ABAIXO JA IMPLEMENTA CORRETAMENTE O TRATAMENTO DO INPUT PARA 1 DIA INTEIRO (ALMOCO E JANTA) FAZER ISSO APRA A SEMANA TODA DE VEZ

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
                dic['sobremesa'] = output #dicionario de restaurante:sobremesa {RU: "xxxx", RA: "xxxx", HC: "xxxx", RS"xxxx",}
            elif (index == 4):
                dic['suco'] = output
            index += 1
    aux += 1
#print(dia)