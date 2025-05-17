import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
BASE_URL = "https://intothespiderverse.fandom.com"
CATEGORY_URL = f"{BASE_URL}/wiki/Category:Characters"
HEADERS = {"User-Agent": "Mozilla/5.0"}
EXCLUDE_FIELDS = {"Portrayed by", "Date of Death", "Romantic Interest(s)", "Voiced by", "Ethnicity", "Weight", "Nickname(s)", "Date of Birthday", "Religion"}
def get_character_links():
    response = requests.get(CATEGORY_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    return [BASE_URL + link.get('href') for link in soup.select('.category-page__member-link')]
def get_character_info(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find('h1', class_='page-header__title').text.strip()
    info_box = soup.find('aside', class_='portable-infobox')
    data = {"Имя": name}
  
    if info_box:
        for row in info_box.find_all('div', class_='pi-item'):
            if (label := row.find('h3', class_='pi-data-label')) and (value := row.find('div', class_='pi-data-value')):
                if (label_text := label.text.strip()) not in EXCLUDE_FIELDS:
                    data[label_text] = value.text.strip()
    return data
def main():
    characters = [get_character_info(link) for link in get_character_links()]
    pd.DataFrame(characters).to_csv("characters.csv", index=False, encoding="utf-8-sig")
    print("Файл сохранен: characters.csv")

if __name__ ==
