import os
from googleapiclient.discovery import build
import json


class Video:
    """Класс для видео с ютуба"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        """Метод для инициализации экземпляра"""
        video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()

        self.video_id = video_id
        self.title = video["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/watch?v={video_id}"
        self.view_count = video["items"][0]["statistics"]["viewCount"]
        self.like_count = video["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        """Возвращает наименование видео"""
        return self.title

    def __repr__(self):
        """Возвращает все аргументы экземпляра"""
        return (f"id = {self.video_id}, имя = {self.title}, "
                f"ссылка = { self.url}, просмотры = {self.view_count}, "
                f"лайки = {self.like_count}")

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.video_id).execute()

        print(json.dumps(video, indent=2, ensure_ascii=False))


class PLVideo(Video):
    """Класс для видео с плейлистом с ютуба"""
    def __init__(self, video_id, playlist_id):
        """Метод для инициализации экземпляра"""
        super().__init__(video_id)
        self.playlist_id = playlist_id
