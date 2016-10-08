#!/usr/bin/env python
from os import environ, path
import os
import shutil

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
from moviepy.editor import *

MODELDIR = "lib/pocketsphinx/model"
DATADIR = "lib/pocketsphinx/test/data"

# Create a decoder with certain model
config = Decoder.default_config()
# config.set_string('-hmm', 'cmusphinx-en-us-5.2')
# config.set_string('-lm', 'en-70k-0.2.lm')
# config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
#config.set_int('-frate', 200)

decoder = Decoder(config)

file = "trumpshort.wav"
#file = "forward.wav"

stream = open(file, 'rb')
#stream = open("forward.wav", 'rb')
#stream = open("steve2.wav", 'rb')
#stream = open(path.join(DATADIR, 'goforward.raw'), 'rb')

decoder.start_utt()

while True:
  buf = stream.read()
  if buf:
    print('read')
    decoder.process_raw(buf, False, False)
  else:
    break
decoder.end_utt()
# decoder.decode_raw(stream)

segs = decoder.seg()

# 16000 sample / second
# framesize = 16000
# framerate = 100 /second

words = {}
minframe = float('inf')

for seg in segs:
  #print(seg.start_frame, seg.end_frame, seg.word)
  print(seg.start_frame, seg.end_frame, seg.word)

  word = seg.word.split('(')[0]
  minframe = min(minframe, seg.start_frame)

  if word.isalpha():
    if not word in words:
      words[word] = []
    words[word].append(seg)

clip = AudioFileClip(file)

import wave
origAudio = wave.open(file,'rb')
frameRate = origAudio.getframerate()
nChannels = origAudio.getnchannels()
sampWidth = origAudio.getsampwidth()

print(origAudio.getparams())

shutil.rmtree('words/', ignore_errors=True)

for word in words:
  for i in range(len(words[word])):
    seg = words[word][i]

    os.makedirs('words/%s'%word,exist_ok=True)

    segname = "words/%s/%d.wav"%(word,i)

    origAudio.setpos((seg.start_frame) * 160)
    chunkData = origAudio.readframes((seg.end_frame - seg.start_frame) * 160)

    chunkAudio = wave.open(segname,'wb')
    chunkAudio.setnchannels(nChannels)
    chunkAudio.setsampwidth(sampWidth)
    chunkAudio.setframerate(frameRate)
    chunkAudio.writeframes(chunkData)
    chunkAudio.close()


print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])
