from bs4 import BeautifulSoup as bs4
import requests
import genanki
import random
import time
import createWordlist

# Anki note models
basicAndReversedDeuEng = genanki.Model(
    1485830181,                             # model ID (must be unique)
    'Basic (and reversed card) (DEU-ENG)',
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


class Flashcard:
    """Represents the representation of anki flashcard."""

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


def parseWordlist(wordlist):
    """Parse online dictionary to create flashcards.

    :param wordlist: Wordlist to create flashcards for.
    :return: List of preprepared anki flashcards.
    :rtype: List of Flashcard
    """
    flashcards = []
    randomGenerator = random.Random(int(time.time()) % 10e12)
    for i, word in enumerate(wordlist):
        # delay call to request.get to avoid ip being blocked due to data
        # scraping
        time.sleep(randomGenerator.randint(1, 10))
        card = Flashcard(word)
        # web scraper api to prevent IP being blocked - scraperapi
        webScraperApi = 'http://api.scraperapi.com?api_key=2931541d27b5b3c4031cd29902ecdad0&url='
        basicUrl = webScraperApi + \
            'https://www.linguee.de/deutsch-englisch/search?source=deutsch&query='
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
                # wordType = div.find('span', class_='tag_type')
                # wordTypeVal = ''
                # noun = ''
                # if wordType is not None:
                #     wordTypeVal = wordType.getText()
                #     if wordTypeVal == 'f':
                #         noun = 'die '
                #     elif wordTypeVal == 'm':
                #         noun = 'der '
                #     elif wordTypeVal == 'nt':
                #         noun = 'das '

                translatedWord = str(translation.getText())
                card.translations.append(translatedWord)

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

        flashcards.append(card)
    return flashcards


def generateAnkiFlashcards(wordlist, modelNote, fileName):
    """Generate Anki flashcards for the given wordlist.

    :param wordlist: Wordlist to create flashcards for.
    :param modelNote: Anki note model.
    :param fileName: File name to save Anki deck.
    """
    flashcards = parseWordlist(wordlist)
    randInt = int(int(time.time()) % 10e12)
    deck = genanki.Deck(
        randInt,            # unique deck ID
        fileName)

    for i in flashcards:
        note = genanki.Note(
            model=modelNote,
            fields=[i.front(), i.back()])
        deck.add_note(note)

    # generate Anki deck
    file = fileName + '.apkg'
    genanki.Package(deck).write_to_file(file)


wordList = createWordlist.createWordList('testDeuEng.txt')

# test function call
generateAnkiFlashcards(wordList, basicAndReversedDeuEng,
                       'testDeuEng2')
