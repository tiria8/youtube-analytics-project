import json
import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YOUTUBE_API')

youtube = build('youtube', 'v3', developerKey=api_key)

class Channel:
    """Класс для ютуб канала"""
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала."""

        self.__channel_id = channel_id

    def get_info(self):
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics')
        response = channel.execute()
        return response

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        data = self.get_info()
        print(json.dumps(data, indent=2, ensure_ascii=False))

    @property
    def title(self):
        channel_info = self.get_info()
        title = channel_info['items'][0]['snippet']['title']
        return title

    @property
    def description(self):
        channel_info = self.get_info()
        description = channel_info['items'][0]['snippet']['description']
        return description

    @property
    def url(self):
        return f"https://www.youtube.com/channel/{self.__channel_id}"

    @property
    def subscriber_count(self):
        channel_info = self.get_info()
        subscriber_count = channel_info['items'][0]['statistics']['subscriberCount']
        return subscriber_count

    @property
    def video_count(self):
        channel_info = self.get_info()
        video_count = channel_info['items'][0]['statistics']['videoCount']
        return video_count

    @property
    def view_count(self):
        channel_info = self.get_info()
        view_count = channel_info['items'][0]['statistics']['viewCount']
        return view_count

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename):
        with open(filename, "w") as file:
            data = {
                "id": self.__channel_id,
                "title": self.title,
                "description": self.description,
                "url": self.url,
                "subscriber_count": self.subscriber_count,
                "video_count": self.video_count,
                "view_count": self.view_count
            }
            json.dump(data, file)


