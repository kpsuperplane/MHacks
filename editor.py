from moviepy.editor import *

clips = {}

def getVideoClip(clip):
    if (not (clip in clips)):
        clips[clip] = VideoFileClip("scratch/young.mp4")
    return clips[clip]

def combineVideos(parts):
    clips = []
    for part in parts:
        clips.append(getVideoClip(part[0]).subclip(part[1], part[1] + part[2]))
        part[0]
    return concatenate_videoclips(clips)


video = "scratch/young.mp4"
combineVideos([[video, 0, 10], [video, 40, 4]]).write_videofile("scratch/young-cut.mp4") # Many options...