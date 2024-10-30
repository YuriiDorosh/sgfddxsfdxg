import asyncio
import aio_pika
import uuid
import json

RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"

async def main():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    # Унікальний ідентифікатор для кореляції запиту та відповіді
    correlation_id = str(uuid.uuid4())

    # Створення ексклюзивної черги для отримання відповіді
    callback_queue = await channel.declare_queue(exclusive=True)

    request_data = {"userId": 1}

    # Відправка повідомлення до request_queue
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(request_data).encode(),
            correlation_id=correlation_id,
            reply_to=callback_queue.name,
        ),
        routing_key="request_queue",
    )
    print(f" [x] Sent request: {request_data}")

    future = asyncio.Future()

    # Слухання черги для отримання відповіді
    async with callback_queue.iterator() as queue_iter:
        async for message in queue_iter:
            if message.correlation_id == correlation_id:
                async with message.process():
                    response_data = json.loads(message.body.decode())
                    print(f" [.] Got response: {response_data}")
                    future.set_result(response_data)
                    break

    await future
    await connection.close()

if __name__ == "__main__":
    asyncio.run(main())
