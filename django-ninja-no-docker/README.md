```python
import os
from django.conf import settings
from myapp.models import CustomUser
from celery import shared_task

@shared_task
def delete_unused_avatars():
    avatars_in_db = CustomUser.objects.values_list('avatar', flat=True)
    avatars_in_db = set(os.path.join(settings.MEDIA_ROOT, avatar) for avatar in avatars_in_db if avatar)
    
    avatars_in_media = set(
        os.path.join(settings.MEDIA_ROOT, 'avatars', filename)
        for filename in os.listdir(os.path.join(settings.MEDIA_ROOT, 'avatars'))
    )
    
    unused_avatars = avatars_in_media - avatars_in_db
    
    for avatar in unused_avatars:
        try:
            os.remove(avatar)
            print(f"Видалено аватар: {avatar}")
        except OSError:
            print(f"Помилка при видаленні аватарки: {avatar}")
```

```python
# Налаштування для Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Можна використовувати Redis або RabbitMQ
CELERY_BEAT_SCHEDULE = {
    'delete-unused-avatars-every-morning': {
        'task': 'myapp.tasks.delete_unused_avatars',
        'schedule': 86400.0,  # Інтервал 24 години (один раз на день)
        'options': {'time_limit': 60 * 30},  # Обмеження на виконання завдання 30 хвилин
    },
}

CELERY_TIMEZONE = 'Europe/Kiev'
```

```python
import os
from django.conf import settings
from myapp.models import CustomUser
from celery import shared_task

@shared_task
def delete_unused_avatars():
    avatars_in_db = CustomUser.objects.values_list('avatar', flat=True)
    avatars_in_db = set(os.path.join(settings.MEDIA_ROOT, avatar) for avatar in avatars_in_db if avatar)
    
    avatars_in_media = set(
        os.path.join(settings.MEDIA_ROOT, 'avatars', filename)
        for filename in os.listdir(os.path.join(settings.MEDIA_ROOT, 'avatars'))
    )
    
    unused_avatars = avatars_in_media - avatars_in_db
    
    for avatar in unused_avatars:
        try:
            os.remove(avatar)
            print(f"Видалено аватар: {avatar}")
        except OSError:
            print(f"Помилка при видаленні аватарки: {avatar}")
```