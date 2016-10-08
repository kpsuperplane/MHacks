from moviepy.editor import *

def videoToAudio(file, output):
    VideoFileClip(file).audio.write_audiofile(output)