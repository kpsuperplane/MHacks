from src.TimeStamp import TimeStamp
from src.editor import *
import os, wave,pickle,random
import re

name = "trump"

v = pickle.load(open("speech/%s.pickle"%name,"rb"))
def find_best_match(word):
    best = -1e10
    ind = 0
    return str(random.randint(0,len(v[word])-1))
    for i in range(len(v[word])):
        if v[word][i][1] > best:
            best = v[word][i][1]
            ind = i
    return str(ind)

def speech_to_audio(words, output):
    print(words)
    if not words: return
    words = re.findall(r"[\w']+", words)

    if len(words) == 0:
        return
    data = []

    for word in words:
        word = word.lower()

        if word not in v and word[-1] == 's' and word[:-1] in v:
            word = word[:-1]

        if word not in v and word[-1] != 's' and word + 's' in v:
            word = word + 's'

        if word in v:
            w = wave.open("speech/%s/"%name+word+"/"+find_best_match(word)+".wav", 'rb')
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()
    print(len(data))
    for datum in data:
        output.writeframes(datum[1])

import markovify

# Get raw text as string.
with open("speech/%s.txt"%name) as f:
    text = f.read()

#text = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
#text = " ".join(filter(lambda x: not x.isalpha() or x in v, text))

#print(text)

# Build the model.
text_model = markovify.Text(text)

output = wave.open("sample.wav","wb")
output.setnchannels(1)
output.setsampwidth(2)
output.setframerate(16000)

# for i in range(5):
#     speech_to_audio(text_model.make_short_sentence(200), output)

speech_to_audio(" ".join(['china'] * 10), output)


output.close()

