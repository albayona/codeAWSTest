import asyncio
from concurrent.futures.process import ProcessPoolExecutor
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Dict
from uuid import UUID, uuid4

from fastapi import BackgroundTasks, HTTPException, status
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from utils.scraper import cpu_bound_func_scrape


class Job(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    status: str = "in_progress"
    result: int = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.executor = ProcessPoolExecutor(1)
    yield
    app.state.executor.shutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,  # Allows cookies to be included in cross-origin requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

jobs: Dict[UUID, Job] = {}


async def run_in_process(fn, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(app.state.executor, fn, *args)  # wait and return result


async def start_cpu_bound_task(uid: UUID, url: int, user: str, token: str) -> None:
    jobs[uid].result = await run_in_process(cpu_bound_func_scrape, user, token, url, 28)
    jobs[uid].status = "complete"


@app.post("/scrape/", status_code=HTTPStatus.ACCEPTED)
async def scrape_task_handler(background_tasks: BackgroundTasks, request: Request):


    user = request.headers.get('X-Consumer-Custom-Id')
    token = get_token(request)
    url_data = await request.json()
    url = url_data['link']

    if not user:
        raise HTTPException(status_code=400, detail="X-Consumer-Custom-Id header missing")

    new_task = Job()
    jobs[new_task.uid] = new_task
    background_tasks.add_task(start_cpu_bound_task, new_task.uid, url, user, token)
    return new_task


@app.get("/status/{uid}")
async def status_handler(uid: UUID):
    return jobs[uid]




def get_token(request: Request):
    authorization: str = request.headers.get("Authorization")
    if authorization:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
            )
        return {"token": token}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
