from moviepy.editor import *
from TimeStamp import TimeStamp

clips = {}

def getVideoClip(clip):
    if (not (clip in clips)):
        clips[clip] = VideoFileClip(clip)
    return clips[clip]

def combineVideos(parts):
    clips = []
    for part in parts:
        clips.append(getVideoClip(part.getName()).subclip(part.getBegin(), part.getBegin() + part.getDuration()))
    return concatenate_videoclips(clips)


video = "scratch/young.mp4"
combineVideos([TimeStamp(video, 0, 10), TimeStamp(video, 50, 10)]).write_videofile("scratch/young-cut.mp4") # Many options...