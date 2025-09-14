from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.downloader.routes import dn_router
from src.database.config import celery_app

app = FastAPI()

app.include_router(dn_router)

@app.get("/")
def show_index():
    return FileResponse('/app/src/static/index.html')
