import requests
import json

def main():
    print('Enter Video ID: ')
    videoId = input()
    download_video(videoId)
    download_chat(videoId)

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
    

# Download video as video.mp4
def download_video(videoId):
    print('Downloading video for ' + videoId)
    
main()
