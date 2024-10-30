import json
from aio_pika import IncomingMessage
from app.repositories.rabbitmq_repository import RabbitMQRepository
from app.services.api_service import APIService
from app.utils.logger import logger

class Consumer:
    def __init__(self):
        self.rabbitmq = RabbitMQRepository()
        self.api_service = APIService()

    async def start(self):
        await self.rabbitmq.connect()
        await self.rabbitmq.consume("request_queue", self.on_message)

    async def on_message(self, message: IncomingMessage):
        async with message.process():
            try:
                request_data = json.loads(message.body.decode())
                logger.info(f"Received message: {request_data}")

                api_response = self.api_service.fetch_data(request_data)

                if api_response is not None:
                    response_body = json.dumps(api_response)
                else:
                    response_body = json.dumps({"error": "Failed to fetch data"})

                await self.rabbitmq.publish(
                    message_body=response_body,
                    routing_key=message.reply_to,
                    correlation_id=message.correlation_id
                )
                logger.info("Response sent")
            except Exception as e:
                logger.error(f"Error processing message: {e}")
