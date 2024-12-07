import queue
from random import randint
from datetime import datetime
import httpx
import time
import threading


SECRET_KEY = "secret_token"
task_queue = queue.Queue()
task_run: dict[int, tuple[datetime, int]] = {}

def process_task(task_id: str, url):        
        time_to_execute = randint(0, 10)
        time_start = datetime.now()
        task_run[task_id] = (time_start, time_to_execute)
        time.sleep(time_to_execute)
        with httpx.Client() as client:
            print(task_run)
            response = client.put(
            url=url,
            headers={"X-Internal-Request": SECRET_KEY},
            json={
                "task_id": task_id,
                "time_start": time_start.isoformat(),
                "time_to_exec": time_to_execute
            }
        )
            if response.status_code == 200:
                print("Task completed successfully")
            else:
                print(f"Failed to complete task")


def queue_worker(url):
    while True:
        with threading.Lock():
            task = task_queue.get()
        if task is None:
            break
        try:
            process_task(task_id=task[0], url=url)
        finally:
            task_queue.task_done()
            task_run.pop(task[0])
        

def threaded_task_manager(num_threads: int, url: str) -> list[threading.Thread]:
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=queue_worker, args=(url,))
        thread.start()
        threads.append(thread)
    return threads
        

async def get_run_task(task_id: int) -> tuple[datetime, int]:
    return task_run.get(task_id)