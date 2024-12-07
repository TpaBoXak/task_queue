from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.schemas.task import (
    TaskBaseSchema,
    TaskSchema
)
from app.models.task import (
    Task,
    TaskStatus
)
from app import db_helper


async def add_task(session: AsyncSession, task_info: TaskBaseSchema) -> Optional[int]:
    try:
        task: Task = Task()
        task.title = task_info.title
        task.status_id = 1
        session.add(task)
    except:
        await session.rollback()
        return None
    else:
        await session.commit()
        # await session.refresh(task)
        return task.id
    

async def get_task(
    session: AsyncSession,
    task_id: int
) -> Optional[TaskSchema]:
    stmt = select(
        Task.title,
        TaskStatus.title,
        Task.create_time,
        Task.start_time,
        Task.exec_time
    ).select_from(Task). \
    where(Task.id == task_id). \
    join(TaskStatus, Task.status_id == TaskStatus.id)

    result = await session.execute(statement=stmt)
    task: tuple = result.first()

    if not task:
        return None
    
    return TaskSchema(
        title=task[0],
        status=task[1],
        create_time=task[2],
        start_time=task[3],
        time_to_execute=task[4]
    )


async def get_title_create(
    session: AsyncSession,
    task_id: int
) -> tuple[datetime, int]:
    stmt = select(Task.title, Task.create_time).where(Task.id == task_id)
    result = await session.execute(statement=stmt)
    task_info = result.first()
    return task_info
    

async def complet_task(
    session: AsyncSession,
    task_id: int,
    time_to_exec: int,
    time_start: datetime
) -> bool:
    try:
        task: Task = await session.get(Task, task_id)
        task.status_id = 2
        task.start_time = time_start
        task.exec_time = time_to_exec
        session.add(task)
    except:
        await session.rollback()
        return False
    else:
        await session.commit()
        return True