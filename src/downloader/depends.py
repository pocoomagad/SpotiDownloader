from typing import Annotated

from fastapi import Depends

from src.downloader.strategies import SpotifyDownloadStrategy
from src.auth.config import spotify
from src.tasks.tasks import youtube_downloader
from src.tasks.manager import TaskManager

def spotify_download_strategy():
    return SpotifyDownloadStrategy(youtube_downloader, spotify)

SpotifyDownloadStrategyDep = Annotated[SpotifyDownloadStrategy, Depends(spotify_download_strategy)]

def task_manager():
    return TaskManager()

TaskManagerDep = Annotated[TaskManager, Depends(task_manager)]