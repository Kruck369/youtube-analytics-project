import isodate
import datetime
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:

    def __init__(self, playlist_id):
        """Инициилизуруем класс по ID"""
        self.playlist_id = playlist_id
        playlist = youtube.playlists().list(id=self.playlist_id, part='snippet,contentDetails').execute()
        self.title = playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.playlist_items = []
        playlist = youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails').execute()
        self.playlist_items += playlist['items']

    @property
    def total_duration(self):
        """Определяет общую продолжительность плейлиста"""
        total_duration = 0
        for item in self.playlist_items:
            video_id = item['contentDetails']['videoId']
            video = youtube.videos().list(part='contentDetails', id=video_id).execute()
            duration = video['items'][0]['contentDetails']['duration']
            total_duration += isodate.parse_duration(duration).total_seconds()
        return datetime.timedelta(seconds=total_duration)

    def show_best_video(self):
        """Определяет видео с наибольшим количеством лайков"""
        video_dict = {}
        for item in self.playlist_items:
            video_id = item['contentDetails']['videoId']
            video_response = youtube.videos().list(part='statistics', id=video_id).execute()
            for video in video_response['items']:
                video_id = video['id']
                video_likes = video['statistics']['likeCount']
                video_dict[video_id] = int(video_likes)
        most_liked = max(video_dict, key=video_dict.get)
        return f"https://youtu.be/{most_liked}"
