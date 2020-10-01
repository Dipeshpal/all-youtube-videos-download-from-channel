from apiclient.discovery import build
from pytube import YouTube
from tqdm import tqdm
import os


class Youtube_API:
    def __init__(self):
        self.key = "AIzaSyDUTICBSWYX6pG6yWaaImZc_afvYXqOPWY"

        self.youtube = build('youtube', 'v3', developerKey=self.key)

    def get_channel_videos(self, channel_id):
        # get Uploads playlist id
        res = self.youtube.channels().list(id=channel_id,
                                      part='snippet, statistics, contentDetails').execute()
        try:
            playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        except:
            return 'Not'
        res_copy = res
        videos = []
        next_page_token = None

        while 1:
            res = self.youtube.playlistItems().list(playlistId=playlist_id,
                                               part='snippet',
                                               maxResults=50,
                                               pageToken=next_page_token).execute()
            videos += res['items']
            next_page_token = res.get('nextPageToken')

            if next_page_token is None:
                break

        return videos

    def get_all_videos_li(self, data):
        videos_list = []
        for i in range(len(data)):
            url = "https://www.youtube.com/watch?v=" + data[i]['snippet']['resourceId']['videoId']
            videos_list.append(url)
        return videos_list

    def download(self, url):
        if not os.path.exists('videos'):
            os.makedirs('videos')

        try:
            yt_obj = YouTube(url)
            yt_obj.streams.get_highest_resolution().download('videos/')
            # success_url_list.append(url)
            return True
        except Exception as e:
            return False


# object
obj = Youtube_API()
channel_id = input("Enter channel id: ")

if len(channel_id) == 0:
    # default channel
    channel_id = "UCGEoRAK92fUk2kY3kSJMR_Q"

# get videos list
data = obj.get_channel_videos(channel_id)
videos_list = obj.get_all_videos_li(data)


# download
success_ = []
fail_ = []
for i in tqdm(range(len(videos_list))):
    url = videos_list[i]
    status = obj.download(url)
    if status:
        success_.append(url)
    else:
        fail_.append(url)


print(f"Success: {len(success_)}, Fail: {len(fail_)}")
print("All fails list in 'fail_list.txt'")
with open('fail_list.txt', 'w') as f:
    for item in fail_:
        f.write("%s\n" % item)
