from . import matcher
from . import pickleLoader

def generateFromText(text, pickle):
    words = text.split(" ")
    input = []
    length = 0
    for word in words:
        input.append([length, len(word), word.lower()])
        length = length + len(word)
    return matcher.match(input, pickleLoader.loadOccurences(pickle))

