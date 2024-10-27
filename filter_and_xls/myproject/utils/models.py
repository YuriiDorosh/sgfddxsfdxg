from django.db import models

class BaseModelMeta(models.base.ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        # Створюємо новий клас
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)
        if not new_class._meta.abstract:
            # Перевіряємо, чи менеджер all_objects не визначений вручну
            if not hasattr(new_class, 'all_objects'):
                # Додаємо менеджер all_objects
                new_class.add_to_class('all_objects', models.Manager())
        return new_class