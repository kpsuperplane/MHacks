# ~ Andrew
# Provides a light-weight class representing a short clip of a video

class TimeStamp:
    # video_base_name is the name of the file without the extension (steve_jobs, instead of steve_jobs.wav)
    def __init__(self, video_base_name, begin_time, duration_time):
        self.video_base_name = video_base_name
        self.begin_time = begin_time
        self.duration_time = duration_time

    def getDuration(self):
        return self.duration_time
    
    def getBegin(self):
        return self.begin_time
    
    def getName(self):
        return self.video_base_name

    # Returns a string interpretation of this to store in a .txt file
    def toString(self):
        return self.video_base_name + " " + str(self.begin_time) + " " + str(self.duration_time)


# Inverts TimeStamp.toString
def stringToTimeStamp(s):
    args = s.split(" ")
    video_base_name = args[0]
    begin_time, duration_time = float(args[1]), float(args[2])
    return TimeStamp(video_base_name,begin_time,duration_time)
