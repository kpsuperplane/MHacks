#"""[[timestamp in milliseconds, length, word], ]"""
#"""{word:[[timestamp, length, filename],[timestamp, length,filename]], word...} """
from . import phonemizer
def match(song, dictionary):
    mapping = []
    phonemes = {}
    for word, pms in phonemizer.getPhonemes(list(dictionary.keys())).items():
        key = 0
        size = 1/float(len(pms))
        for phoneme in pms:
            phoneme = phoneme[0]
            if (not (phoneme in phonemes)):
                phonemes[phoneme] = []
            phonemes[phoneme].append([word, size * key, size])
            key = key + 1
    for i in range(len(song)):
        word = song[i][2]
        timestamp = song[i][0]
        length = song[i][1] * 1.5
        if word[-1:] == 's':
            word = word[0:-1]
        if (word in dictionary):
            opt_diff = 0
            index = 0
            for j in range(0, len(dictionary[word])):
                diff = dictionary[word][j][1]#abs(length - dictionary[word][j][1])
                if (diff < opt_diff):
                    index = j
                    opt_diff = diff
            mapping.append(dictionary[word][index])
        else:
            wordnemes = phonemizer.getPhonemes([word])[word]
            targetLength = length*(1/float(len(wordnemes)))
            for phoneme in wordnemes:
                if phoneme[0] in phonemes:
                    opt_diff = 1<<29
                    foundLength = 0
                    foundOffset = 0
                    index = 0
                    cnt = 0
                    usedWord = None
                    phonword = max(phonemes[phoneme[0]])
                    for k in range(0, len(dictionary[phonword[0]])):
                        phonLength = dictionary[phonword[0]][k][1]*phonword[2]
                        diff = abs(targetLength - phonLength)
                        if diff < opt_diff:
                            opt_diff = diff
                            foundLength = phonLength
                            foundOffset = dictionary[phonword[0]][k][1] * phonword[1]
                            index = k
                            usedWord = phonword[0]
                    cpy = dictionary[usedWord][index][:] #shallow copy this 
                    cpy[1] = int(foundLength)
                    cpy[0] = int(cpy[0] + foundOffset) 
                    print(usedWord)
                    mapping.append(cpy)
                else:
                    print("Missing phoneme for " + phoneme[0])

    print(mapping)
    return mapping


    
