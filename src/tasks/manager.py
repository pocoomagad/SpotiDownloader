from abc import ABC, abstractmethod

from fastapi import HTTPException

from src.database.config import celery_app

class AbstractTaskManager(ABC):
    @abstractmethod
    def get_task_response(self, task_id: int):
        ...

    @abstractmethod
    def cancel_task(self, task_id: int):
        ...

class TaskManager(AbstractTaskManager):
    def get_task_response(self, task_id: str, as_tuple: bool = False, as_list: bool = False):
        """Get task response as json, if task is faliled,
        throws error"""

        TaskFailedException = HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "error": "task failed",
                "msg": "please try later"
            }
        )

        task_response = celery_app.AsyncResult(task_id)

        if sum([as_tuple, as_list]) > 1:
            raise ValueError("Only one return format can be specified: as_tuple or as_list")

        state = task_response.state
        result = task_response.result
        failed = task_response.failed()

        response_json = {
            "state": state,
            "result": result
        }

        if as_list:
            response_json.update(
                {"result": task_response.as_list()}
            )
        elif as_tuple:
            response_json.update(
                {"result": task_response.as_tuple()}
            )
        else:
            if not failed:
                return response_json
            raise TaskFailedException

    def cancel_task(self, task_id: int):
        task = celery_app.AsyncResult(task_id)
        return task.revoke()