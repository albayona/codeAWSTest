from fastapi import FastAPI, WebSocket
import redis
import asyncio
from sse_starlette.sse import EventSourceResponse
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,  # Allows cookies to be included in cross-origin requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Redis client configuration
redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)


# Function to publish data to Redis
def publish_data_on_redis(user_id, scraped_id):
    redis_client.publish(user_id, scraped_id)


# Function to subscribe to Redis channel
def subscribe(user_id):
    p = redis_client.pubsub()
    p.psubscribe(user_id)
    return p


# SSE endpoint to subscribe and stream events
@app.get("/subscribe/{user}")
async def subscribe_to_events(user: str, request: Request):
    async def event_generator():
        uid = request.headers.get('X-Consumer-Custom-Id')
        print(uid)
        uid = uid.replace("@", "")
        print(f"Subscribing to user's channel: {uid}")
        # Subscribe to user's channel
        p = subscribe(uid)
        try:
            while True:
                message = p.get_message()
                if message:
                    data = message.get('data')
                    if data:
                        yield f"data: {data}\n\n"
                    await asyncio.sleep(0.1)  # Optional: Adjust the sleep time
                else:
                    await asyncio.sleep(1)
        except asyncio.CancelledError:
            p.unsubscribe(uid)
            p.close()

    return EventSourceResponse(event_generator())


# Endpoint to publish a message to Redis
@app.post("/publish/{user_id}/{scraped_id}")
async def publish_message(user_id: str, scraped_id: str, request: Request):
    try:
        publish_data_on_redis(user_id, scraped_id)
        print(f"Published message '{scraped_id}' to user '{user_id}'")
        return {"detail": f"Published message '{scraped_id}' to user '{user_id}'"}
    except Exception as e:
        return {"error": str(e)}
