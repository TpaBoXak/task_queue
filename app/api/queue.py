from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from typing import Optional
from typing import Annotated
from fastapi import Header

from config import settings
from app import db_helper
from app.schemas.task import (
    TaskBaseSchema,
    TaskSchema,
    TaskCompletionRequest
)
from app.schemas.responses import SuccessResponse
import app.dao.task as task_dao
from app.utils.queue_worker import (
    task_queue,
    get_run_task
)


router: APIRouter = APIRouter(prefix=settings.api.queue_prefix)

@router.post(
    "/addtask",
    responses={
        200: {"model": SuccessResponse, "description": "Успешный ответ"},
        500: {"description": "Ошибка сервера при добавлении данных"}
    },
)
async def add_rate(
    task_info: TaskBaseSchema,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Добавляет задачу
    """
    task_id: Optional[None] = await task_dao.add_task(session=session,
            task_info=task_info)
    if not task_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error, task title: {task_info.title}",
        )
    task_queue.put((task_id, task_info.title))

    return SuccessResponse(message=f"Task successfully added with id {task_id}")

@router.get(
    "/gettask",
    responses={
        200: {"model": TaskSchema, "description": "Успешный ответ"},
        500: {"description": "Ошибка сервера при выгрузке данных"}
    },
)
async def add_rate(
    task_id: Annotated[int, Header()],
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Выгружает информацию по задаче
    """
    task_info = await get_run_task(task_id=task_id)
    if task_info:
        title, create_time = await task_dao.get_title_create(
            session=session,
            task_id=task_id
        )
        return TaskSchema(
            title=title,
            status="Run",
            create_time=create_time,
            start_time=task_info[0],
            time_to_execute=task_info[1]
        )
    
    task_schema: TaskSchema = await task_dao.get_task(
        session=session,
        task_id=task_id
    )
    if not task_schema:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error, task id: {task_id}",
        )
    return task_schema

@router.put(
    "/taskcomplete/",
    responses={
        200: {"model": SuccessResponse, "description": "Успешный ответ"},
        403: {"description": "Ошибка прав доступа"},
        500: {"description": "Ошибка сервера при обновлении данных"}
    },
)
async def complete_task(
    task_compl: TaskCompletionRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    x_internal_request: Optional[str] = Header()
):
    if x_internal_request != settings.secret_key:
        raise HTTPException(status_code=403, detail="Forbidden")
    result: bool = await task_dao.complet_task(
        session=session,
        task_id=task_compl.task_id,
        time_start=task_compl.time_start,
        time_to_exec=task_compl.time_to_exec
    )
    if not result:
        HTTPException(
            status_code=500,
            detail=f"Unable to complete task {task_compl.task_id}"
        )
    return {"message": "Task completed successfully"}
