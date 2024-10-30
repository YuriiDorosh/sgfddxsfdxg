import aio_pika
import asyncio
from app.core.config import settings
from app.utils.logger import logger

class RabbitMQRepository:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self, retries=5, delay=5):
            for attempt in range(retries):
                try:
                    logger.info(f"Attempting to connect to RabbitMQ (Attempt {attempt + 1})...")
                    self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
                    self.channel = await self.connection.channel()
                    logger.info("Connected to RabbitMQ")
                    break
                except Exception as e:
                    logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                    if attempt < retries - 1:
                        logger.info(f"Retrying in {delay} seconds...")
                        await asyncio.sleep(delay)
                    else:
                        logger.error("All connection attempts failed.")
                        raise e

    async def close(self):
        await self.connection.close()
        logger.info("Connection to RabbitMQ closed")

    async def consume(self, queue_name, callback):
        queue = await self.channel.declare_queue(queue_name, durable=True)
        await queue.consume(callback)
        logger.info(f"Started consuming queue: {queue_name}")

    async def publish(self, message_body, routing_key, correlation_id=None):
        message = aio_pika.Message(
            body=message_body.encode(),
            correlation_id=correlation_id
        )
        await self.channel.default_exchange.publish(
            message, routing_key=routing_key
        )
        logger.info(f"Published message to {routing_key}")
