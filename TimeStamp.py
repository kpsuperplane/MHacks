# ~ Andrew
# Provides a light-weight class representing a short clip of a video

class TimeStamp:
    # video_base_name is the name of the file without the extension (steve_jobs, instead of steve_jobs.wav)
    def __init__(self, video_base_name, begin_time, duration_time):
        self.video_base_name = video_base_name
        self.begin_time = begin_time
        self.duration_time = duration_time
