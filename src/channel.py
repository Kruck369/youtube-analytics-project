import os
import json

from googleapiclient.discovery import build

api_key: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.total_views = channel["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Получение объекта для работы с API вне класса."""
        return youtube

    @property
    def channel_id(self):
        """Геттер для id канала."""
        return self.__channel_id

    def to_json(self, filename):
        """Выводит информацию с атрибутами класса в файл .json"""
        channel = Channel(self.channel_id)
        with open(filename, 'a', encoding='utf-8') as f:
            if os.stat(filename).st_size == 0:
                json.dump([channel.__dict__], f, ensure_ascii=False, indent=1)
            else:
                pass
