import os
import json

from googleapiclient.discovery import build

api_key: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        video = youtube.videos().list(id=self.video_id, part='snippet,statistics').execute()
        self.video_title = video["items"][0]['snippet']["title"]
        self.video_url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.video_views = video['items'][0]['statistics']['viewCount']
        self.video_likes = video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.video_title}"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
