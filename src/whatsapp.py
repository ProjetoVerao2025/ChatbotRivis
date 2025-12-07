# codigo para enviar a mensagem formatada 

# codigo para enviar a mensagem formatada

import json
from pywhatkit import sendwhatmsg_to_group
from random import choice
from datetime import date

def excessoes(comida: str, code: int, h: int, m: int):
    # code 0 representa almoço, 1 é janta
    chave = "almoco"
    if code == 1:
        chave = "jantar"
        
    if ref[diAtual]["almoco"]["proteina"][:5] == "PEIXE":
        sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["proteina"]["peixe"])}""", h, m, 10)
    elif ref[diAtual]["almoco"]["proteina"][:8] == "FEIJOADA":
        sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["proteina"]["feijoada"])}""", h, m, 10)
    elif ref[diAtual]["almoco"]["proteina"][:9] == "SOBRECOXA":
        sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["proteina"]["sobrecoxa"])}""", h, m, 10)
    elif ref[diAtual]["almoco"]["proteina"][:6] == "NUGGET":
        sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["proteina"]["nugget"])}""", h, m, 10)
    elif ref[diAtual]["almoco"]["guarnicao"][:8] == "MACARRÃO":
        sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["guarnicao"]["macarrao"])}""", h, m, 10)
    elif ref[diAtual]["almoco"]["suco"][12:] == "MANGA":
        sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["refresco"]["manga"])}""", h, m, 10)
    elif ref[diAtual]["almoco"]["suco"][12:] == "LIMÃO":
        sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["refresco"]["limao"])}""", h, m, 10)
    elif ref[diAtual]["almoco"]["proteina"][:7] == "LARANJA":
        sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["sobremesa"]["laranja"])}""", h, m, 10)
    elif ref[diAtual]["almoco"]["proteina"][:7] == "MELANCIA":
        sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["sobremesa"]["melancia"])}""", h, m, 10)

def enviarRef(comida: str, code: int, h: int, m: int):
    if code == 0: # code 0 representa almoço, 1 é janta
        sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{comida}""", h, m, 10)
        return
    sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{comida}""", h, m, 10)

diAtual = date.today().isoformat()  #classe data do datetime que tem o método today, isoformat é o formato da data na chave do dict
with open("../weekly-quotes.json", "r", encoding= "utf8") as f: #abrir arquivo padrão
    msgs = json.load(f)

with open("../weekly-data.json", "r", encoding= "utf8") as f:
    ref = json.load(f)

enviarRef(f"""{ref[diAtual]["almoco"]}""", 0, 10, 0)
excessoes(f"""{ref[diAtual]["almoco"]}""", 0, 10, 0)
try:
    enviarRef(f"""{ref[diAtual]["jantar"]}""", 1, 15, 0)
    excessoes(f"""{ref[diAtual]["jantar"]}""", 1, 15, 5)

#Domingo e feriados não tem janta
except KeyError:
    pass