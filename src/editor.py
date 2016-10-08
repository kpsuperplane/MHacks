from moviepy.editor import *
#from . import TimeStamp
import wave

clips = {}
audioClips = {}

def getVideoClip(clip):
    if (not (clip in clips)):
        clips[clip] = VideoFileClip(clip)
    return clips[clip]

def getAudioClip(clip):
    clip = "scratch/" + clip
    if (not (clip in audioClips)):
        audioClips[clip] = wave.open(clip, "rb")
    return audioClips[clip]

def combineVideos(parts):
    clips = []
    for part in parts:
        clips.append(getVideoClip(part.getName()).subclip(part.getBegin(), part.getBegin() + part.getDuration()))
    return concatenate_videoclips(clips)
    for clip, data in clips.items():
        data.close()

def combineAudio(parts, outfile):
    data = []
    files = {}
    output = wave.open(outfile, 'wb')
    for part in parts:
        w = getAudioClip(part[2])
        #framesize = w.getsampwidth() * w.getnchannels()
        #w.rewind()                   
        w.setpos(part[0])
        data.append([w.getparams(), w.readframes(part[1])])
    #output.setparams(data[0][0])
    output.setframerate(16000)
    output.setsampwidth(2)
    output.setnchannels(1)
    for frame in data:
        output.writeframes(frame[1])
    output.close()
    for clip, data in audioClips.items():
        data.close()
        
    
