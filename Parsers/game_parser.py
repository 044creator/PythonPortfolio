import requests
from bs4 import BeautifulSoup
import xlsxwriter
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0"}

def fullInfo():
    i = 1
    while True:
        url = f"https://game-shop.com.ua/ua/category/igryi-dlya-playstation-4/{i}"
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.text, "lxml")
        div = soup.find("div", class_ = "block-body")
        if not div:
            break
        data = div.find_all("div", class_="cs-product-block")
        for card in data:
            name = card.find("div", class_ = "name").text.replace("PS4", "").strip()
            new_name = re.sub('[\u0400-\u04FF]', '', name)
            price = card.find("span", class_ = "orig").text
            new_price = re.search(r'\d+', price).group()
            yield new_name, new_price
        i += 1

def writer(param):
    book = xlsxwriter.Workbook("E:\learnGPT\proff\Game.xlsx")
    page = book.add_worksheet("Game")

    row = 1
    col = 0

    page.set_column("A:A", 50)
    page.set_column("B:B", 20)

    page.write(0,0, "Game:")
    page.write(0, 1, "Price:")

    for i in param():
        page.write(row, col, i[0])
        page.write(row, col + 1, i[1])
        row += 1

    book.close()

writer(fullInfo)