from src.TimeStamp import TimeStamp
from src.editor import *
import os, wave,pickle,random
import re

import markovify

class S2A:
    def __init__(self, name):
        self.name = name
        self.v = pickle.load(open("speech/%s.pickle"%self.name,"rb"))

        #text = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
        #text = " ".join(filter(lambda x: not x.isalpha() or x in v, text))

        #print(text)
        # Get raw text as string.
        with open("speech/%s.txt"%self.name) as f:
            text = f.read()

        self.text_model = markovify.Text(text)

    def find_best_match(self, word):
        best = -1e10
        ind = 0
        return str(random.randint(0,len(self.v[word])-1))
        for i in range(len(self.v[word])):
            if self.v[word][i][1] > best:
                best = self.v[word][i][1]
                ind = i
        return str(ind)

    def speech_to_audio(self, words, output):
        print(words)
        if not words: return
        words = re.findall(r"[\w']+", words)

        if len(words) == 0:
            return
        data = []

        for word in words:
            word = word.lower()

            if word not in self.v and word[-1] == 's' and word[:-1] in self.v:
                word = word[:-1]

            if word not in self.v and word[-1] != 's' and word + 's' in self.v:
                word = word + 's'

            if word in self.v:
                w = wave.open("speech/%s/"%self.name+word+"/"+self.find_best_match(word)+".wav", 'rb')
                data.append([w.getparams(), w.readframes(w.getnframes())])
                w.close()
        print(len(data))
        for datum in data:
            output.writeframes(datum[1])

output = wave.open("sample.wav","wb")
output.setnchannels(1)
output.setsampwidth(2)
output.setframerate(16000)

s2a = [S2A('trump'), S2A('hillary'), S2A('obama')]

for i in range(5):
    for s in s2a:
        s.speech_to_audio(s.text_model.make_short_sentence(200), output)

output.close()

