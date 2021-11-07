import string


def createTextList(fileName, outputFile):
    """Strip all whitespaces, digits and punctuations from list of words and
    save stored list in output file.

    :param fileName: Input file name.
    :param outputFile: Output file name.
    """
    with open(fileName, 'r') as reader, open(outputFile, 'w') as writer:
        toStrip = string.digits + '.' + string.whitespace
        for line in reader:
            if len(line) != 0:
                writer.write(line.strip(toStrip) + '\n')


def createWordList(fileName):
    """Create word list from txt file.

    :param fileName: Input file name.
    :rtype: list
    """
    wordlist = []
    with open(fileName, 'r') as reader:
        for line in reader:
            if len(line) > 0 and line != '\n':
                wordlist.append(line.strip())
    return wordlist
