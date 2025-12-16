# codigo para enviar a mensagem formatada 

import json
import os
from random import choice
from datetime import date, datetime
from urllib.parse import quote
import selenium.webdriver as wb
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
import time
from config import config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_msg(meal: dict, classification: dict, msg_dict: dict, msg: str = ""):
    """
    meal: dict -> Refeição do dia.
    classification: dict -> Dicionário que classifica as refeições.
    msg_dict: dict -> Dicionário das mensagens.
    msg: str -> String adicionada no início de toda mensagem. 
    """
    proteina = meal["proteina"]
    guarnicao = meal["guarnicao"]
    salada = meal["salada"]
    sobremesa = meal["sobremesa"]
    suco = meal["suco"]

    proteina_msg = list(choice(msg_dict["proteina"][classification["proteina"]])[:])
    guarnicao_msg = list(choice(msg_dict["guarnicao"][classification["guarnicao"]])[:])
    salada_msg = list(choice(msg_dict["salada"][classification["salada"]])[:])
    sobremesa_msg = list(choice(msg_dict["sobremesa"][classification["sobremesa"]])[:])
    suco_msg = list(choice(msg_dict["refresco"][classification["suco"]])[:])

    for i in range(len(proteina_msg)):
        if proteina_msg[i] == "_":
            proteina_msg[i:i + 1] = proteina
    proteina_msg = "".join(proteina_msg)

    for i in range(len(guarnicao_msg)):
        if guarnicao_msg[i] == "_":
            guarnicao_msg[i:i + 1] = guarnicao
    guarnicao_msg = "".join(guarnicao_msg)

    for i in range(len(salada_msg)):
        if salada_msg[i] == "_":
            salada_msg[i:i + 1] = salada
    salada_msg = "".join(salada_msg)

    for i in range(len(sobremesa_msg)):
        if sobremesa_msg[i] == "_":
            sobremesa_msg[i:i + 1] = sobremesa
    sobremesa_msg = "".join(sobremesa_msg)

    for i in range(len(suco_msg)):
        if suco_msg[i] == "_":
            suco_msg[i:i + 1] = suco.split()[2]
    suco_msg = "".join(suco_msg)
    
    return msg + proteina_msg + guarnicao_msg + salada_msg + sobremesa_msg + suco_msg



def wait_for_element(driver, xpath, retries=10, delay=2):
    for i in range(retries):
        try:
            return driver.find_element(By.XPATH, xpath)
        except:
            time.sleep(delay)
    raise Exception(f"Elemento não encontrado para o XPath: {xpath}")


def select_group(driver, group_name: str):
    wait = WebDriverWait(driver, 10)

    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')),
        search_box.click(),
        search_box.clear(),
        search_box.send_keys(group_name)
        )

    group = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f'//span[@title="{group_name}"]')
        )
    )
    group.click()

def wait_for_element(driver, locator, retries=10, delay=2):
    """
    Helper to wait for elements with a custom retry loop if needed, 
    though WebDriverWait is generally preferred.
    """
    wait = WebDriverWait(driver, delay)
    for i in range(retries):
        try:
            return wait.until(EC.presence_of_element_located(locator))
        except:
            pass
    raise Exception(f"Elemento não encontrado: {locator}")

def send_msg_via_url(driver, msg: str, group_name: str):
    wait = WebDriverWait(driver, 5)

    encoded_msg = quote(msg)
    driver.get(f"https://web.whatsapp.com/send?text={encoded_msg}")

    search_box = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@contenteditable='true']"))
    )
    
    search_box.click()
    search_box.clear()
    search_box.send_keys(group_name)
    time.sleep(1.5)

    try:
        xpath_group = f"//span[@title='{group_name}']"
        group_item = wait.until(EC.presence_of_element_located((By.XPATH, xpath_group)))
        
        try:
            group_item.click()
        except:
            driver.execute_script("arguments[0].click();", group_item)
            
        print("Grupo selecionado.")
    except Exception as e:
        raise Exception(f"Não foi possível encontrar ou clicar no grupo '{group_name}'. Erro: {e}")


    forward_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="wds-ic-send-filled"]')))
    driver.execute_script("arguments[0].click();", forward_btn)
    
    time.sleep(3)

    print("Entrou na tela de mensagem do grupo")
    send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[.//span[@data-icon="wds-ic-send-filled"]]')))
    driver.execute_script("arguments[0].click();", send_btn)
    time.sleep(10)
    print("Mensagem enviada com sucesso.")

def send_msg(msg: str):
    options = Options()
    options.add_argument(f"user-data-dir={config.chrome_dir}")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--headless") # Uncomment if you don't want to see the browser
    
    driver = wb.Chrome(options=options)
    
    try:
        driver.get("https://web.whatsapp.com/")
        load_cookies(driver)
        driver.refresh()

        # Check login status
        wait = WebDriverWait(driver, 20)
        try:
            # Wait for the main side panel to ensure we are logged in
            wait.until(EC.presence_of_element_located((By.ID, "side")))
        except:
            print("WhatsApp não está logado ou demorou para carregar. Verifique o QR Code.")
            # Allow manual login time if needed
            WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.ID, "side"))
            )
            # Save new cookies after manual login
            pickle.dump(driver.get_cookies(), open('.cookies.pkl', 'wb'))

        # Perform the sending logic
        # We assume the group name is "TCN" based on your original code
        # Ideally, move "TCN" to your Config file
        send_msg_via_url(driver, msg, "TCN") 

    except Exception as e:
        print(f"Erro Fatal: {e}")
    finally:
        # Save cookies and close
        try:
            pickle.dump(driver.get_cookies(), open('.cookies.pkl', 'wb'))
        except:
            pass
        driver.quit()


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


def get_quality(meal: dict, classification: dict):
    quality = {
        "proteina": "neutro",
        "guarnicao": "neutro",
        "salada": "neutro",
        "sobremesa": "neutro",
        "suco": "neutro"
    }
    
    proteina = meal["proteina"]
    guarnicao = meal["guarnicao"]
    salada = meal["salada"]
    sobremesa = meal["sobremesa"]
    suco = meal["suco"]

    proteina_simplificado = simplify_proteina(proteina)
    if proteina_simplificado in classification["proteina"]:
        quality["proteina"] = classification["proteina"][proteina_simplificado]

    guarnicao_simplificado = simplify_guarnicao(guarnicao)
    if guarnicao_simplificado in classification["guarnicao"]:
        quality["guarnicao"] = classification["guarnicao"][guarnicao_simplificado]

    salada_simplificado = simplify_salada(salada)
    if salada_simplificado in classification["salada"]:
        quality["salada"] = classification["salada"][salada_simplificado]
    
    sobremesa_simplificado = simplify_sobremesa(sobremesa)
    if sobremesa_simplificado in classification["sobremesa"]:
        quality["sobremesa"] = classification["sobremesa"][sobremesa_simplificado]
    
    if suco in classification["suco"]:
        quality["suco"] = classification["suco"][suco]

    return quality


def simplify_proteina(item: str):
    if item.startswith("ALMONDEGA"):
        return "ALMONDEGA"
    elif item.startswith("BIFE"):
        return "BIFE"
    elif item.startswith("BISTECA"):
        return "BISTECA"
    elif item.startswith("CARNE"):
        return "CARNE"
    elif item.startswith("CUBOS BOVINO"):
        return "CUBOS BOVINO"
    elif item.startswith("CUBOS DE CARNE"):
        return "CUBOS DE CARNE"
    elif item.startswith("CUBOS DE FRANGO"):
        return "CUBOS DE FRANGO"
    elif item.startswith("CUBOS SUINOS"):
        return "CUBOS SUINOS"
    elif item.startswith("FILEZINHO"):
        return "FILE DE FRANGO"
    elif item.startswith("FILE DE FRANGO"):
        return "FILE DE FRANGO"
    elif item.startswith("FILE DE PEIXE"):
        return "PEIXE"
    elif item.startswith("FILE DE TILAPIA"):
        return "PEIXE"
    elif item.startswith("FRANGO"):
        return "FRANGO"
    elif item.startswith("FRICASSE"):
        return "FRICASSE"
    elif item.startswith("FRITADA AMERICANA"):
        return "FRITADA AMERICANA"
    elif item.startswith("GOULASH"):
        return "GOULASH"
    elif item.startswith("GUIZADO"):
        return "GUIZADO"
    elif item.startswith("ISCA BOVINA"):
        return "ISCA BOVINA"
    elif item.startswith("ISCA DE FRANGO"):
        return "ISCA DE FRANGO"
    elif item.startswith("ISCAS BOVINAS"):
        return "ISCA BOVINA"
    elif item.startswith("ISCAS DE CARNE"):
        return "ISCA DE CARNE"
    elif item.startswith("ISCAS DE FRANGO"):
        return "ISCA DE FRANGO"
    elif item.startswith("ISCAS SUINAS"):
        return "ISCA SUINA"
    elif item.startswith("LUINGUICA"):
        return "LINGUICA"
    elif item.startswith("MOQUECA"):
        return "PEIXE"
    elif item.startswith("NUGGETS"):
        return "NUGGETS"
    elif item.startswith("PEIXE"):
        return "PEIXE"
    elif item.startswith("PESCADA"):
        return "PEIXE"
    elif item.startswith("PUCHERO"):
        return "PUCHERO"
    elif item.startswith("SOBRECOXA"):
        return "SOBRECOXA"
    elif item.startswith("COXA"):
        return "SOBRECOXA"
    elif item.startswith("STROGONOFF DE CARNE"):
        return "STROGONOFF DE CARNE"
    elif item.startswith("STROGONOFF DE FRANGO"):
        return "STROGONOFF DE FRANGO"
    elif item.startswith("TILAPIA"):
        return "PEIXE"
    else:
        return "NEUTRO"
def simplify_guarnicao(item: str):
    if item.startswith("ABOBRINHA"):
        return "ABOBRINHA"
    elif item.startswith("ABOBORA"):
        return "ABOBORA"
    elif item.startswith("ACELGA"):
        return "ACELGA"
    elif item.startswith("ANGU"):
        return "ANGU"
    elif item.startswith("ARROZ"):
        return 'ARROZ ESPECIAL'
    elif item.startswith("BATATA PALHA"):
        return "BATATA PALHA"
    elif item.startswith("BATATA"):
        return "BATATA"
    elif item.startswith("BETERRABA"):
        return "BETERRABA"
    elif item.startswith("CENOURA"):
        return "CENOURA"
    elif item.startswith("COUVE"):
        return "COUVE"
    elif item.startswith("CUZCUZ"):
        return "CUZCUZ"
    elif item.startswith("ESCAROLA"):
        return "ESCAROLA"
    elif item.startswith("FAROFA"):
        return "FAROFA"
    elif item.startswith("JARDINEIRA"):
        return "JARDINEIRA"
    elif item.startswith("LEGUMES"):
        return "LEGUMES"
    elif item.startswith("MACARRAO"):
        return "MACARRAO"
    elif item.startswith("MANDIOQUINHA"):
        return "MANDIOQUINHA"
    elif item.startswith("REPOLHO"):
        return "REPOLHO"
    elif item.startswith("ARROZ"):
        return "ARROZ ESPECIAL"
    else:
        return "NEUTRO"
def simplify_salada(item: str):
    if item.startswith("ACELGA"):
        return "ACELGA"
    elif item.startswith("ALFACE"):
        return "ALFACE"
    elif item.startswith("ALMEIRAO"):
        return "ALMEIRAO"
    elif item.startswith("MIX DE ALFACE"):
        return "MIX DE ALFACE"
    elif item.startswith("MIX DE FOLHAS"):
        return "MIX DE FOLHAS"
    elif item.startswith("MIX DE REPOLHO"):
        return "MIX DE REPOLHO"
    elif item.startswith("PICLES"):
        return "PICLES"
    elif item.startswith("REPOLHO"):
        return "REPOLHO"
    elif item.startswith("RUCULA"):
        return "RUCULA"
    elif item.startswith("SALADA DE ACELGA"):
        return "SALADA DE ACELGA"
    elif item.startswith("SALADA DE AGRIAO"):
        return "SALADA DE AGRIAO"
    elif item.startswith("SALADA DE ALFACE"):
        return "SALADA DE ALFACE"
    elif item.startswith("SALADA DE ALMEIRAO"):
        return "SALADA DE ALMEIRAO"
    elif item.startswith("SALADA DE BETERRABA"):
        return "SALADA DE BETERRABA"
    elif item.startswith("SALADA DE CENOURA"):
        return "SALADA DE CENOURA"
    elif item.startswith("SALADA DE CHICORIA"):
        return "SALADA DE CHICORIA"
    elif item.startswith("SALADA DE COUVE"):
        return "SALADA DE COUVE"
    elif item.startswith("SALADA DE ESCAROLA"):
        return "SALADA DE ESCAROLA"
    elif item.startswith("SALADA DE PEPINO"):
        return "SALADA DE PEPINO"
    elif item.startswith("SALADA DE RABANETE"):
        return "SALADA DE RABANETE"
    elif item.startswith("SALADA DE REPOLHO"):
        return "SALADA DE REPOLHO"
    elif item.startswith("SALADA DE RUCULA"):
        return "SALADA DE RUCULA"
    elif item.startswith("SALADA DE SOJA"):
        return "SALADA DE SOJA"
    elif item.startswith("SALADA DE TABULE"):
        return "SALADA DE TABULE"
    elif item.startswith("SALADA DE TOMATE"):
        return "SALADA DE TOMATE"
    else:
        return "NEUTRO"
def simplify_sobremesa(item: str):
    if item.startswith("BANANA"):
        return "BANANA"
    elif item.startswith("ABACAXI EM CALDA"):
        return "ABACAXI EM CALDA"
    elif item.startswith("BARRA DE"):
        return "BARRA DE CEREAL"
    elif item.startswith("LARANJA"):
        return "LARANJA"
    elif item.startswith("DOCE DE ABOBORA"):
        return "DOCE DE ABOBORA"
    elif item.startswith("DOCE DE BANANA"):
        return "DOCE DE BANANA"
    elif item.startswith("DOCE DE FIGO EM CALDA"):
        return "FIGO EM CALDA"
    elif item.startswith("FIGO DE CALDA"):
        return "FIGO EM CALDA"
    elif item.startswith("DOCE DE GOI"):
        return "DOCE DE GOIABA"
    elif item.startswith("GOIABADA"):
        return "GOIABADA"
    elif item.startswith("MACA"):
        return "MACA"
    elif item.startswith("MELANCIA"):
        return "MELANCIA"
    elif item.startswith("MELAO"):
        return "MELAO"
    elif item.startswith("MURCOTE"):
        return "TANGERINA"
    elif item.startswith("SAGU DE MARACUJA"):
        return "SAGU DE MARACUJA"
    elif item.startswith("SAGU DE UVA"):
        return "SAGU DE UVA"
    elif item.startswith("TANGERINA"):
        return "TANGERINA"
    else:
        return "BANANA"

def send():
    #if datetime.now().day == "sunday"
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_raiz = os.path.dirname(diretorio_atual)
    caminho_arquivo = os.path.join(diretorio_raiz, config.week_meals_file)

    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        meal = json.load(file)[str(date.today())]
        time = "almoco" if datetime.now().hour < 15 else "jantar"
        if time in meal:
            meal = meal[time]["RU"]
        else:
            return -1


    caminho_arquivo = os.path.join(diretorio_raiz, config.msgs)
    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        msgs = json.load(file)

    caminho_arquivo = os.path.join(diretorio_raiz, config.relationships)
    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        classification = json.load(file)
    
    quality = get_quality(meal, classification)
    msg = create_msg(meal, quality, msgs)
    send_msg(msg)
    return

if (__name__ == "__main__"):
    send()
