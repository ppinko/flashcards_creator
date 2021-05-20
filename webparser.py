from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd

print('\n')

basicUrl = 'https://www.linguee.de/deutsch-englisch/search?source=englisch&query='

words = ['home', 'kitchen', 'bedroom', 'bathroom', 'corridor']
translated = []

for i in range(len(words)):
    url = basicUrl + words[i]
    # print(url)
    page = requests.get(url)               
    soup = bs4(page.text, 'html.parser')
    divs =soup.findAll('div', class_='translation sortablemg featured')
    for i, div in enumerate(divs):
        if i < 3:
            translation=div.find('a',class_='dictLink featured')
            print(translation.getText())
    print()