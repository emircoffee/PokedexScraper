from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from typing import List, NamedTuple
import csv
import json

class Pokemon(NamedTuple):
    name: str
    dex_entries: List[str]
# pokemon object that holds all the data

outfile = open("serebii_data.csv","w",encoding="utf-8")
writer = csv.writer(outfile)
# creates csv output file for data

with open('serebii_data.json', 'w', encoding='utf-8') as f:
    json.dump([], f, ensure_ascii=False, indent=4)

def scrape_pokedex(url):
    scraper_counter = 0
    request = Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    page = urlopen(request)
    page_content_bytes = page.read()
    page_html = page_content_bytes.decode("utf-8", 'ignore')

    soup = BeautifulSoup(page_html, "html.parser")
    directory = soup.find_all("div", {"align": "center"})[1].find_all("table")[1].find_all("td")[3].find_all("select", {"name": "SelectURL"})[0].find_all("option")
    for link in directory:
        try:
            extension = link["value"]
            scrape_page("https://serebii.net" + extension)
        except:
            print("Huh?")

def scrape_page(page_name):
    request = Request(
        page_name,
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    page = urlopen(request)
    page_content_bytes = page.read()
    page_html = page_content_bytes.decode("utf-8", 'ignore')

    soup = BeautifulSoup(page_html, "html.parser")

    name = soup.find_all("div", {"id": "content"})[0].find_all("div", {"align": "center"})[1].find_all("table", {"class": "dextable"})[1].find_all("tr")[1].find_all("td")[0].getText()
    dex_entries = []
    dex_entries.append(soup.find_all("div", {"id": "content"})[0].find_all("div", {"align": "center"})[1].find_all("table", {"class": "dextable"})[7].find_all("tr")[1].find_all("td")[1].getText())
    dex_entries.append(soup.find_all("div", {"id": "content"})[0].find_all("div", {"align": "center"})[1].find_all("table", {"class": "dextable"})[7].find_all("tr")[2].find_all("td")[1].getText())


    scraped_pokemon = Pokemon(
        name = name,
        dex_entries = dex_entries,
    )

    writer.writerow(scraped_pokemon)
    with open('serebii_data.json', 'r+', encoding='utf-8') as f:
        file = json.load(f)
        data = {
            name:
            {
                "dex_entries": dex_entries
            }
        }
        file.append(data)
        f.seek(0)
        json.dump(file, f, ensure_ascii=False, indent=4)
    print(name)

scrape_pokedex("https://serebii.net/pokedex-sv/")