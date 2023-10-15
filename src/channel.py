import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Метод для инициализации экземпляра"""
        channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        self.__channel_id = channel_id
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/channel/" + channel_id
        self.subscriber_count = channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.view_count = channel["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        """Метод возвращает название и ссылку на канал"""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """
        Метод для сложения кол-во подписчиков
        """
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """
        Метод для вычитания кол-во подписчиков
        """
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        """
        Метод для сравнения > кол-во подписчиков
        """
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """
        Метод для сравнения >= кол-во подписчиков
        """
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        """
        Метод для сравнения < кол-во подписчиков
        """
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """
        Метод для сравнения <= кол-во подписчиков
        """
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        """
        Метод для сравнения == кол-во подписчиков
        """
        return int(self.subscriber_count) == int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def to_json(self, path):
        json_data = {"channel_id": self.__channel_id,
                     "title": self.title,
                     "description": self.description,
                     "url": self.url,
                     "subscriber_count": self.subscriber_count,
                     "video_count": self.video_count,
                     "view_count": self.view_count}

        with open(path, "w", encoding="utf-8") as file:
            json.dump([json_data], file, ensure_ascii=False)

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return cls.youtube
