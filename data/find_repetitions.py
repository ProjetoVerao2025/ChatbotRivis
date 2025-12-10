import unicodedata, json, os

'''recebe uma string e retorna a mesma string sem acentuacoes'''
def remover_acentos(texto) -> str:
    forma_normalizada = unicodedata.normalize('NFKD', texto)
    texto_sem_acentos = "".join([c for c in forma_normalizada if unicodedata.category(c) != 'Mn'])
    return texto_sem_acentos

"""Funcao que trata os inputs inconsistentes de comida e retorna uma lista de elementos daquela categoria de comida presentes na string"""
def splitter(str) -> list:
    if (str == "RU" or str == "RS" or str == "RA" or str == "HC"): return None
    resultado = []
    if '(' and ')' not in str:
        resultado.append(str.strip())
        return resultado
    bracket = False
    object = ''
    prevprevprev = None
    prevprev = None
    prev = None
    for char in str:
        prevprevprev = prevprev
        prevprev = prev
        prev = char
        if char == ')':
            bracket = False
            resultado.append(object.strip())
            object = ''
            continue
        if bracket:
            continue
        if char.isalpha() or char == ' ':
            if prev == 'E' and prevprev == ' ' and prevprevprev == ')':
                continue
            else:
                object += char
        if char == '(':
            bracket = True
            continue
    return resultado

proteina = []
guarnicao = []
salada = [] 
sobremesa = []
refresco = []

files = {'proteina.json': proteina, 'guarnicao.json': guarnicao, 'salada.json': salada, 'sobremesas.json': sobremesa, 'refrescos.json':refresco}

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_raiz = os.path.dirname(diretorio_atual)

for file,dish_type in files.items():
    caminho_arquivo = os.path.join(diretorio_raiz + '/bot_chatrivis', file)
    if caminho_arquivo:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dish_type = json.load(f)
            new_values = []
            for item in dish_type:
                item = remover_acentos(item)
                lista_outputs = splitter(item)
                if (lista_outputs == None):
                    continue
                for itens in lista_outputs:
                    new_values.append(itens)
            if file == 'guarnicao.json':
                for i in range(len(new_values)):
                    item = new_values[i]
                    if item.startswith("ABOBRINHA"):
                        new_values[i] = "ABOBRINHA"
                    elif item.startswith("ABOBORA"):
                        new_values[i] = "ABOBORA"
                    elif item.startswith("ACELGA"):
                        new_values[i] = "ACELGA"
                    elif item.startswith("ANGU"):
                        new_values[i] = "ANGU"
                    elif item.startswith("ARROZ"):
                        new_values[i] = 'ARROZ ESPECIAL'
                    elif item.startswith("BATATA") and item != "BATATA PALHA":
                        new_values[i] = "BATATA"
                    elif item.startswith("BETERRABA"):
                        new_values[i] = "BETERRABA"
                    elif item.startswith("CENOURA"):
                        new_values[i] = "CENOURA"
                    elif item.startswith("COUVE"):
                        new_values[i] = "COUVE"
                    elif item.startswith("CUZCUZ"):
                        new_values[i] = "CUZCUZ"
                    elif item.startswith("ESCAROLA"):
                        new_values[i] = "ESCAROLA"
                    elif item.startswith("FAROFA"):
                        new_values[i] = "FAROFA"
                    elif item.startswith("JARDINEIRA"):
                        new_values[i] = "JARDINEIRA"
                    elif item.startswith("LEGUMES"):
                        new_values[i] = "LEGUMES"
                    elif item.startswith("MACARRAO"):
                        new_values[i] = "MACARRAO"
                    elif item.startswith("MANDIOQUINHA"):
                        new_values[i] = "MANDIOQUINHA"
                    elif item.startswith("REPOLHO"):
                        new_values[i] = "REPOLHO"
                    else:
                        new_values[i] = "ARROZ ESPECIAL"
            elif file == 'proteina.json':
                for i in range(len(new_values)):
                    item = new_values[i]
                    if item.startswith("ALMONDEGA"):
                        new_values[i] = "ALMONDEGA"
                    elif item.startswith("BIFE"):
                        new_values[i] = "BIFE"
                    elif item.startswith("BISTECA"):
                        new_values[i] = "BISTECA"
                    elif item.startswith("CARNE"):
                        new_values[i] = "CARNE"
                    elif item.startswith("CUBOS BOVINO"):
                        new_values[i] = "CUBOS BOVINO"
                    elif item.startswith("CUBOS DE CARNE"):
                        new_values[i] = "CUBOS DE CARNE"
                    elif item.startswith("CUBOS DE FRANGO"):
                        new_values[i] = "CUBOS DE FRANGO"
                    elif item.startswith("CUBOS SUINOS"):
                        new_values[i] = "CUBOS SUINOS"
                    elif item.startswith("FILEZINHO"):
                        new_values[i] = "FILE DE FRANGO"
                    elif item.startswith("FILE DE FRANGO"):
                        new_values[i] = "FILE DE FRANGO"
                    elif item.startswith("FILE DE PEIXE"):
                        new_values[i] = "PEIXE"
                    elif item.startswith("FILE DE TILAPIA"):
                        new_values[i] = "PEIXE"
                    elif item.startswith("FRANGO"):
                        new_values[i] = "FRANGO"
                    elif item.startswith("FRICASSE"):
                        new_values[i] = "FRICASSE"
                    elif item.startswith("FRITADA AMERICANA"):
                        new_values[i] = "FRITADA AMERICANA"
                    elif item.startswith("GOULASH"):
                        new_values[i] = "GOULASH"
                    elif item.startswith("GUIZADO"):
                        new_values[i] = "GUIZADO"
                    elif item.startswith("ISCA BOVINA"):
                        new_values[i] = "ISCA BOVINA"
                    elif item.startswith("ISCA DE FRANGO"):
                        new_values[i] = "ISCA DE FRANGO"
                    elif item.startswith("ISCAS BOVINAS"):
                        new_values[i] = "ISCA BOVINA"
                    elif item.startswith("ISCAS DE CARNE"):
                        new_values[i] = "ISCA DE CARNE"
                    elif item.startswith("ISCAS DE FRANGO"):
                        new_values[i] = "ISCA DE FRANGO"
                    elif item.startswith("ISCAS SUINAS"):
                        new_values[i] = "ISCA SUINA"
                    elif item.startswith("LUINGUICA"):
                        new_values[i] = "LINGUICA"
                    elif item.startswith("MOQUECA"):
                        new_values[i] = "PEIXE"
                    elif item.startswith("NUGGETS"):
                        new_values[i] = "NUGGETS"
                    elif item.startswith("PEIXE"):
                        new_values[i] = "PEIXE"
                    elif item.startswith("PESCADA"):
                        new_values[i] = "PEIXE"
                    elif item.startswith("PUCHERO"):
                        new_values[i] = "PUCHERO"
                    elif item.startswith("SOBRECOXA"):
                        new_values[i] = "SOBRECOXA"
                    elif item.startswith("COXA"):
                        new_values[i] = "SOBRECOXA"
                    elif item.startswith("STROGONOFF DE CARNE"):
                        new_values[i] = "STROGONOFF DE CARNE"
                    elif item.startswith("STROGONOFF DE FRANGO"):
                        new_values[i] = "STROGONOFF DE FRANGO"
                    elif item.startswith("TILAPIA"):
                        new_values[i] = "PEIXE"
                    else:
                        new_values[i] = "PEIXE"
            elif file == 'salada.json':
                for i in range(len(new_values)):
                    item = new_values[i]
                    if item.startswith("ACELGA"):
                        new_values[i] = "ACELGA"
                    elif item.startswith("ALFACE"):
                        new_values[i] = "ALFACE"
                    elif item.startswith("ALMEIRAO"):
                        new_values[i] = "ALMEIRAO"
                    elif item.startswith("MIX DE ALFACE"):
                        new_values[i] = "MIX DE ALFACE"
                    elif item.startswith("MIX DE FOLHAS"):
                        new_values[i] = "MIX DE FOLHAS"
                    elif item.startswith("MIX DE REPOLHO"):
                        new_values[i] = "MIX DE REPOLHO"
                    elif item.startswith("PICLES"):
                        new_values[i] = "PICLES"
                    elif item.startswith("REPOLHO"):
                        new_values[i] = "REPOLHO"
                    elif item.startswith("RUCULA"):
                        new_values[i] = "RUCULA"
                    elif item.startswith("SALADA DE ACELGA"):
                        new_values[i] = "SALADA DE ACELGA"
                    elif item.startswith("SALADA DE AGRIAO"):
                        new_values[i] = "SALADA DE AGRIAO"
                    elif item.startswith("SALADA DE ALFACE"):
                        new_values[i] = "SALADA DE ALFACE"
                    elif item.startswith("SALADA DE ALMEIRAO"):
                        new_values[i] = "SALADA DE ALMEIRAO"
                    elif item.startswith("SALADA DE BETERRABA"):
                        new_values[i] = "SALADA DE BETERRABA"
                    elif item.startswith("SALADA DE CENOURA"):
                        new_values[i] = "SALADA DE CENOURA"
                    elif item.startswith("SALADA DE CHICORIA"):
                        new_values[i] = "SALADA DE CHICORIA"
                    elif item.startswith("SALADA DE COUVE"):
                        new_values[i] = "SALADA DE COUVE"
                    elif item.startswith("SALADA DE ESCAROLA"):
                        new_values[i] = "SALADA DE ESCAROLA"
                    elif item.startswith("SALADA DE PEPINO"):
                        new_values[i] = "SALADA DE PEPINO"
                    elif item.startswith("SALADA DE RABANETE"):
                        new_values[i] = "SALADA DE RABANETE"
                    elif item.startswith("SALADA DE REPOLHO"):
                        new_values[i] = "SALADA DE REPOLHO"
                    elif item.startswith("SALADA DE RUCULA"):
                        new_values[i] = "SALADA DE RUCULA"
                    elif item.startswith("SALADA DE SOJA"):
                        new_values[i] = "SALADA DE SOJA"
                    elif item.startswith("SALADA DE TABULE"):
                        new_values[i] = "SALADA DE TABULE"
                    elif item.startswith("SALADA DE TOMATE"):
                        new_values[i] = "SALADA DE TOMATE"
                    else:
                        new_values[i] = "SALADA DE TOMATE"
            elif file == 'sobremesas.json':
                for i in range(len(new_values)):
                    item = new_values[i]
                    if item.startswith("BANANA"):
                        new_values[i] = "BANANA"
                    elif item.startswith("ABACAXI EM CALDA"):
                        new_values[i] = "ABACAXI EM CALDA"
                    elif item.startswith("BARRA DE"):
                        new_values[i] = "BARRA DE CEREAL"
                    elif item.startswith("LARANJA"):
                        new_values[i] = "LARANJA"
                    elif item.startswith("DOCE DE ABOBORA"):
                        new_values[i] = "DOCE DE ABOBORA"
                    elif item.startswith("DOCE DE BANANA"):
                        new_values[i] = "DOCE DE BANANA"
                    elif item.startswith("DOCE DE FIGO EM CALDA"):
                        new_values[i] = "FIGO EM CALDA"
                    elif item.startswith("FIGO DE CALDA"):
                        new_values[i] = "FIGO EM CALDA"
                    elif item.startswith("DOCE DE GOI"):
                        new_values[i] = "DOCE DE GOIABA"
                    elif item.startswith("GOIABADA"):
                        new_values[i] = "GOIABADA"
                    elif item.startswith("MACA"):
                        new_values[i] = "MACA"
                    elif item.startswith("MELANCIA"):
                        new_values[i] = "MELANCIA"
                    elif item.startswith("MELAO"):
                        new_values[i] = "MELAO"
                    elif item.startswith("MURCOTE"):
                        new_values[i] = "TANGERINA"
                    elif item.startswith("SAGU DE MARACUJA"):
                        new_values[i] = "SAGU DE MARACUJA"
                    elif item.startswith("SAGU DE UVA"):
                        new_values[i] = "SAGU DE UVA"
                    elif item.startswith("TANGERINA"):
                        new_values[i] = "TANGERINA"
                    else:
                        new_values[i] = "BANANA"
            elif file == 'refrescos.json':
                for i in range(len(new_values)):
                    item = new_values[i]
                    if item.startswith("REFRESCO"):
                        continue
                    else:
                        new_values[i] = "REFRESCO DE UVA"
            new_values = set(new_values)
            new_values = sorted(list(new_values))

        with open(caminho_arquivo, "w", encoding='utf-8') as f:
            json.dump(new_values, f, indent=4, ensure_ascii=False)