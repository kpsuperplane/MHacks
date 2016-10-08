import pickle

def loadOccurences(file):
    data = pickle.load(open(file, "rb"))
    output = {}
    for word, occurences in data.items():
        if word[-1:] == 's':
            word = word[0:-1]
        if (not (word in output)):
            output[word] = []
        for occurence in occurences:
            if occurence[2]/100 < 180:
                continue
            output[word].append([occurence[2]*160, 160*(occurence[3] - occurence[2]), "trump.wav"])
    return output

def loadWords(file):
    data = pickle.load(open(file, "rb"))
    output = []
    for word, occurences in data.items():
        if word[-1:] == 's':
            word = word[0:-1]
        for occurence in occurences:
            output.append([occurence[2]*160, 160*(occurence[3] - occurence[2]), file, "trump.wav"])
    return sorted(output)
