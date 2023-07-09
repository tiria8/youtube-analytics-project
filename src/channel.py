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

    def get_info(self):
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics')
        response = channel.execute()

        return response
    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        info = self.get_info
        print(json.dumps(info, indent=2, ensure_ascii=False))

    @property
    def title(self):
        channel_info = self.get_info()
        self.title = channel_info['items']['snippet']['title']

    @property
    def description(self):
        channel_info = self.get_info()
        self.description = channel_info['items']['snippet']['description']

    @property
    def url(self):
        channel_info = self.get_info()
        self.url = channel_info['items']['snippet']['thumbnails']['url']

    @property
    def subscriber_count(self):
        channel_info = self.get_info()
        self.subscriber_count = channel_info['items']['statistics']['subscriberCount']

    @property
    def video_count(self):
        channel_info = self.get_info()
        self.video_count = channel_info['items']['statistics']['videoCount']

    @property
    def view_count(self):
        channel_info = self.get_info()
        self.view_count = channel_info['items']['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename):
        with open(filename, "w") as file:
            data = {
                "id": self.channel_id,
                "title": self.title,
                "description": self.description,
                "url": self.url,
                "subscriber_count": self.subscriber_count,
                "video_count": self.video_count,
                "view_count": self.view_count
            }
            json.dump(data, file)


