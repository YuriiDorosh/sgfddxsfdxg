pip install flower
celery -A myproject flower


pip install celery[redis,rabbitmq]  # Встановіть відповідний брокер


# celery.py
from celery import Celery

app = Celery('fastapi_gateway', broker='amqp://guest:guest@rabbitmq:5672/')

# Якщо потрібно, можна додати конфігурацію
app.conf.update(
    task_routes={
        'tasks.send_data_to_project_a': {'queue': 'queue_project_a'},
        'tasks.send_data_to_project_b': {'queue': 'queue_project_b'},
        # Додайте інші маршрути для проектів
    }
)


# __init__.py
from .celery import app as celery_app

__all__ = ('celery_app',)



# tasks.py
from .celery import app

@app.task
def send_data_to_project_a(data):
    # Логіка обробки даних, якщо потрібно
    return data  # Повертаємо дані для Django-проекту

@app.task
def send_data_to_project_b(data):
    # Логіка обробки даних
    return data




# main.py
from fastapi import FastAPI
from .tasks import send_data_to_project_a, send_data_to_project_b

app = FastAPI()

@app.post("/send-data/")
def send_data():
    # Отримуємо дані з віддаленого API
    data = fetch_data_from_remote_api()

    # Відправляємо задачі до відповідних проектів
    send_data_to_project_a.delay(data)
    send_data_to_project_b.delay(data)

    return {"status": "tasks sent"}



def fetch_data_from_remote_api():
    # Реалізуйте логіку отримання даних
    return {"some": "data"}


pip install celery[redis,rabbitmq]



# myproject/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject', broker='amqp://guest:guest@rabbitmq:5672/')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Налаштування маршрутизації задач
app.conf.task_routes = {
    'tasks.process_data': {'queue': 'queue_project_a'},  # Змініть на відповідну чергу
}

app.autodiscover_tasks()



# myproject/__init__.py
from .celery import app as celery_app

__all__ = ('celery_app',)



# myapp/tasks.py
from celery import shared_task
from .models import YourModel  # Замініть на вашу модель

@shared_task
def process_data(data):
    # Обробка та збереження даних
    obj = YourModel.objects.create(**data)
    return obj.id



celery -A myproject worker --loglevel=info --queues=queue_project_a


