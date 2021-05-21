from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import copy
import genanki

print('\n')

basicUrl = 'https://www.linguee.de/deutsch-englisch/search?source=englisch&query='

words = ['kitchen', 'bedroom', 'bathroom', 'corridor']
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

    def front(self) -> str:
        front = ''
        front += self.word + '<br/><br/>'
        for i, val in enumerate(self.questions):
            if val != '':
                front += '{0}) {1}'.format(i, val) + '<br/>'
        return front

    def back(self) -> str:
        equivalents = ''
        for i in self.translations:
            equivalents += i + ', '
        equivalents = equivalents[0:-2]

        back = equivalents + '<br/><br/>'
        for i, val in enumerate(self.examples):
            if val != '':
                back += '{0}) {1} -> {2}'.format(i,
                                                 self.translations[i],
                                                 val) + '<br/>'
            else:
                back += '{0}) {1}'.format(i, self.translations[i]) + '<br/>'
        return back


for i, word in enumerate(words):
    card = Flashcard(word)
    url = basicUrl + word
    page = requests.get(url)
    soup = bs4(page.text, 'html.parser')
    divs = soup.findAll('div', class_='translation sortablemg featured')
    for i, div in enumerate(divs):
        if i < 3:
            translation = div.find('a', class_='dictLink featured')
            card.translations.append(translation.getText())

            example = div.find('div', class_='example line')
            examplesENG = example.findAll('span', class_='tag_s')
            if len(examplesENG) != 0:
                card.questions.append(examplesENG[0].getText())
            else:
                card.questions.append('')

            examplesDEU = example.findAll('span', class_='tag_t')
            if len(examplesDEU) != 0:
                card.examples.append(examplesDEU[0].getText())
            else:
                card.examples.append('')

    flashcards.append(copy.deepcopy(card))

basicAndReversedEngDeu = genanki.Model(
    1485830180,
    'Basic (and reversed card) (ENG-DEU)',
    fields=[
        {
            'name': 'Front',
            'font': 'Arial',
        },
        {
            'name': 'Back',
            'font': 'Arial',
        },
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}',
        },
        {
            'name': 'Card 2',
            'qfmt': '{{Back}}',
            'afmt': '{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}',
        },
    ],
    css='.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n',
)

my_deck = genanki.Deck(
    2059400111,
    'rooms')

for i in flashcards:
    my_note = genanki.Note(
        model=basicAndReversedEngDeu,
        fields=[i.front(), i.back()])
    my_deck.add_note(my_note)

# generate Anki deck
genanki.Package(my_deck).write_to_file('rooms.apkg')
