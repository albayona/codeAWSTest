import asyncio
from concurrent.futures.process import ProcessPoolExecutor
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Dict
from uuid import UUID, uuid4
from fastapi.middleware.cors import CORSMiddleware

import requests
from fastapi import BackgroundTasks, HTTPException
from fastapi import FastAPI
from fastapi import Request
from pydantic import BaseModel, Field

from utils import NLPScraper
from utils.NLPScraper import cpu_bound_func_scrape


class Job(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    status: str = "in_progress"
    result: int = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.executor = ProcessPoolExecutor(3)
    yield
    app.state.executor.shutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,  # Allows cookies to be included in cross-origin requests
    allow_methods=["*"],     # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],     # Allows all headers
)

jobs: Dict[UUID, Job] = {}

async def run_in_process(fn, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(app.state.executor, fn, *args)  # wait and return result


async def start_cpu_bound_task(uid: UUID, param: int, user: str) -> None:
    jobs[uid].result = await run_in_process(cpu_bound_func_scrape, param, user)
    jobs[uid].status = "complete"
    publish_to_api(user, param)



@app.post("/scrape/{param}", status_code=HTTPStatus.ACCEPTED)
async def scrape_task_handler(param: str, background_tasks: BackgroundTasks, request: Request):
    user = request.headers.get('X-Consumer-Custom-Id')

    if not user:
        raise HTTPException(status_code=400, detail="X-Consumer-Custom-Id header missing")

    new_task = Job()
    jobs[new_task.uid] = new_task
    background_tasks.add_task(start_cpu_bound_task, new_task.uid, param, user)
    return new_task


@app.get("/status/{uid}")
async def status_handler(uid: UUID):
    return jobs[uid]


@app.post("/login/")
def login():
    try:
        NLPScraper.login()
    except Exception as e:
        return {"message": f"Login Error: {e}"}
    return {"message": "Logged in"}


def publish_to_api(user_id, scraped_id, base_url='http://localhost:8090'):
    try:
        # Define the endpoint URL
        url = f"{base_url}/publish/{user_id}/{scraped_id}"

        # Make a POST request
        response = requests.post(url)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            print(f"Message '{scraped_id}' published to user '{user_id}' successfully.")
            return True
        else:
            print(f"Failed to publish message. Status code: {response.status_code}")
            return False

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False