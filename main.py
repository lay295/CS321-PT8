import requests
import json
import youtube_dl
import os
from moviepy.editor import *

def main():
    print('Enter Video ID: ')
    videoId = input()
    download_video(videoId)
    download_chat(videoId)

    if os.path.exists('sound.mp3'):
        os.remove('sound.mp3')
    #------------This needs to be worked on: says that a process is open, so it can not delete video----------
    #if os.path.exists('VODEdited.mp4'):
        #os.remove('VODEdited.mp4')
    if os.path.exists('VOD.mp4'):
        os.remove('VOD.mp4')

# Download video as chat.json
def download_chat(videoId):
    print('Downloading chat for ' + videoId)
    comments = []
    done = False
    cursor = ''

    while done is False:
        requestUrl = 'https://api.twitch.tv/v5/videos/' + videoId + '/comments?' + ('content_offset_seconds=0' if comments.count == 0 else 'cursor=' + cursor)
        response = requests.get(
            requestUrl,
            headers={
                'Accept': 'application/vnd.twitchtv.v5+json; charset=UTF-8',
                'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko'
            }
        )
        json_response = response.json()
        for comment in json_response['comments']:
            comments.append(comment)
        if "_next" in json_response:
            cursor = json_response['_next']
        else:
            done = True
    chatFile = open("chat.json", "w")
    chatFile.write(json.dumps(comments))
    chatFile.close()
    

# Download video as video.mp4
def download_video(videoId):
    print('Downloading video for ' + videoId)
    print('Downloading video for ' + videoId)

    ydl_opts = { 
        'format' : 'mp4',
        'outtmpl' : 'VOD.mp4'
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
       ydl.download([videoId])

    #Variable array to store videoclips
    video = VideoFileClip('VOD.mp4')  #clip that is saved
    audio = AudioFileClip('VOD.mp4')
    video_array = []
    audio_array = []

    #Start and end time for the clip in seconds
    #NOTE: does not work with a 0 second start time
    start = 300
    end = 310

    # Test peaks at 5min 10 min 15 min that last 1/2 a minute each
    for x in range(3): #Change for loop to match comment peak times
        clips = video.subclip(start,end)
        audio_clips = audio.subclip(start,end)

        video_array.append(clips) #creates an array for all clips
        audio_array.append(audio_clips)

        #Adds 5 min for clip difference
        start += (300) 
        end += (300)
    
    
    #Creates tmps of the combined audio and video files
    video = concatenate_videoclips(video_array)
    audio = concatenate_audioclips(audio_array)

    #exports both tmp files files
    audio.write_audiofile('sound.mp3')
    video.write_videofile('VODEdited.mp4')

    #Calls files exported to combine the audio and video
    final = VideoFileClip('VODEdited.mp4')
    final = final.set_audio(AudioFileClip('sound.mp3'))
    final.write_videofile('final_version.mp4')

    audio_clips.close()
    clips.close()
    final.close()
    video.close()
    audio.close()
    
main()
