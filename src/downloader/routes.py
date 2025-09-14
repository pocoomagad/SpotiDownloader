from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse, FileResponse

import os

from src.downloader.depends import SpotifyDownloadStrategyDep, TaskManagerDep

dn_router = APIRouter()

@dn_router.post(
    "/spotify/audio",
    response_class=JSONResponse,
    description="Add task to download spotify audio by url",
    summary="Add task",
    status_code=202
    )
async def add_download_task(
    url: str,
    audioformat: str,
    quality: str,
    strategy: SpotifyDownloadStrategyDep
):
    return strategy.download(spotify_url=url, download_parameters=(audioformat, quality))

@dn_router.get(
    "/tasks/{task_id}",
    response_class=JSONResponse,
    description="Get status of task",
    summary="Status",
    status_code=200
    )
async def get_track_status(task_id: str, task_manager: TaskManagerDep):
    task_response = task_manager.get_task_response(task_id)
    result = task_response["result"]
    if result:
        filename = os.path.basename(result)

        return FileResponse(
            result,
            media_type='application/octet-stream', 
            filename=filename, 
            headers={
                "Content-Disposition": f"attachment; filename={filename}"}
        )
    return task_response