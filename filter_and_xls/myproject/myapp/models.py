from django.db import models
from utils.models import BaseModelMeta


class BaseQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super(BaseQuerySet, self).__init__(*args, **kwargs)
        self._is_hidden_filter_applied = False

    def _apply_is_hidden_filter(self):
        if not self._is_hidden_filter_applied:
            self._is_hidden_filter_applied = True
            # Додаємо фільтр is_hidden=False
            self.query.add_q(models.Q(is_hidden=False))

    def _clone(self, **kwargs):
        clone = super(BaseQuerySet, self)._clone(**kwargs)
        clone._is_hidden_filter_applied = self._is_hidden_filter_applied
        return clone

    def iterator(self, *args, **kwargs):
        self._apply_is_hidden_filter()
        return super(BaseQuerySet, self).iterator(*args, **kwargs)

    def count(self):
        self._apply_is_hidden_filter()
        return super(BaseQuerySet, self).count()

    def aggregate(self, *args, **kwargs):
        self._apply_is_hidden_filter()
        return super(BaseQuerySet, self).aggregate(*args, **kwargs)

    def get(self, *args, **kwargs):
        # Додаємо is_hidden=False до фільтрів
        kwargs.setdefault('is_hidden', False)
        return super(BaseQuerySet, self).get(*args, **kwargs)

    def first(self):
        self._apply_is_hidden_filter()
        return super(BaseQuerySet, self).first()

    def last(self):
        self._apply_is_hidden_filter()
        return super(BaseQuerySet, self).last()

    def exists(self):
        self._apply_is_hidden_filter()
        return super(BaseQuerySet, self).exists()

    def update(self, **kwargs):
        self._apply_is_hidden_filter()
        return super(BaseQuerySet, self).update(**kwargs)

    def delete(self):
        self._apply_is_hidden_filter()
        return super(BaseQuerySet, self).delete()

    # Перекриваємо методи, що повертають новий QuerySet
    def all(self):
        qs = super(BaseQuerySet, self).all()
        qs._apply_is_hidden_filter()
        return qs

    def filter(self, *args, **kwargs):
        qs = super(BaseQuerySet, self).filter(*args, **kwargs)
        qs._apply_is_hidden_filter()
        return qs

    def exclude(self, *args, **kwargs):
        qs = super(BaseQuerySet, self).exclude(*args, **kwargs)
        qs._apply_is_hidden_filter()
        return qs

    def order_by(self, *field_names):
        qs = super(BaseQuerySet, self).order_by(*field_names)
        qs._apply_is_hidden_filter()
        return qs

    def reverse(self):
        qs = super(BaseQuerySet, self).reverse()
        qs._apply_is_hidden_filter()
        return qs

    def distinct(self, *field_names):
        qs = super(BaseQuerySet, self).distinct(*field_names)
        qs._apply_is_hidden_filter()
        return qs

    def values(self, *fields, **expressions):
        qs = super(BaseQuerySet, self).values(*fields, **expressions)
        qs._apply_is_hidden_filter()
        return qs

    def values_list(self, *fields, **kwargs):
        qs = super(BaseQuerySet, self).values_list(*fields, **kwargs)
        qs._apply_is_hidden_filter()
        return qs

    def annotate(self, *args, **kwargs):
        qs = super(BaseQuerySet, self).annotate(*args, **kwargs)
        qs._apply_is_hidden_filter()
        return qs

    def raw(self, raw_query, params=None, *args, **kwargs):
        # Для сирих запитів фільтр не застосовується
        return super(BaseQuerySet, self).raw(raw_query, params=params, *args, **kwargs)

    def __getitem__(self, k):
        self._apply_is_hidden_filter()
        return super(BaseQuerySet, self).__getitem__(k)

    def __len__(self):
        self._apply_is_hidden_filter()
        return super(BaseQuerySet, self).__len__()

    def __iter__(self):
        self._apply_is_hidden_filter()
        return super(BaseQuerySet, self).__iter__()



class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db).filter(is_hidden=False)


class BaseModel(models.Model, metaclass=BaseModelMeta): 
    is_hidden = models.BooleanField(default=False)
    
    objects = BaseManager()    

    class Meta:
        abstract = True 




























class Author(BaseModel):
    name = models.CharField(max_length=255)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Book(BaseModel):
    title = models.CharField(max_length=255)
    publication_date = models.DateField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
