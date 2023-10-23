import os
from googleapiclient.discovery import build
import json
import datetime


class PlayList:
    """Класс для плейлиста с ютуба"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        playlist = self.youtube.playlists().list(id=playlist_id,
                                                 part='snippet',
                                                 maxResults=50, ).execute()

        self.playlist_id = playlist_id
        self.title = playlist["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

    def __str__(self):
        """Возвращает имя плейлиста"""
        return self.title

    def __repr__(self):
        """Возвращает все свойства экземпляра"""
        return f"id = {self.playlist_id}, title = {self.title}, url = {self.url}"

    def get_video_ids(self):
        """Возвращает id всех видео из плейлиста в виде списка"""
        playlist = self.youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails',
                                                     maxResults=50, ).execute()["items"]
        video_ids = []

        for video in playlist:
            video_ids.append(video["contentDetails"]["videoId"])

        return video_ids

    @property
    def total_duration(self):
        """Возвращает длительность всего плейлиста"""
        video_ids = ",".join(self.get_video_ids())

        videos = self.youtube.videos().list(part='contentDetails',
                                            id=video_ids).execute()["items"]

        duration_playlist = datetime.timedelta()

        for video in videos:
            time = video["contentDetails"]["duration"]
            if "S" in time:
                time = datetime.datetime.strptime(time, "PT%MM%SS")
            elif "s" not in time:
                time = datetime.datetime.strptime(time, "PT%MM")

            duration_playlist += datetime.timedelta(minutes=time.minute, seconds=time.second)

        return duration_playlist

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста"""
        video_ids = ",".join(self.get_video_ids())

        videos = self.youtube.videos().list(part='statistics',
                                            id=video_ids).execute()["items"]

        popular_video_like = 0
        video_id = ""

        for video in videos:
            count_like = int(video['statistics']['likeCount'])
            if count_like > popular_video_like:
                popular_video_like = count_like
                video_id = video["id"]

        return f"https://youtu.be/{video_id}"

    def print_playlist_info(self):
        """Выводит в консоль информацию о плейлисте."""
        playlist = self.youtube.playlists().list(id=self.playlist_id,
                                                     part='snippet',
                                                     maxResults=50, ).execute()

        print(json.dumps(playlist, indent=2, ensure_ascii=False))
