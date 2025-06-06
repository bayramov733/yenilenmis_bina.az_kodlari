from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from telegram.ext import ApplicationBuilder, CommandHandler
import time
import asyncio
import re 

def a():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get("https://bina.az/")
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    evler = []

    elanlar = soup.find_all("div", class_="location")
    qiymetler = soup.find_all("div", class_="abs_block")
    unvanlar = soup.find_all("ul", class_="name")

    for elan_div, qiymet_div, unvan_div in zip(elanlar, qiymetler, unvanlar):
        try:
            elan = elan_div.get_text(strip=True)
            qiymet_raw = qiymet_div.get_text(strip=True)
            unvan = unvan_div.get_text(strip=True)

            # Qiyməti təmizləyib int-ə çeviririk
            qiymet_str = re.sub(r"[^\d]", "", qiymet_raw) 
            qiymet = int(qiymet_str) if qiymet_str else 0

            if qiymet > 100000:
                evler.append(f"{elan} - {qiymet} AZN - {unvan}")
        except:
            continue

    return evler if evler else ["heç bir uyğun elan tapılmadı"]

async def evler(update, context):
    if update.effective_user.id != 1502078472:
        await update.message.reply_text("Bu botdan istifadə etməyə icazə yoxdur.")
        return

    await update.message.reply_text("Evler yüklənir...")
    loop = asyncio.get_event_loop()
    ev_list = await loop.run_in_executor(None, a)

    for ev in ev_list:
        await update.message.reply_text(ev)

if __name__ == '__main__':
    Token = "7805677448:AAFvjnopHMKaabZ9oR8OpE0ZgU-_V8CwI1A"

    app = ApplicationBuilder().token(Token).build()
    app.add_handler(CommandHandler("evler", evler))
    print("Bot işə düşdü...")
    app.run_polling()