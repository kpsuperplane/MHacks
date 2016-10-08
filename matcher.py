#"""[[timestamp in milliseconds, length, word], ]"""
#"""{word:[[timestamp, length, filename],[timestamp, length,filename]], word...} """
from phonemizer import getPhonemes
def match(song, dictionary):
    mapping = []
    phonemes = {}
    for word, pms in getPhonemes(list(dictionary.keys())).items():
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
        length = song[i][1]
        if (word in dictionary):
            min_diff = length
            index = 0
            for j in len(dictionary[word]):
                diff = abs(length - dictionary[word][j][1])
                if (diff < min_diff):
                    index = j
                    min_diff = diff
            mapping.append(dictionary[word][index])
        else:
            wordnemes = getPhonemes([word])[word]
            targetLength = length*(1/float(len(wordnemes)))
            for phoneme in wordnemes:
                if phoneme[0] in phonemes:
                    min_diff = 1<<29
                    foundLength = 0
                    foundOffset = 0
                    index = []
                    cnt = 0
                    for j in range(0, len(phonemes[phoneme[0]])):
                        phonword = phonemes[phoneme[0]][j]
                        for k in range(0, len(dictionary[phonword[0]])):
                            phonLength = dictionary[phonword[0]][k][1]*phonword[2]
                            diff = abs(targetLength - phonLength)
                            if diff < min_diff:
                                min_diff = diff
                                foundLength = phonLength
                                foundOffset = dictionary[phonword[0]][k][1] * phonword[1]
                                index = [j, k]
                    cpy = list(dictionary[phonemes[phoneme[0]][index[0]][0]][index[1]]) #shallow copy this 
                    cpy[1] = foundLength
                    cpy[0] = cpy[0] + foundOffset
                    mapping.append(cpy)

    return mapping


    

print(match([[123, 2, "andrew"]], {"anna": [[23, 1, "anna.mp3"]], "drink": [[16, 1, "drink.mp3"]], "euphoria": [[1, 2, "euphoria.mp3"]]}))