from fastapi import FastAPI
from contextlib import asynccontextmanager
from threading import Thread
from app.utils.queue_worker import (
    threaded_task_manager,
    task_queue
)

from app.models import DataBaseHelper
from app.models import Base
from config import settings

URL_COMPLETE = "http://localhost:8000/api/queue/taskcomplete/"

db_helper = DataBaseHelper(
        url=str(settings.db.url),
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(str(settings.db.url))
    threads: list[Thread] = threaded_task_manager(
        num_threads=settings.max_thread,
        url=URL_COMPLETE
    )
    yield
    for _ in range(settings.max_thread):
        task_queue.put(None)
    for thread in threads:
        thread.join()
    print("dispose engine")
    await db_helper.dispose()

app = FastAPI(lifespan=lifespan)

from app.api import api_router
app.include_router(api_router)


