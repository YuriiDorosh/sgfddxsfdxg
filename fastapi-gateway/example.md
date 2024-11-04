https://pika.readthedocs.io/en/stable/

https://chatgpt.com/share/6727e018-2e1c-8011-bada-d21c47a856fe

https://chatgpt.com/share/6728454e-2600-8011-9c3d-47e8b31ddd67

```python
import pika

# Параметри підключення
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

# Встановлюємо з'єднання
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
```


```python
# Створюємо чергу, якщо вона ще не існує
channel.queue_declare(queue='my_queue', durable=True)

# Відправляємо повідомлення
message = "Hello, World!"
channel.basic_publish(
    exchange='',
    routing_key='my_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # Зробити повідомлення стійким (persistent)
    )
)
print("Повідомлення відправлено до my_queue")
```


```python
# Оголошуємо обмінник типу 'direct'
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Черги
queues = ['queue1', 'queue2', 'queue3']

# Створюємо та зв'язуємо черги з обмінником
for queue_name in queues:
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=queue_name)

# Відправляємо повідомлення до певних черг
message = "Hello to multiple queues!"
for queue_name in ['queue1', 'queue3']:
    channel.basic_publish(
        exchange='direct_logs',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    print(f"Повідомлення відправлено до {queue_name}")
```

```python
# Оголошуємо обмінник типу 'direct'
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Черги
queues = ['queue1', 'queue2', 'queue3']

# Створюємо та зв'язуємо черги з обмінником
for queue_name in queues:
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=queue_name)

# Відправляємо повідомлення до певних черг
message = "Hello to multiple queues!"
for queue_name in ['queue1', 'queue3']:
    channel.basic_publish(
        exchange='direct_logs',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    print(f"Повідомлення відправлено до {queue_name}")
```


```python
# Оголошуємо обмінник типу 'fanout'
channel.exchange_declare(exchange='broadcast_exchange', exchange_type='fanout')

# Створюємо та зв'язуємо черги з обмінником
queues = ['queue1', 'queue2', 'queue3']
for queue_name in queues:
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange='broadcast_exchange', queue=queue_name)

# Відправляємо повідомлення
message = "Hello to all queues!"
channel.basic_publish(
    exchange='broadcast_exchange',
    routing_key='',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,
    )
)
print("Повідомлення відправлено до всіх черг")
```

```python
def callback(ch, method, properties, body):
    print(f"Отримано повідомлення: {body.decode()}")

channel.basic_consume(
    queue='my_queue',
    on_message_callback=callback,
    auto_ack=True
)

print('Очікуємо повідомлень. Натисніть CTRL+C для виходу.')
channel.start_consuming()
```


```python
def callback(ch, method, properties, body):
    print(f"Отримано повідомлення: {body.decode()}")
    # Виконуємо обробку повідомлення
    # ...

    # Після успішної обробки відправляємо підтвердження
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue='my_queue',
    on_message_callback=callback,
    auto_ack=False  # Вимикаємо автоматичне підтвердження
)

print('Очікуємо повідомлень. Натисніть CTRL+C для виходу.')
channel.start_consuming()
```


```python
# Встановлюємо з'єднання в режимі підтвердження
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.confirm_delivery()

# Відправляємо повідомлення з підтвердженням
message = "Message with publisher confirm"
try:
    channel.basic_publish(
        exchange='',
        routing_key='my_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        ),
        mandatory=True
    )
    print("Повідомлення успішно відправлено")
except pika.exceptions.UnroutableError:
    print("Повідомлення не було доставлене")
```

```python
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_key = 'kern.critical'  # Приклад ключа маршрутизації
message = "A critical kernel error"

channel.basic_publish(
    exchange='topic_logs',
    routing_key=routing_key,
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,
    )
)
print(f"Відправлено повідомлення з ключем {routing_key}")
```


```python
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# Створюємо чергу з унікальним ім'ям
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

# Ключі маршрутизації, на які підписується споживач
binding_keys = ['kern.*', '*.critical']

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs',
        queue=queue_name,
        routing_key=binding_key
    )

def callback(ch, method, properties, body):
    print(f"Отримано повідомлення з ключем {method.routing_key}: {body.decode()}")

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

print('Очікуємо повідомлень. Натисніть CTRL+C для виходу.')
channel.start_consuming()
```


```python
channel.queue_declare(queue='priority_queue', durable=True, arguments={'x-max-priority': 10})

message = "High priority message"
channel.basic_publish(
    exchange='',
    routing_key='priority_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,
        priority=9  # Встановлюємо пріоритет
    )
)
print("Відправлено повідомлення з високим пріоритетом")
```


```python
channel.queue_declare(queue='priority_queue', durable=True)

def callback(ch, method, properties, body):
    print(f"Отримано повідомлення з пріоритетом {properties.priority}: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue='priority_queue',
    on_message_callback=callback,
    auto_ack=False
)

print('Очікуємо повідомлень. Натисніть CTRL+C для виходу.')
channel.start_consuming()
```

```python
def callback(ch, method, properties, body):
    try:
        # Виконуємо обробку повідомлення
        # ...

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Помилка обробки: {e}")
        # Повторно ставимо повідомлення в чергу
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
```


```python
# Створюємо DLQ
channel.queue_declare(queue='dead_letter_queue', durable=True)

# Створюємо основну чергу з посиланням на DLQ
args = {
    'x-dead-letter-exchange': '',
    'x-dead-letter-routing-key': 'dead_letter_queue'
}
channel.queue_declare(queue='main_queue', durable=True, arguments=args)
```

```python
def callback(ch, method, properties, body):
    try:
        # Обробка повідомлення
        # ...
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Помилка обробки: {e}")
        # Не повторюємо, повідомлення перейде в DLQ
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
```


```python
connection.close()
```