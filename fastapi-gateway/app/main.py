import asyncio
from fastapi import FastAPI
from app.api.consumers import Consumer

app = FastAPI()
consumer = Consumer()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consumer.start())
