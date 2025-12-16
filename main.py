# logica central de chamar a api, salvar ela em data (para nao ter que fzr o web scrapping duas
# vezes por dia), depois linkar ela com a classe, e mandar para o zap.
# agendamento de mensagem atraves de bibliotecas como a prorpia schedule (chama web-scraper e whatsapp)

import schedule
import time
from src.web_scraper import save_weekly_data
from src.whatsapp import send

schedule.every().monday.at("08:00").do(save_weekly_data)
schedule.every().day.at("09:00").do(send)
schedule.every().day.at("16:00").do(send)

# Garantindo que temos dados para enviar
save_weekly_data() 

while True:
    schedule.run_pending()
    time.sleep(1)    
