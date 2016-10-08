from matcher import match
from pickleLoader import *

def generateFromText(text, pickle):
    words = text.split(" ")
    input = []
    length = 0
    for word in words:
        input.append([length, len(word), word.lower()])
        length = length + len(word)
    return match(input, loadOccurences(pickle))

print(generateFromText("I like to eat pie because it tastes great", "words.pickle"))
