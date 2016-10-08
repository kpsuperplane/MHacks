"""[[timestamp in milliseconds, length, word], …]"""
"""{word:[[timestamp, length, filename],[timestamp, length,filename]], word...} """
def funct(song, dictionary):
    mapping = []
    for i in range(len(song)):
        word = song[i][2]
        timestamp = song[i][0]
        length = song[i][1]
        if (word in dictionary):
            min_diff = length
            index = 0
            for j in len(dictionary[word]):
                if (length - dictionary[word][j][1] < min_diff):
                    index = j
            mapping.append(dictionary[word][index]+[word])
        else:
            mapping.append("invalid")
