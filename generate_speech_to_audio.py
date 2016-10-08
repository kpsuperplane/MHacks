from TimeStamp import TimeStamp
from editor import *
import os, wave

def speech_to_audio(words):
    if len(words) == 0:
        return
    data = []
    for word in words:
        if os.path.isfile("words/"+word+"/0.wav"):
            w = wave.open("words/"+word+"/0.wav", 'rb')
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()
    print(len(data))
    output = wave.open("sample.wav","wb")
    output.setparams(data[0][0])
    for datum in data:
        output.writeframes(datum[1])
    output.close()


