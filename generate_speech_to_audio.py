from src.TimeStamp import TimeStamp
from src.editor import *
import os, wave,pickle,random
import re

import markovify

from pydub import AudioSegment

import nltk
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer

import inflect

inflect_engine = inflect.engine()

class S2A:
    volumns = {
        'obama': 10,
        'trump': -5,
        'hillary': 10
    }

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

        lst = []
        for i in range(len(self.v[word])):
            if self.name == 'trump':
                if self.v[word][i][3]/100 < 180:
                    continue
            lst.append((self.v[word][i] , i))

        lst.sort(key = lambda x: x[0][3] - x[0][2])
        #lst.sort(key = lambda x: x[0][1])

        return str(lst[len(lst)//2][1])

        for i in range(len(self.v[word])):
            if self.v[word][i][1] > best:
                best = self.v[word][i][1]
                ind = i
        return str(ind)

    def speech_to_audio(self, words, output):
        print(words)
        print()

        if not words: return
        words = re.findall(r"[\w]+", words)

        if len(words) == 0:
            return
        data = []

        for word in words:
            self.word_to_audio(word, data)

        #print(len(data))
        for datum in data:
            output.writeframes(datum)

    def word_to_audio(self, word, data):
        word = word.lower()

        if word not in self.v and inflect_engine.plural(word) in self.v:
            word = inflect_engine.plural(word)

        if word not in self.v and inflect_engine.singular_noun(word) in self.v:
            word = inflect_engine.singular(word)

        if word not in self.v and inflect_engine.present_participle(word) in self.v:
            word = inflect_engine.present_participle(word)

        if word not in self.v and WordNetLemmatizer().lemmatize(word,'v') in self.v:
            word = WordNetLemmatizer().lemmatize(word,'v')

        if word in self.v:
            filename = "speech/%s/"%self.name+word+"/"+self.find_best_match(word)+".wav"

            #w = wave.open(filename, 'rb')
            clip = AudioSegment.from_wav(filename)
            if self.name in self.volumns:
                clip = clip + self.volumns[self.name]

            #data.append(w.readframes(w.getnframes()))
            #w.close()
            data.append(clip.raw_data)
        else:
            if word[0].isdigit():
                num = inflect_engine.number_to_words(word)
                for word in re.findall(r"[\w]+", num):
                    self.word_to_audio(word, data)

output = wave.open("sample.wav","wb")
output.setnchannels(1)
output.setsampwidth(2)
output.setframerate(16000)

s2a = [S2A('trump'), S2A('hillary'), S2A('obama')]

for i in range(5):
    for s in s2a:
        s.speech_to_audio(s.text_model.make_short_sentence(200), output)

output.close()

