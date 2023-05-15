import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

api_key: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        try:
            video = youtube.videos().list(id=self.video_id, part='snippet,statistics').execute()
            if len(video["items"]) > 0:
                self.title = video["items"][0]['snippet']["title"]
                self.video_url = f"https://www.youtube.com/watch?v={self.video_id}"
                self.video_views = video['items'][0]['statistics']['viewCount']
                self.like_count = video['items'][0]['statistics']['likeCount']
            else:
                self.title = None
                self.video_url = None
                self.video_views = None
                self.like_count = None
        except HttpError:
            self.title = None
            self.video_url = None
            self.video_views = None
            self.like_count = None

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
