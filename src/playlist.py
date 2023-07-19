import os
from datetime import timedelta

import isodate
from googleapiclient.discovery import build

api_key: str = os.getenv('YOUTUBE_API')

youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id):
        self._playlist_id = playlist_id

    def get_info(self):
        playlist = youtube.playlists().list(id=self._playlist_id, part='snippet,contentDetails', maxResults=50)
        response = playlist.execute()
        return response

    @property
    def title(self):
        playlist_info = self.get_info()
        title = playlist_info['items'][0]['snippet']['title']
        return title

    @property
    def url(self):
        return f"https://www.youtube.com/playlist?list={self._playlist_id}"

    def get_videos(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self._playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        return video_response

    @property
    def total_duration(self):
        videos = self.get_videos()
        durations = timedelta(hours=0, minutes=0, seconds=0)
        for video in videos['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            durations += duration

        return durations

    def show_best_video(self):
        best_video = ''
        top_like_count = 0
        videos = self.get_videos()
        for video in videos['items']:
            if int(video["statistics"]["likeCount"]) > top_like_count:
                top_like_count = int(video["statistics"]["likeCount"])
                best_video = f"https://youtu.be/{video['id']}"

        return best_video
