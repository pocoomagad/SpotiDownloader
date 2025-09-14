import re
from abc import ABC, abstractmethod
from typing import Callable, Any

from fastapi import HTTPException

from spotipy import Spotify
from celery import Task

class AbstractStrategy(ABC):
    @abstractmethod
    def download(*args, **kwargs):
        ...

class SpotifyDownloadStrategy(AbstractStrategy):
    """Spotify download strategy class"""

    def __init__(self, downloader: Task, spotify_client: Callable):
        self.downloader = downloader
        self.spotify_client = spotify_client

        self.regex = regex = {
            r'^https://open\.spotify\.com/playlist/[a-zA-Z0-9]+(\?si=.+)?$': "playlist",
            r'^https://open\.spotify\.com/album/[a-zA-Z0-9]+(\?si=.+)?$': "album",
            r'^https://open\.spotify\.com/track/[a-zA-Z0-9]+(\?si=.+)?$': "track"
        }

    def download(self, spotify_url: str, download_parameters: tuple) -> dict:
            """
            Creates a task in Celery and sends 
            a task ID to track the task status

            :params 
            :spotify_url url of track, album, playlist
            :download_parameters parameters for downloader
            :return: dict
            """

            audio_json = self._get(spotify_url)
            queries = self._create_queries(audio_json)
            task = self.downloader.apply_async(
                args=[
                queries,
                *download_parameters
                ]
            )
            return {
                "task_id": task.id,
                "audio_data": audio_json["data"]
            }
                
    def _get(self, spotify_url: str) -> dict[Any]:
        """
        Checks the validity of the link 
        and if it is valid sends information about the resource 
        by contacting the Spotify client, 
        otherwise throws an error
        
        :params
        :spotify url url for get data
        :return: dict[Any]
        """
        InvalidUrlFormError = HTTPException(
            status_code=400, 
            detail={
                "status": "error",
                "error": "invalid url form",
                "msg": "enter another url"
            }
        )

        for pattern, url_type in self.regex.items():
            if re.match(pattern, spotify_url):
                content_type = url_type
                break
        else:
            raise InvalidUrlFormError


        if content_type == "track":
            track_data = self.spotify_client.track(spotify_url)
            return {
                "type": "track",
                "data": track_data,
                "tracks": [track_data]
            }

        elif content_type == "playlist":
            playlist_data = self.spotify_client.playlist(spotify_url)
            return {
                "type": "playlist",
                "data": playlist_data,
                "tracks": [item['track'] for item in playlist_data['tracks']['items'] 
                        if item['track'] is not None]
            }

        elif content_type == "album":
            album_data = self.spotify_client.album_tracks(spotify_url)
            return {
                "type": "album",
                "data": album_data,
                "tracks": album_data['items']
            }  

    def _create_queries(self, audio_json: dict) -> list[str]:
        """
        Create queries for downloader in list
        :params
        :audio_json dict object of audio data
        :return: list of query
        """
        
        tracks = audio_json.get("tracks", [])
        queries = []

        for track in tracks:
            if track:
                query = self._create_query(track)
                queries.append(query)

        return queries

    @staticmethod
    def _create_query(track: dict) -> str:
        """
        Create query for download by downloader
        :param
        :track info about track
        :return: query
        """

        performers = ""
        music = track['name']
        for names in track['artists']:
            performers = performers + names['name'] + ", "
        performers = performers.rstrip(", ")
        result_query = f'{performers} - {music}'
        return result_query