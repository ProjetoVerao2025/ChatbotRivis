from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests, os, json
from dataclasses import dataclass
# 2025-03-01 ate 2025-12-08 (FORMATACAO: ?d=2025-12-01) 

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

@dataclass
class Config():
    week_meals_file = './aaa.json'

config = Config()

day = date.today()
url = f'https://sistemas.prefeitura.unicamp.br/apps/cardapio/index.php?d={day.isoformat()}' #...index.php?d=2025-12-01
proteinas = set()
guarnicao = set()
sobremesas = set()
refrescos = set()
saladas = set()

while day.month >= 3: #tem q ir ate mes 3
    day = day - timedelta(days=1)
    
    url = f'https://sistemas.prefeitura.unicamp.br/apps/cardapio/index.php?d={day.isoformat()}' #...index.php?d=2025-12-01

    chave = day.isoformat()
    pagina = requests.get(url)
    html = pagina.text
    soup = BeautifulSoup(html, 'html.parser')

    # criar um set() para sobremesa, suco, proteina, guarnicao .add()

    #objeto de retorno
    resposta = {'proteina': proteinas, 'guarnicao':guarnicao, 'sobremesas':sobremesas, 'refrescos':refrescos}

    #[0] = almoco, [1] = almoco vegano, [2] = jantar e [3] = jantar vegano
    proteina = soup.find_all('div', class_ = "menu-item-name")

    tmp = 0
    for p in proteina:
        p = p.text.strip()
        if (tmp == 0 or tmp == 2):
            resposta['proteina'].add(p)
        tmp += 1

    #[0] = padroes ('arroz e feijao'), [1] = especial, [2] = salada, [3] = sobremesa (output especial), [4] = refresco
    acompanhamentos = soup.find_all('div', class_ = "menu-item-description")

    aux = 0
    for list in acompanhamentos:
        index = 0
        if aux == 0:
            aux += 1
            continue
        for a in list:
            if (a.text.strip() != ''):
                output = f'{a.text.strip()}'
                if (index == 1):
                    for _, guar in splitter(output).items():
                        if guar != "":
                            guarnicao.add(guar)
                elif (index == 2):
                    for _, salada in splitter(output).items():
                        if salada != "":
                            saladas.add(salada)
                elif (index == 3):
                    for _, sobremesa in splitter(output).items():
                        if sobremesa != "":
                            sobremesas.add(sobremesa)
                elif (index == 4):
                    for _, refresco in splitter(output).items():
                        if refresco != "":
                            refrescos.add(refresco)
                index += 1
        aux += 1

    ### transformar os sets em listas para dump ###


    
    dados = [proteinas, guarnicao, sobremesas, refrescos]

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_raiz = os.path.dirname(diretorio_atual)

    arquivos = ['proteina', 'guarnicao', 'sobremesas', 'refrescos', 'salada']
    dados = [proteinas, guarnicao, sobremesas, refrescos, saladas]

for i, arq in enumerate(arquivos):
    caminho_arquivo = os.path.join(diretorio_raiz, arq)
    caminho_arquivo = f'{arq}.json'
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        if type(dados[i]) == set:
            json.dump([*dados[i]], f, indent = 4, ensure_ascii = False)
        else:
            json.dump([dados[i]], f, indent = 4, ensure_ascii = False)