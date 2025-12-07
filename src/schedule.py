# agendamento de mensagem atraves de bibliotecas como a prorpia schedule (chama web-scraper e whatsapp)
import schedule
import time
from init import save_weekly_data

schedule.every().monday.at("10:00").do(save_weekly_data)

while True:
    schedule.run_pending()
    time.sleep(1)