import requests
import json
import youtube_dl
from moviepy.editor import *
import os
from tkinter import filedialog
from tkinter import *
import shutil
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import math
'''
def main():

    #folder_path
    #save_name
    #input_url
    #time_length

    videoId = input('Enter Twitch Url')
    #Uses videoID as a link
    download_video(videoId)
    
    #download_chat(videoId)
    
    if os.path.exists('sound.mp3'):
        os.remove('sound.mp3')
    #------------This needs to be worked on: says that a process is open, so it can not delete video----------
    #if os.path.exists('VODEdited.mp4'):
        #os.remove('VODEdited.mp4')
    if os.path.exists('VOD.mp4'):
        os.remove('VOD.mp4')
'''
#------------------------GUI------------------------------
def start():
    # Start downloading and everything else
    # Globals are printed below for debug and informational purposes.
    
    #---Variables---
    #folder_path
    #save_name
    #input_url
    #time_length

    #Uses videoID as a link
    download_video(input_url.get(), clipTimes)
    download_chat(input_url.get())

    #initalized 2d array for start and end time
    clipTimes = analyze()
    
    if os.path.exists('sound.mp3'):
        os.remove('sound.mp3')
    #This needs to be worked on: says that a process is open, so it can not delete video
    #if os.path.exists('VODEdited.mp4'):
        #os.remove('VODEdited.mp4')
    if os.path.exists('VOD.mp4'):
        os.remove('VOD.mp4')

    
    #move to desired directory
    shutil.move(save_name + '.mp4' , folder_path)
    
def analyze():
    with open('chat.json') as json_file:
        data = json.load(json_file)
    
    #last comment shows how long the VOD is
    length = data[-1]['content_offset_seconds']
    output = []

    #sample positive sentiment comments over every minute
    for i in range(math.ceil(length/60)):
        min = i * 60
        max = min + 60
        messages = []
        for comment in data:
            if comment['content_offset_seconds'] > min and comment['content_offset_seconds'] < max:
                messages.append(comment['message']['body'])
        
        X_new_counts = count_vect.transform(messages)
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)
        predicted = clf.predict(X_new_tfidf)
        output.append(sum(predicted))
        messages.clear()

    #Top 10 moments sorted cronologically
    #https://stackoverflow.com/questions/13070461/get-indices-of-the-top-n-values-of-a-list
    top = sorted(sorted(range(len(output)), key=lambda i: output[i], reverse=True)[:10])

    timelist = []
    for index in top:
        newlist = []
        start = index * 60
        end = start + 60
        newlist.append(start)
        newlist.append(end)
        timelist.append(newlist)
    return timeList

def start_button():
    #Saves all the globals that are currently in the fillable boxes
    clear_labels()
    global save_name
    save_name.set(SaveFileNameTxt.get())
    global folder_path
    folder_path.set(SaveDestTxt.get())
    global input_url
    input_url.set(URLtxt.get())
    global time_length
    safe = spinbox.get().isdecimal()
    if safe:
        time_length.set(spinbox.get())
    else:
        sanitize_time_length_failed()

    if safe and handle_folder_path_check() and handle_time_length_check() and handle_input_url_check() and handle_save_name_check():
        lbl5.config(text="Correct Settings: Starting")
        clear_labels()
        start()
    else:
        lbl5.config(text="Incorrect Settings")


def handle_folder_path_check():
    if os.path.isdir(folder_path.get()):
        lbl6.config(text="Correct Path")
        return True
    lbl6.config(text="Incorrect Path")
    return False


def handle_save_name_check():
    if len(save_name.get()) == 0:
        lbl7.config(text="Invalid Name")
        return False
    lbl7.config(text="Valid Name")
    return True


def sanitize_time_length_failed():
    lbl6.config(text="Length contains non-number")


def handle_time_length_check():
    if 0 < time_length.get() <= 30:
        lbl8.config(text="Valid Length")
        return True
    lbl8.config(text="Invalid Length")
    return False


def handle_input_url_check():
    lbl8.config(text="Valid URL")
    return True


def clear_labels():
    lbl6.config(text="")
    lbl7.config(text="")
    lbl8.config(text="")
    lbl9.config(text="")


def browse_button():
    # Allow user to select a directory and store it in global var called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    set_text_input(filename)


def set_text_input(text):
    SaveDestTxt.delete(0, "end")
    SaveDestTxt.insert(0, text)

window = Tk()
window.title("Vod Downloader App")
window.geometry('500x300')

folder_path = StringVar()
save_name = StringVar()
input_url = StringVar()
time_length = IntVar()


lbl1 = Label(window, text="Input URL:", anchor="w", justify=LEFT, width=23)
lbl1.grid(row=0, column=0)
URLtxt = Entry(window,width=45)
URLtxt.grid(row=0, column=1)

lbl2 = Label(window, text="Target video length(minutes):", anchor="w", justify=LEFT, width=23)
lbl2.grid(row=1, column=0)
spinbox = Spinbox(window, from_=1, to=30, width=5)
spinbox.grid(row=1, column=1)

lbl3 = Label(window, text="Output Destination:", anchor="w", justify=LEFT, width=23)
lbl3.grid(row=2, column=0)
SaveDestTxt = Entry(window,width=45)
SaveDestTxt.grid(row=2, column=1)
SaveDestTxt.delete(0, "end")
SaveDestTxt.insert(0, "Click Browse to select a destination to save your file!")
browse = Button(text="Browse", command=browse_button)
browse.grid(row=2, column=2)

lbl4 = Label(window, text="File Name:", anchor="w", justify=LEFT, width=23)
lbl4.grid(row=3, column=0)
SaveFileNameTxt = Entry(window,width=45)
SaveFileNameTxt.grid(row=3, column=1)

lbl5 = Label(window, text="", width=23)
lbl5.grid(row=4, column=0)
StartButton = Button(text="Start", command=lambda: start_button())
StartButton.grid(row=4, column=1)

lbl6 = Label(window, text="", width=23)
lbl6.grid(row=5, column=0)

lbl7 = Label(window, text="", width=23)
lbl7.grid(row=6, column=0)

lbl8 = Label(window, text="", width=23)
lbl8.grid(row=7, column=0)

lbl9 = Label(window, text="", width=23)
lbl9.grid(row=7, column=0)

#--------------------End GUI-----------------------


#---------Download video as chat.json----------
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

# Download video as video.mp4
def download_video(videoId, time):
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

    #Code for a double array time[cliptimes][0] (start time) time[cliptimes][1] (end time) 
    '''
    for clipTimes in range(len(time[clipTimes])):
        clips = video.subclip(time[clipTimes][0],time[clipTimes][1])
        audio_clips = audio.subclip(start,end)

        video_array.append(clips) #creates an array for all clips
        audio_array.append(audio_clips)
    '''
    # Test peaks at 5min 10 min 15 min that last 1/2 a minute each
    x = 0
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

    #Attempt to close all possible opened files
    while not video_array is None:
        video_array.pop
        audio_array.pop

    #exports both tmp files files
    audio.write_audiofile('sound.mp3')
    video.write_videofile('VODEdited.mp4')

    #Calls files exported to combine the audio and video
    final = VideoFileClip('VODEdited.mp4')
    final = final.set_audio(AudioFileClip('sound.mp3'))
    final.write_videofile(save_name + '.mp4')

    
    clips.close()
    final.close()
    video.close()
    audio.close()

mainloop()