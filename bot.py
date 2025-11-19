import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ocr import extract_score_from_image_path
from estrategia import gerar_sinal
from telegram import Bot

TELEGRAM_TOKEN = "TOKEN_DO_TELEGRAM"
CHAT_ID = "SEU_CHAT_ID"

URL = "https://www.bet365.com/#/AVR/B146/"

bot = Bot(token=TELEGRAM_TOKEN)
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1280,900")

driver = webdriver.Chrome(options=options)
driver.get(URL)
time.sleep(10)

historico = []
last = None

try:
    while True:
        driver.save_screenshot("tela.png")
        placar = extract_score_from_image_path("tela.png")

        if placar:
            print("Placar:", placar)
            if not historico or placar != historico[-1]:
                historico.append(placar)
                sinal = gerar_sinal(historico)
                if sinal and sinal != last:
                    bot.send_message(chat_id=CHAT_ID, text=sinal)
                    last = sinal
                    print("Enviado:", sinal)

        time.sleep(5)

finally:
    driver.quit()
