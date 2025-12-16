import json
import os
import base64
from random import choice
from datetime import date, datetime
from urllib.parse import quote
import selenium.webdriver as wb
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
import time
from src.config import config  # Certifique-se de que este arquivo existe
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from PIL import Image
from pyzbar.pyzbar import decode
import qrcode
from io import BytesIO
from selenium.webdriver.common.keys import Keys


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

def create_msg(meal: dict, classification: dict, msg_dict: dict, msg: str = ""):
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

def simplify_proteina(item: str):
    if item.startswith("ALMONDEGA"): return "ALMONDEGA"
    elif item.startswith("BIFE"): return "BIFE"
    elif item.startswith("BISTECA"): return "BISTECA"
    elif item.startswith("CARNE"): return "CARNE"
    elif item.startswith("CUBOS BOVINO"): return "CUBOS BOVINO"
    elif item.startswith("CUBOS DE CARNE"): return "CUBOS DE CARNE"
    elif item.startswith("CUBOS DE FRANGO"): return "CUBOS DE FRANGO"
    elif item.startswith("CUBOS SUINOS"): return "CUBOS SUINOS"
    elif item.startswith("FILEZINHO"): return "FILE DE FRANGO"
    elif item.startswith("FILE DE FRANGO"): return "FILE DE FRANGO"
    elif item.startswith("FILE DE PEIXE"): return "PEIXE"
    elif item.startswith("FILE DE TILAPIA"): return "PEIXE"
    elif item.startswith("FRANGO"): return "FRANGO"
    elif item.startswith("FRICASSE"): return "FRICASSE"
    elif item.startswith("FRITADA AMERICANA"): return "FRITADA AMERICANA"
    elif item.startswith("GOULASH"): return "GOULASH"
    elif item.startswith("GUIZADO"): return "GUIZADO"
    elif item.startswith("ISCA BOVINA"): return "ISCA BOVINA"
    elif item.startswith("ISCA DE FRANGO"): return "ISCA DE FRANGO"
    elif item.startswith("ISCAS BOVINAS"): return "ISCA BOVINA"
    elif item.startswith("ISCAS DE CARNE"): return "ISCA DE CARNE"
    elif item.startswith("ISCAS DE FRANGO"): return "ISCA DE FRANGO"
    elif item.startswith("ISCAS SUINAS"): return "ISCA SUINA"
    elif item.startswith("LUINGUICA"): return "LINGUICA"
    elif item.startswith("MOQUECA"): return "PEIXE"
    elif item.startswith("NUGGETS"): return "NUGGETS"
    elif item.startswith("PEIXE"): return "PEIXE"
    elif item.startswith("PESCADA"): return "PEIXE"
    elif item.startswith("PUCHERO"): return "PUCHERO"
    elif item.startswith("SOBRECOXA"): return "SOBRECOXA"
    elif item.startswith("COXA"): return "SOBRECOXA"
    elif item.startswith("STROGONOFF DE CARNE"): return "STROGONOFF DE CARNE"
    elif item.startswith("STROGONOFF DE FRANGO"): return "STROGONOFF DE FRANGO"
    elif item.startswith("TILAPIA"): return "PEIXE"
    else: return "NEUTRO"

def simplify_guarnicao(item: str):
    if item.startswith("ABOBRINHA"): return "ABOBRINHA"
    elif item.startswith("ABOBORA"): return "ABOBORA"
    elif item.startswith("ACELGA"): return "ACELGA"
    elif item.startswith("ANGU"): return "ANGU"
    elif item.startswith("ARROZ"): return 'ARROZ ESPECIAL'
    elif item.startswith("BATATA PALHA"): return "BATATA PALHA"
    elif item.startswith("BATATA"): return "BATATA"
    elif item.startswith("BETERRABA"): return "BETERRABA"
    elif item.startswith("CENOURA"): return "CENOURA"
    elif item.startswith("COUVE"): return "COUVE"
    elif item.startswith("CUZCUZ"): return "CUZCUZ"
    elif item.startswith("ESCAROLA"): return "ESCAROLA"
    elif item.startswith("FAROFA"): return "FAROFA"
    elif item.startswith("JARDINEIRA"): return "JARDINEIRA"
    elif item.startswith("LEGUMES"): return "LEGUMES"
    elif item.startswith("MACARRAO"): return "MACARRAO"
    elif item.startswith("MANDIOQUINHA"): return "MANDIOQUINHA"
    elif item.startswith("REPOLHO"): return "REPOLHO"
    else: return "NEUTRO"

def simplify_salada(item: str):
    if item.startswith("ACELGA"): return "ACELGA"
    elif item.startswith("ALFACE"): return "ALFACE"
    elif item.startswith("ALMEIRAO"): return "ALMEIRAO"
    elif item.startswith("MIX DE ALFACE"): return "MIX DE ALFACE"
    elif item.startswith("MIX DE FOLHAS"): return "MIX DE FOLHAS"
    elif item.startswith("MIX DE REPOLHO"): return "MIX DE REPOLHO"
    elif item.startswith("PICLES"): return "PICLES"
    elif item.startswith("REPOLHO"): return "REPOLHO"
    elif item.startswith("RUCULA"): return "RUCULA"
    elif item.startswith("SALADA DE ACELGA"): return "SALADA DE ACELGA"
    elif item.startswith("SALADA DE AGRIAO"): return "SALADA DE AGRIAO"
    elif item.startswith("SALADA DE ALFACE"): return "SALADA DE ALFACE"
    elif item.startswith("SALADA DE ALMEIRAO"): return "SALADA DE ALMEIRAO"
    elif item.startswith("SALADA DE BETERRABA"): return "SALADA DE BETERRABA"
    elif item.startswith("SALADA DE CENOURA"): return "SALADA DE CENOURA"
    elif item.startswith("SALADA DE CHICORIA"): return "SALADA DE CHICORIA"
    elif item.startswith("SALADA DE COUVE"): return "SALADA DE COUVE"
    elif item.startswith("SALADA DE ESCAROLA"): return "SALADA DE ESCAROLA"
    elif item.startswith("SALADA DE PEPINO"): return "SALADA DE PEPINO"
    elif item.startswith("SALADA DE RABANETE"): return "SALADA DE RABANETE"
    elif item.startswith("SALADA DE REPOLHO"): return "SALADA DE REPOLHO"
    elif item.startswith("SALADA DE RUCULA"): return "SALADA DE RUCULA"
    elif item.startswith("SALADA DE SOJA"): return "SALADA DE SOJA"
    elif item.startswith("SALADA DE TABULE"): return "SALADA DE TABULE"
    elif item.startswith("SALADA DE TOMATE"): return "SALADA DE TOMATE"
    else: return "NEUTRO"

def simplify_sobremesa(item: str):
    if item.startswith("BANANA"): return "BANANA"
    elif item.startswith("ABACAXI EM CALDA"): return "ABACAXI EM CALDA"
    elif item.startswith("BARRA DE"): return "BARRA DE CEREAL"
    elif item.startswith("LARANJA"): return "LARANJA"
    elif item.startswith("DOCE DE ABOBORA"): return "DOCE DE ABOBORA"
    elif item.startswith("DOCE DE BANANA"): return "DOCE DE BANANA"
    elif item.startswith("DOCE DE FIGO EM CALDA"): return "FIGO EM CALDA"
    elif item.startswith("FIGO DE CALDA"): return "FIGO EM CALDA"
    elif item.startswith("DOCE DE GOI"): return "DOCE DE GOIABA"
    elif item.startswith("GOIABADA"): return "GOIABADA"
    elif item.startswith("MACA"): return "MACA"
    elif item.startswith("MELANCIA"): return "MELANCIA"
    elif item.startswith("MELAO"): return "MELAO"
    elif item.startswith("MURCOTE"): return "TANGERINA"
    elif item.startswith("SAGU DE MARACUJA"): return "SAGU DE MARACUJA"
    elif item.startswith("SAGU DE UVA"): return "SAGU DE UVA"
    elif item.startswith("TANGERINA"): return "TANGERINA"
    else: return "BANANA"

def print_terminal_qr(driver):
    """
    Retorna a string do QR Code se encontrado.
    Retorna None se não encontrar (o que é bom, significa que logou ou está carregando).
    """
    # 1. Verifica Botão de Recarregar (Correção para Headless)
    try:
        reload_targets = driver.find_elements(By.XPATH, "//button[contains(., 'Recarregar')] | //div[@role='button'][contains(., 'Reload')] | //span[@data-icon='refresh']")
        if reload_targets:
            print("DEBUG: Botão 'Recarregar' detectado. Clicando...")
            driver.execute_script("arguments[0].click();", reload_targets[0])
            time.sleep(3)
            return None
    except:
        pass

    # 2. Tenta ler o Canvas
    try:
        qr_canvas = driver.find_element(By.XPATH, "//div[@data-ref]//canvas")
        
        # Extrai imagem via JS
        canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", qr_canvas)
        png_data = base64.b64decode(canvas_base64)
        img = Image.open(BytesIO(png_data))

        # Borda branca
        border_size = 30
        new_size = (img.size[0] + border_size * 2, img.size[1] + border_size * 2)
        img_with_border = Image.new("RGB", new_size, "white")
        img_with_border.paste(img, (border_size, border_size))

        decoded_objects = decode(img_with_border)
        if not decoded_objects:
            return None

        qr_data = decoded_objects[0].data.decode("utf-8")
        
        # Só imprime se for um dado válido
        if qr_data:
            # Monta o QR para o terminal
            qr = qrcode.QRCode(version=1, border=2)
            qr.add_data(qr_data)
            qr.make(fit=True)

            print("\n" + "="*40)
            print(f"NOVO QR CODE ({datetime.now().strftime('%H:%M:%S')})")
            print("="*40 + "\n")
            qr.print_ascii(invert=True)
            print("\n" + "="*40 + "\n")
            return qr_data
            
    except Exception:
        # Elemento não encontrado (Normal se já tiver escaneado)
        return None
    
    return None


def send_msg_via_url(driver, msg: str, group_name: str):
    print("DEBUG: Iniciando send_msg_via_url...")
    wait = WebDriverWait(driver, 30)

    encoded_msg = quote(msg)
    url = f"https://web.whatsapp.com/send?text={encoded_msg}"
    driver.get(url)

    print("DEBUG: Aguardando caixa de pesquisa do modal...")
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        modal_search_xpath = "//div[@role='dialog']//div[@contenteditable='true']"
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, modal_search_xpath)))
        driver.execute_script("arguments[0].click();", search_box)
        search_box.clear()
        search_box.send_keys(group_name)
        time.sleep(3)
    except Exception as e:
        print(f"DEBUG: Falha ao focar na busca do modal. Erro: {e}")
        raise e

    print(f"DEBUG: Selecionando grupo '{group_name}'...")
    try:
        xpath_group = f"//div[@role='dialog']//span[@title='{group_name}']"
        group_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_group)))
        try:
            row = group_element.find_element(By.XPATH, "./ancestor::div[@role='button'] | ./ancestor::div[@class='_21S-L']")
            driver.execute_script("arguments[0].click();", row)
        except:
            driver.execute_script("arguments[0].click();", group_element)
    except Exception as e:
        raise Exception(f"DEBUG: Grupo não encontrado. {e}")

    time.sleep(2)

    print("DEBUG: Clicando no botão do modal (Encaminhar)...")
    modal_btn_xpath = '//div[@role="dialog"]//span[@data-icon="wds-ic-send-filled"]/ancestor::div[@role="button"] | //div[@role="dialog"]//span[@data-icon="send"]/ancestor::div[@role="button"]'
    try:
        send_btn_modal = wait.until(EC.presence_of_element_located((By.XPATH, modal_btn_xpath)))
        driver.execute_script("arguments[0].click();", send_btn_modal)
    except Exception as e:
        print(f"DEBUG: Erro botão modal ({e}). Tentando ENTER...")
        search_box.send_keys(Keys.ENTER)

    print("DEBUG: Aguardando carregamento do chat principal (10s)...")
    time.sleep(10)

    print("DEBUG: Escaneando rodapé em busca do botão de envio final...")
    try:
        footer = wait.until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
        buttons = footer.find_elements(By.XPATH, ".//button | .//div[@role='button']")
        target_btn = None

        for btn in buttons:
            html = btn.get_attribute('outerHTML')
            if 'data-icon="send"' in html or 'data-icon="wds-ic-send-filled"' in html or 'aria-label="Send"' in html or 'aria-label="Enviar"' in html:
                target_btn = btn
                print(f"DEBUG: Botão encontrado por análise de HTML!")
                break

        if target_btn:
            driver.execute_script("arguments[0].click();", target_btn)
            print("DEBUG: CLIQUE REALIZADO NO BOTÃO ENCONTRADO.")
        else:
            print("DEBUG: Botão não encontrado. Tentando ENTER no input.")
            inp = footer.find_element(By.XPATH, ".//div[@contenteditable='true']")
            inp.send_keys(Keys.ENTER)

    except Exception as e:
        print(f"DEBUG: Erro na etapa final: {e}")
        driver.save_screenshot("debug_final_step_error.png")

    print("DEBUG: Aguardando 5 minutos para garantir envio...")
    driver.save_screenshot("debug_final_step.png")
    time.sleep(5 * 60)
    driver.save_screenshot("debug_final_step_after.png")
    print("DEBUG: Fluxo finalizado.")


def send_msg(msg: str):
    options = Options()
    
    # Evitar que detectem o bot
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # User-Agent Windows + Chrome
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')
    
    options.add_argument(f"user-data-dir={config.chrome_dir}")

    # Rodar sem interface grafica (para o server)
    if config.headless:
        options.binary_location = "/usr/bin/chromium" 
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument("--force-device-scale-factor=1")

    service = Service("/usr/bin/chromedriver")

    print("DEBUG: Inicializando driver...")
    driver = wb.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        print("DEBUG: Abrindo WhatsApp Web...")
        driver.get("https://web.whatsapp.com/")

        logged_in = False
        last_qr_code = None
        attempts = 0
        max_attempts = 90

        print("DEBUG: Aguardando Login ou QR Code...")
        
        while not logged_in and attempts < max_attempts:
            try:
                driver.find_element(By.ID, "side")
                print("\nDEBUG: LOGIN REALIZADO COM SUCESSO!")
                logged_in = True
                break
            except:
                pass

            try:
                current_qr = print_terminal_qr(driver)
                
                if current_qr:
                    if current_qr != last_qr_code:
                        last_qr_code = current_qr
                        attempts = 0
                else:
                    # SE NÃO TEM QR CODE E NÃO TEM LOGIN (SIDE)
                    # Significa que está na tela de "Sincronizando mensagens..."
                    print(f"DEBUG: Processando login/Sincronizando... ({attempts}/{max_attempts})", end='\r')
                    
            except:
                pass

            time.sleep(2)
            attempts += 1

        print("") # Quebra de linha após o loop

        if not logged_in:
            print("ERRO: Tempo limite excedido na sincronização.")
            driver.save_screenshot("debug_timeout_sync.png")
            return

        # Pós-Login
        print("DEBUG: Aguardando carregamento das conversas (15s)...")
        time.sleep(15) 

        try:
            pickle.dump(driver.get_cookies(), open('.cookies.pkl', 'wb'))
        except:
            pass

        print("DEBUG: Enviando mensagem...")
        send_msg_via_url(driver, msg, "TCN")

    except Exception as e:
        print(f"Erro Fatal (Main): {e}")
        driver.save_screenshot("debug_fatal_error.png")
    finally:
        driver.quit()
        print("DEBUG: Driver encerrado.")

def send():
    # Verifica o dia/hora e carrega refeição
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_raiz = os.path.dirname(diretorio_atual)
    
    try:
        caminho_meal = os.path.join(diretorio_raiz, config.week_meals_file)
        with open(caminho_meal, "r", encoding="utf-8") as file:
            meal = json.load(file)[str(date.today())]
            hour = datetime.now().hour
            time_key = "almoco" if hour < 15 else "jantar"
            
            if time_key in meal:
                meal = meal[time_key]["RU"]
            else:
                print("Refeição não encontrada para o horário.")
                return -1

        caminho_msgs = os.path.join(diretorio_raiz, config.msgs)
        with open(caminho_msgs, "r", encoding="utf-8") as file:
            msgs = json.load(file)

        caminho_rel = os.path.join(diretorio_raiz, config.relationships)
        with open(caminho_rel, "r", encoding="utf-8") as file:
            classification = json.load(file)

        quality = get_quality(meal, classification)
        msg_final = create_msg(meal, quality, msgs)
        
        send_msg(msg_final)

    except Exception as e:
        print(f"Erro na preparação dos dados: {e}")

if __name__ == "__main__":
    send()
