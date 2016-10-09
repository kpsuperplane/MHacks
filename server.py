from flask import Flask, request, send_from_directory, send_file
##

from src.TimeStamp import TimeStamp
from src.editor import *
import os, wave,pickle,random
import re
from pydub import AudioSegment
import markovify

##
from generate_speech_to_audio import S2A
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_folder='client/build/', static_url_path='')


@app.route('/')
def root():
    return app.send_static_file("index.html")


s2a = {'trump': S2A('trump',2), 'hillary': S2A('hillary',1), 'obama': S2A('obama',2)}

@app.route('/generate/audio')
def gen_audio():
    person = request.args.get("person")
    text = request.args.get("text")
    #person: 'trump', 'hillary', or 'obama'
    output = wave.open("sample-o.wav", "wb")
    output.setnchannels(1)
    output.setsampwidth(2)
    output.setframerate(16000)
    s = s2a[person]
    s.speech_to_audio(text,output)
    output.close()
    AudioSegment.from_wav("sample-o.wav").export("sample-o.mp3", format="mp3")
    try:
        return send_file('sample-o.mp3', attachment_filename='sample-o.mp3')
    except Exception as e:
        return str(e)

@app.route('/generate/phrase')
def gen_phrase():
    person = request.args.get("person")
    #markov shit
    s = s2a[person]
    return s.text_model.make_short_sentence(200)


if __name__ == "__main__":
    app.run()
