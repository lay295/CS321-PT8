def main():
    print('Enter Video ID: ')
    videoId = input()
    download_video(videoId)
    download_chat(videoId)

# Download video as chat.json
def download_chat(videoId):
    print('Downloading chat for ' + videoId)

# Download video as video.mp4
def download_video(videoId):
    print('Downloading video for ' + videoId)
    
main()