import yt_dlp
from celery import Task
from youtubesearchpython import VideosSearch

from typing import Callable
from abc import ABC, abstractmethod

from src.utils.files import place_for_download, zip
from src.database.config import celery_app

import os

@celery_app.task(bind=True, name="youtube_downloader_class")
def youtube_downloader(
    self,
    query: list[str],
    audioformat: str,
    quality: str
    ) -> str:
    """Performs a task"""
    outtmpl = place_for_download()
    urls = search_track(query)

    with yt_dlp.YoutubeDL(
    {
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': audioformat,
        'preferredquality': quality,
            }
        ],
        'outtmpl': os.path.join(outtmpl, "%(title)s.%(ext)s"),
    }
        ) as dl:
        dl.download(urls)
        
    return zip(outtmpl)

def search_track(query: list[str]) -> list[str]:
    """Searches for a track in the YouTube database"""
    extracted_links = []

    for q in query:
        videosSearch = VideosSearch(q, limit = 1)
        videoresult = videosSearch.result()["result"][0]["link"]

        extracted_links.append(videoresult)
    return extracted_links