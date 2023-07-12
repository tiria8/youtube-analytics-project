import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YOUTUBE_API')

youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id: str) -> None:
        self.__video_id = video_id

    def __str__(self):
        return f"{self.title}"

    def get_info(self):
        video = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=self.__video_id)
        response = video.execute()
        return response

    @property
    def title(self):
        video_info = self.get_info()
        title = video_info['items'][0]['snippet']['title']
        return title

    @property
    def url(self):
        return f"https://www.youtube.com/watch?v={self.__video_id}"

    @property
    def view_count(self):
        video_info = self.get_info()
        view_count = video_info['items'][0]['statistics']['viewCount']
        return view_count

    @property
    def like_count(self):
        video_info = self.get_info()
        like_count = video_info['items'][0]['statistics']['likeCount']
        return like_count


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    def get_video_ids(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.__playlist_id, part='contentDetails',
                                                       maxResults=50)
        response = playlist_videos.execute()
        return response

    def get_video(self):
        playlist_videos = self.get_video_ids()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        if self.__video_id not in video_ids:
            print('Видео не найдено')

        return self.get_info()

