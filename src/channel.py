import json
import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YOUTUBE_API')

youtube = build('youtube', 'v3', developerKey=api_key)

class Channel:
    """Класс для ютуб канала"""


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала."""
        self.channel_id = channel_id


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics')
        response = channel.execute()
        print(json.dumps(response, indent=2, ensure_ascii=False))
