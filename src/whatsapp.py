# codigo para enviar a mensagem formatada 

# codigo para enviar a mensagem formatada

import json
from pywhatkit import sendwhatmsg_to_group
from random import choice
from datetime import date
from urllib.parse import quote
import selenium.webdriver as wb
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
import time

def create_msg(refeição: dict, classing: dict, msg_dict: dict):
    msg = ""
    
    proteina = refeição["proteina"]
    guarnicao = refeição["guarnicao"]
    salada = refeição["salada"]
    sobremesa = refeição["sobremesa"]["RU"]
    suco = refeição["suco"]

    proteina_msg = choice(msg_dict[classing[proteina]])[:]
    guarnicao_msg =  choice(msg_dict[classing[guarnicao]])[:]
    salada_msg =  choice(msg_dict[classing[salada]])[:]
    sobremesa_msg =  choice(msg_dict[classing[sobremesa]])[:]
    suco_msg =  choice(msg_dict[classing[suco]])[:]

    for i in range(len(proteina_msg)):
        if proteina_msg[i] == "_":
            proteina_msg[i:i + 1] = proteina

    for i in range(len(guarnicao_msg)):
        if guarnicao_msg[i] == "_":
            guarnicao_msg[i:i + 1] = guarnicao

    for i in range(len(salada_msg)):
        if salada_msg[i] == "_":
            salada_msg[i:i + 1] = salada

    for i in range(len(sobremesa_msg)):
        if sobremesa_msg[i] == "_":
            sobremesa_msg[i:i + 1] = sobremesa
    
    for i in range(len(suco_msg)):
        if suco_msg[i] == "_":
            suco_msg[i:i + 1] = suco
    
    return quote(msg + proteina_msg + guarnicao_msg + salada_msg + sobremesa_msg + suco_msg)

def send_msg(msg: str):
    
    options = Options()
    options.add_argument("user-data-dir=C:\\Users\\Bernardo\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    driver = wb.Chrome(options=options)
    driver.get(f"https://web.whatsapp.com/")
    load_cookies(driver)
    driver.get(f"https://web.whatsapp.com/send?&text={quote("victor viado")}")
    aa = True
    while aa:
        try:
            box = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/span[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div[2]/div/div[2]')
            aa = False
        except:
            pass
    box.click()
    
    bb = True
    while bb:
        try:
            forward_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/span[2]/div/div/div/div/div/div/div/span/div/div/div')
            bb = False
        except:
            pass
    time.sleep(2)
    forward_button.click()

    cc = True
    while cc:
        try:
            send_button = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[4]/div/span/button')
            cc = False
        except:
            pass
    time.sleep(2)
    send_button.click()
    time.sleep(2)
    save_and_exit(driver)

def load_cookies(driver):
    try:
        cookies = pickle.load(open('.cookies.pkl', 'rb'))
        for cookie in cookies:
            driver.add_cookie(cookie)
    except Exception:
        pass

def save_and_exit(driver):
    pickle.dump(driver.get_cookies(), open('.cookies.pkl', 'wb'))
    driver.close()
    exit()

# def excessoes(comida: str, code: int, h: int, m: int):
#     # code 0 representa almoço, 1 é janta
#     chave = "almoco"
#     if code == 1:
#         chave = "jantar"
        
#     if ref[diAtual]["almoco"]["proteina"][:5] == "PEIXE":
#         sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["proteina"]["peixe"])}""", h, m, 10)
#     elif ref[diAtual]["almoco"]["proteina"][:8] == "FEIJOADA":
#         sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["proteina"]["feijoada"])}""", h, m, 10)
#     elif ref[diAtual]["almoco"]["proteina"][:9] == "SOBRECOXA":
#         sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["proteina"]["sobrecoxa"])}""", h, m, 10)
#     elif ref[diAtual]["almoco"]["proteina"][:6] == "NUGGET":
#         sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["proteina"]["nugget"])}""", h, m, 10)
#     elif ref[diAtual]["almoco"]["guarnicao"][:8] == "MACARRÃO":
#         sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["guarnicao"]["macarrao"])}""", h, m, 10)
#     elif ref[diAtual]["almoco"]["suco"][12:] == "MANGA":
#         sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["refresco"]["manga"])}""", h, m, 10)
#     elif ref[diAtual]["almoco"]["suco"][12:] == "LIMÃO":
#         sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["refresco"]["limao"])}""", h, m, 10)
#     elif ref[diAtual]["almoco"]["proteina"][:7] == "LARANJA":
#         sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["sobremesa"]["laranja"])}""", h, m, 10)
#     elif ref[diAtual]["almoco"]["proteina"][:7] == "MELANCIA":
        # sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{choice(msgs["sobremesa"]["melancia"])}""", h, m, 10)

def enviarRef(comida: str, code: int, h: int, m: int):
    if code == 0: # code 0 representa almoço, 1 é janta
        sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{comida}""", h, m, 10)
        return
    sendwhatmsg_to_group("BmrEqCXJkUTHlEiZhCifUD", f"""{comida}""", h, m, 10)

# diAtual = date.today().isoformat()  #classe data do datetime que tem o método today, isoformat é o formato da data na chave do dict
# with open("../weekly-quotes.json", "r", encoding= "utf8") as f: #abrir arquivo padrão
#     msgs = json.load(f)

# with open("../weekly-data.json", "r", encoding= "utf8") as f:
#     ref = json.load(f)

# enviarRef(f"""{ref[diAtual]["almoco"]}""", 0, 10, 0)
# excessoes(f"""{ref[diAtual]["almoco"]}""", 0, 10, 0)
# try:
#     enviarRef(f"""{ref[diAtual]["jantar"]}""", 1, 15, 0)
#     excessoes(f"""{ref[diAtual]["jantar"]}""", 1, 15, 5)

# #Domingo e feriados não tem janta
# except KeyError:
#     pass

send_msg("msg")