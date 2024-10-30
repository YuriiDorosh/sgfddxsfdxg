from pydantic import BaseSettings

class Settings(BaseSettings):
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"
    EXTERNAL_API_URL: str = "https://jsonplaceholder.typicode.com/posts"

settings = Settings()
