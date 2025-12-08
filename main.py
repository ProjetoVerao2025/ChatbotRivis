# logica central de chamar a api, salvar ela em data (para nao ter que fzr o web scrapping duas
# vezes por dia), depois linkar ela com a classe, e mandar para o zap.
# agendamento de mensagem atraves de bibliotecas como a prorpia schedule (chama web-scraper e whatsapp)
    
import schedule
import time
from init import save_weekly_data

schedule.every().monday.at("10:00").do(save_weekly_data)

while True:
    schedule.run_pending()
    time.sleep(1)