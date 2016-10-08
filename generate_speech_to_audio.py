from src.TimeStamp import TimeStamp
from src.editor import *
import os, wave,pickle,random

v = pickle.load(open("test/trump.pickle","rb"))
def find_best_match(word):
    best = -1e10
    ind = 0
    return str(random.randint(0,len(v[word])-1))
    for i in range(len(v[word])):
        if v[word][i][1] > best:
            best = v[word][i][1]
            ind = i
    return str(ind)

def speech_to_audio(words):
    if len(words) == 0:
        return
    data = []
 
    for word in words:
        if word in v:
            w = wave.open("words/"+word+"/"+find_best_match(word)+".wav", 'rb')
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()
    print(len(data))
    output = wave.open("sample.wav","wb")
    output.setparams(data[0][0])
    for datum in data:
        output.writeframes(datum[1])
    output.close()

sent = "obama is horrible and hillary"
speech_to_audio(sent.split(" "))


