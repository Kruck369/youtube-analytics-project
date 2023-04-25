import os
import json

from googleapiclient.discovery import build
CHANNEL_INFO = 'channel_info.json'


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        with open(CHANNEL_INFO, 'a', encoding='utf-8') as f:
            if os.stat(CHANNEL_INFO).st_size == 0:
                json.dump([channel], f, ensure_ascii=False)
            else:
                with open(CHANNEL_INFO, encoding='utf-8') as f:
                    channel_list = json.load(f)
                    for i in range(0,):
                        if self.channel_id not in channel_list[i]['items']:
                            pass
                        else:
                            channel_list.append(channel)
                with open(CHANNEL_INFO, 'w', encoding='utf-8') as f:
                    json.dump(channel_list, f, ensure_ascii=False, indent=2)
        print(json.dumps(channel, indent=2, ensure_ascii=False))


