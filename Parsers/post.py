from requests import Session
import requests
from bs4 import BeautifulSoup
import xlsxwriter
import sys
import html
sys.stdout.reconfigure(encoding='utf-8')

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0"}

work = Session()
work.get("https://quotes.toscrape.com/", headers = headers)
resp = work.get("https://quotes.toscrape.com/login", headers = headers)

soup = BeautifulSoup(resp.text, "lxml")
token = soup.find("form").find("input").get("value")
data = {"csrf_token" : token,
        "username" : "123",
        "password" : "1234"}

res = work.post("https://quotes.toscrape.com/login", headers=headers, data=data, allow_redirects = True)

def fullInfo():
    c = 1
    while True:
        url = f"https://quotes.toscrape.com/page/{c}/"
        c += 1
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.text, "lxml")
        data  = soup.find_all("div", class_ = "quote")
        if not data:
            break
        for i in data:
            quote = i.find("span").text
            quote = quote.replace('“', '"').replace('′', "'")
            author = i.find("small").text
            print(quote + "\n" + author + "\n\n")
            yield quote, author

def writer(param):
    book = xlsxwriter.Workbook("E:\learnGPT\proff\quote.xlsx")
    page = book.add_worksheet("Quote")

    row = 1
    col = 0

    page.set_column("A:A", 20)
    page.set_column("B:B", 50)

    page.write(0,0, "Author")
    page.write(0, 1, "Quote")

    for i in param():
        page.write(row, col, i[1])
        page.write(row, col + 1, i[0])
        row += 1

    book.close()

writer(fullInfo)