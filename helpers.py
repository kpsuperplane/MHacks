from moviepy.editor import *

def videoToAudio(file, output):
    getVideoClip(file).write_audiofile(output)