from pydantic_settings import BaseSettings, SettingsConfigDict
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

class Oauth2Settings(BaseSettings):
    CLIENT_SECRET: str
    CLIENT_ID: str

    model_config = SettingsConfigDict(env_file="src/env/auth.env")

settings = Oauth2Settings()

spotify = Spotify(
    oauth_manager=SpotifyClientCredentials(
        client_id=settings.CLIENT_ID, 
        client_secret=settings.CLIENT_SECRET
    )
)