import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Sayta sorğu göndər
url = "https://bina.az/"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Excel faylı üçün hazırlıq
wb = Workbook()
ws = wb.active
ws.title = "bina Listings"
ws.append(["Ad", "Qiymət (AZN)"])

# Üç listi eyni anda al
hous = soup.find_all("div", class_="card_params")

for i in hous:
    ad_tag = i.find("div", class_="location")
    qiymet_tag = i.find("span", class_="price-val")

    ad = ad_tag.get_text(strip=True) if ad_tag else ""
    qiymet_raw = qiymet_tag.get_text(strip=True) if qiymet_tag else ""

    qiymet = int(qiymet_raw.replace(" ", "").replace("₼", "").replace(",", "")) if qiymet_raw else 0
    if ad and qiymet > 100000:
        ws.append([ad, qiymet])

# Excel faylını yadda saxla
wb.save("bina_listings.xlsx")
print("Done: bina_listings.xlsx")
