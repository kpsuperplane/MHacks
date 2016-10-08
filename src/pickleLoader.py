import pickle

def loadOccurences(file):
    data = pickle.load(open(file))
    output = {}
    for word, occurences in data:
        if (not (word in output)):
            output[word] = []
        for occurence in occurences:
            output[word].append([occurence[2], occurence[3] - occurence[2],file])
    return output