from apiclient.discovery import build
from pytube import YouTube
from tqdm import tqdm
import os
import json
import datetime


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
        dict_data = {}
        for i in range(len(data)):
            title = str(len(data) - i) + ' ' + str(data[i]['snippet']['publishedAt'][:-10]) + ' ' + data[i]['snippet'][
                'title']
            url = "https://www.youtube.com/watch?v=" + str(data[i]['snippet']['resourceId']['videoId'])
            dict_data[title] = url
        return dict_data

    def download(self, title, url, most_recent):
        if not os.path.exists('videos'):
            os.makedirs('videos')

        try:
            if not most_recent:
                if os.path.exists(f'videos/{title}'):
                    return True
            yt_obj = YouTube(url)
            yt_obj.streams.get_highest_resolution().download(f'videos/{title}')
            return True
        except Exception as e:
            return False

    def check_n_download(self, date, videos):

        # delete corrupt videos
        all_existing_videos = os.listdir("videos")
        all_existing_videos = [int(i.split(' ')[0]) for i in all_existing_videos]
        most_recent_video = str(min(all_existing_videos))

        # download
        print("Downloading...")
        success_ = {}
        fail_ = {}
        for i in tqdm(range(len(videos))):
            title = list(videos.keys())[i]
            url = list(videos.values())[i]

            if most_recent_video in title:
                status = self.download(title, url, True)
            else:
                status = self.download(title, url, False)
            if status:
                success_[title] = url
            else:
                fail_[title] = url
        with open(f'{date}-{"success_download.json"}', 'w') as json_file:
            json.dump(success_, json_file, indent=4)
        with open(f'{date}-{"fail_download.json"}', 'w') as json_file:
            json.dump(fail_, json_file, indent=4)
        print(f"{len(success_)} Successfully Downloaded")
        print(f"{len(fail_)} Fail to Download")
        print(f"'success_download.json' and 'fail_download.json' Created")
        print("Rerun script to check non existing download")


def start():
    obj = Youtube_API()
    channel_id = input("Enter Channel ID: ")
    if len(channel_id) == 0:
        channel_id = "UCGEoRAK92fUk2kY3kSJMR_Q"
    file_name = "total_videos.json"

    date = datetime.datetime.today().strftime("%Y-%m-%d")

    if not os.path.exists(date+'-'+file_name):
        # get videos list
        data = obj.get_channel_videos(channel_id)
        videos = obj.get_all_videos_li(data)
        with open(f'{date}-{file_name}', 'w') as json_file:
            json.dump(videos, json_file, indent=4)
        print(f"{len(videos)} Fetched")
    else:
        with open(f'{date}-{file_name}', 'r') as json_file:
            videos = json.load(json_file)
        print(f"{len(videos)} Videos Already Exist till {date} ")
        print("Checking if any missing videos...")
        obj.check_n_download(date, videos)


if __name__ == '__main__':
    start()
