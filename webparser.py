from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import copy

print('\n')

basicUrl = 'https://www.linguee.de/deutsch-englisch/search?source=englisch&query='

words = ['home', 'kitchen', 'bedroom', 'bathroom', 'corridor']
translated = []
flashcards = []


class Flashcard:
    # data members
    word = ''
    translations = []
    questions = []
    examples = []

    def __init__(self, word):
        self.word = word
        self.translations = []
        self.questions = []
        self.examples = []

    def print(self):
        print('#' * 20)
        print(self.word, '\n')
        for i, val in enumerate(self.questions):
            if val != '':
                print('{0}) {1}'.format(i, val))
        print()

        equivalents = ''
        for i in self.translations:
            equivalents += i + ', '
        equivalents = equivalents[0:-2]
        print(equivalents, '\n')

        for i, val in enumerate(self.examples):
            if val != '':
                print('{0}) {1} -> {2}'.format(i, self.translations[i], val))
            else:
                print('{0}) {1}'.format(i, self.translations[i]))


for i, word in enumerate(words):
    card = Flashcard(word)
    url = basicUrl + word
    # print(url)
    page = requests.get(url)
    soup = bs4(page.text, 'html.parser')
    divs = soup.findAll('div', class_='translation sortablemg featured')
    for i, div in enumerate(divs):
        if i < 3:
            translation = div.find('a', class_='dictLink featured')
            # print(translation.getText())
            card.translations.append(translation.getText())

            example = div.find('div', class_='example line')
            examplesENG = example.findAll('span', class_='tag_s')
            if len(examplesENG) != 0:
                # print(examplesENG[0].getText())
                card.questions.append(examplesENG[0].getText())
            else:
                card.questions.append('')

            examplesDEU = example.findAll('span', class_='tag_t')
            if len(examplesDEU) != 0:
                # print(examplesDEU[0].getText())
                card.examples.append(examplesDEU[0].getText())
            else:
                card.examples.append('')

    flashcards.append(copy.deepcopy(card))

for i in flashcards:
    i.print()
