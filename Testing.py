from moviepy.editor import *
import youtube_dl

#This downlaods the file:
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
       ydl.download(['https://www.twitch.tv/videos/954748026'])

# a & b are the seconds in the video clips. A = starttime b= endtime
a = 60*5
b = 65*5
#empty array to store files
video = []
for x in range(3): # for loop to create 3 clips
   result = VideoFileClip("VideoBitch.mp4").subclip(a,b)  #clip that is saved
   video.append(result) #creates an array for all clips
   result.close()
   a += 60*5   #new starttime
   b += 65*5   #new endtime

tmpvideo =  concatenate_videoclips(video)
tmpvideo = VideoFileClip("VideoBitch.mp4").subclip(600,660)

tmpvideo.write_videofile("StreamEdited.mp4",fps=30, audio = True) # Many options...

