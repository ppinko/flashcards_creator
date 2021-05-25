from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import copy
import genanki

print('\n')

basicUrl = 'https://www.linguee.de/deutsch-englisch/search?source=englisch&query='

words = ['sleep']
translated = []
flashcards = []


class Flashcard:
    """Represents the representation of anki flashcard."""

    # data members
    word = ''
    translations = []
    questions = []
    examples = []

    def __init__(self, word):
        """Basic constructor.

        :param word: A word to translate.
        """
        self.word = word
        self.translations = []
        self.questions = []
        self.examples = []

    def front(self):
        """Return string representation of the front side of the flashcard.

        :return: The string representation of the front side of the flashcard.
        :rtype: str
        """
        front = ''
        front += self.word + '<br/><br/>'
        for i, val in enumerate(self.questions):
            if val != '':
                front += '{0}) {1}'.format(i, val) + '<br/>'
        return front

    def back(self):
        """Return string representation of the back side of the flashcard.

        :return: The string representation of the back side of the flashcard.
        :rtype: str
        """
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
        return back


for i, word in enumerate(words):
    card = Flashcard(word)
    url = basicUrl + word
    page = requests.get(url)
    soup = bs4(page.text, 'html.parser')
    divs = soup.findAll('div', class_='translation sortablemg featured')
    counter = 0
    for div in divs:
        if counter < 3:
            translation = div.find('a', class_='dictLink featured')
            if translation is None:
                continue

            counter += 1
            wordType = div.find('span', class_='tag_type')
            wordTypeVal = ''
            noun = ''
            if wordType is not None:
                wordTypeVal = wordType.getText()
                if wordTypeVal == 'f':
                    noun = 'die '
                elif wordTypeVal == 'm':
                    noun = 'der '
                elif wordTypeVal == 'nt':
                    noun = 'das '

            translatedWord = str(translation.getText())
            card.translations.append(noun + translatedWord)

            example = div.find('div', class_='example line')

            if example is not None:
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
            else:
                card.questions.append('')
                card.examples.append('')
        else:
            break

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
