https://docs.djangoproject.com/en/5.1/topics/db/queries/

https://www.django-rest-framework.org/api-guide/views/

https://github.com/saintqqe/roflan

https://www.youtube.com/watch?v=EsBqIZmR2Uc&list=PL-2EBeDYMIbQXKsyNweppuFptuogJe2L-

---

```python
from django.db import connect, reset_queries

import time
import functools


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, *kwargs):
        reset_queries()
        start_queries = len(connection.queries)

        start = time.perf_counter()
        funct(*args, *kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"View (function.name): {func.__name}")
        print(f"Queries quantity: {end_queries - start_queries}")
        print(f"Execution time: {(end - start):.2f}s")

    return inner_func
```

```python
@query_debugger
def bld():
    # qs = Blog.objects.all() # 2k
    # qs = Blog.objects.select_related('category') # 1001
    qs = Blog.objects.select_related('category', 'author') # 1

    print(qs.query)

    posts = []
    for item in qs:
        posts.append([
            'id' : item.id,
        ])

    
    return posts


 @query_debugger
 def cld():
    qs = Communities.objects.all()
    # qs = Communities.objects.prefetch_related('blog_posts')
    # qs = Communities.objects.prefetch_related(
    #    Prefetch('blog_posts', queryset=Blog.objects.filter(tags__name__in=['tag1', 'tag2', 'tag3'])))

    print(qs.query)

    communities = []
    for item in qs:
        # blog_posts = [post.title for post in item.blog_posts.filter(tags__name__in=['tag1', 'tag2', 'tag3'])]
        # blog_posts = [post.title for post in item.blog_posts.all()] # Prefetch

        # print(item,blog_posts.all()) 

        communities.append({
            'id': item.id,
            'name': item,name,
            # 'blog_posts': item.blog_posts.all(),
            'blog_posts': blog_posts, # Prefetch
        }) 

    return communities
```

---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---

```python
from inventory.models import Product, Category, Brand
from django.db.models import Avg, Max, Count, Sum, Min

Product.objects.all()[:1] #start, stop, step/ перший елемент
Product.objects.all().values("id", "name")[:3] # у вигляді словника
Product.objects.all().values_list("id", "name")[:3] # у вигляді списку
Product.objects.order_by('name') # сортування 
Product.objects.order_by('-id').values_list('id') # сортування у зворотному порядку
Product.objects.order_by('?') # випадкове сортування
Product.objects.order_by('id').values_list('id').reverse().reverse() # зворотне сортування
Product.objects.all().first() # перший елемент
Product.objects.all().last() # останній елемент
Product.objects.all().earliest('time_create') # найраніший елемент
Product.objects.all().latest('time_create') # найновіший елемент

Product.objects.aggregate(Avg('quantity')) # Середня кількість всіх
Product.objects.aggregate(average_q_ty=Avg('quantity')) # Середня кількість всіх з використанням власної змінної
Product.objects.filter(quantity__gt=15).aggregate(Sum('quantity')) # Сума для відфільтрованих
Category.objects.filter(id=3).aggregate(Sum('products__quantity')) # Сума через зовнішній ключ для відфільтрованих
Product.objects.aggregate(Max('quantity'), Min('quantity')) # Комбінування кількох агрегатів
x = Product.objects.annotate(num_q=Count('quantity')) # Анотування
x[0].num_q # Анотування повертає змінну, яку можна використовувати
Product.objects.values('category').annotate(num_cat=Count('quantity')) # Анотування: скільки категорій вибрано
Product.objects.values('category').annotate(num_cat=Sum('quantity')) # Анотування суми для кожної категорії

```

```python
from inventory.models import Tag, Category, Brand, Stock

Brand.objects.filter(brand_id=1).update(name="new name") # оновлення імені за ID
Brand.objects.update_or_create(name="new name") # оновлення імені, використовувати з defaults
Tag.objects.update_or_create(name="new name") # оновлення імені, використовувати з defaults
Tag.objects.update_or_create(name="new name", defaults={"name": "old name"}) # оновлення імені

# bulk_update(objs, fields, batch_size=None)

objs = [Tag.objects.get(id=6), Tag.objects.get(id=7)]
objs[0].name = ["old old name"]
objs[1].name = ["new new name2"]

Tag.objects.bulk_update(objs, ['name']) # оновлення імені для багатьох записів

Brand.objects.all().delete() # Видалення всіх даних
Brand.objects.filter(brand_id=1).delete() # Видалення за ID
Stock.objects.filter(id=4).delete() # Видалення за ID
```

```python
from inventory.models import Tag, Category, Brand, Stock
from django.shortcuts import get_object_or_404
from django.db.models import Q

Tag.objects.get(id=1) # Отримання тільки одного об'єкта
Tag.objects.get_or_create(name="django-react") # Отримання одного об'єкта, якщо відсутній — створення
get_object_or_404(Tag, name="django-react") # Отримання одного об'єкта, якщо відсутній — помилка 404

Tag.objects.all().filter(id=4) # Фільтр за ID
Tag.objects.filter(id=4) # Фільтр за ID
Tag.objects.exclude(id=3) # Фільтр виключити за ID

Tag.objects.filter(name="django") | Tag.objects.filter(name="react") # Фільтр використовуючи АБО
Tag.objects.filter(Q(id=2) | Q(id=5)) # Фільтр використовуючи АБО
Tag.objects.filter(id__gt=2) # Фільтр за ГОТОВИМИ ПАРАМЕТРАМИ (Більше ніж)
Tag.objects.filter(name__startswith="d") # Фільтр за ГОТОВИМИ ПАРАМЕТРАМИ (починається з)

Brand.objects.filter(category_id__name="Python") # Перехід в таблицю Категорія
Brand.objects.filter(category_id__name__contains="p") # Перехід в таблицю Категорія + пошук за фільтром
first_brand = Category.objects.first() # Перший об'єкт у таблиці
first_brand.brand_set.all() # Без використання related_name
first_brand.brands.all() # З використанням related_name

Stock.objects.filter(product_brand__name__contains='adi') # Витягуємо name з таблиці Brand
Brand.objects.filter(stock_brand__quantity__lte=3) # Витягуємо кількість з таблиці Stock через related_name
Brand.objects.filter(stock_brand__quantity__gte=3) # Витягуємо кількість з таблиці Stock через related_name

Brand.objects.filter(tag__id=1) # Фільтр тегів для об'єктів Brand, де ID = 1
Brand.objects.filter(tag__name__contains="re") # Фільтр тегів для об'єктів Brand, де ім'я містить
Brand.tag.through.objects.all() # Виведення всіх об'єктів у проміжній таблиці
Tag.objects.filter(brand_tags__brand_id=1) # Виведення тегів, де brand_id = 1
Tag.objects.filter(brand_tags__brand_id__gte=1) # Виведення тегів, де brand_id >= 1
```