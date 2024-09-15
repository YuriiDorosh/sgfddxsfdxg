ENV = --env-file .env
LOGS = docker logs
EXEC = docker exec -it
APP_CONTAINER = django
WORKER_1_CONTAINER = celery_worker_1
WORKER_2_CONTAINER = celery_worker_2
WORKER_BEAT_CONTAINER = celery_beat
REDIS_CONTAINER = redis
NGINX_CONTAINER = nginx
DB_CONTAINER = postgres
DC = docker compose
MANAGE_PY = python manage.py
NETWORK_NAME = backend


.PHONY: check-network up-all up-all-2 up-django up-django-db up-django-db-pgadmin-adminer up-pgadmin up-db up-adminer down-all down-all-2 down-django down-django-db down-pgadmin down-db down-adminer migrations superuser test collectstatic

check-network:
	@echo "Checking for network $(NETWORK_NAME)..."
	@if ! docker network ls | grep -q $(NETWORK_NAME); then \
		echo "Network $(NETWORK_NAME) does not exist. Creating..."; \
		docker network create $(NETWORK_NAME); \
	else \
		echo "Network $(NETWORK_NAME) already exists."; \
	fi

up-all: check-network
	$(DC) -f docker_compose/db/docker-compose.yml $(ENV) up -d
	$(DC) -f docker_compose/django/docker-compose.yml $(ENV) up -d
	$(DC) -f docker_compose/pgadmin/docker-compose.yml $(ENV) up -d
	$(DC) -f docker_compose/adminer/docker-compose.yml $(ENV) up -d

up-all-2:
	$(DC) -f docker_compose/db/docker-compose.yml \
	      -f docker_compose/django/docker-compose.yml \
	      -f docker_compose/pgadmin/docker-compose.yml \
	      -f docker_compose/adminer/docker-compose.yml \
	      $(ENV) up -d

up-django:
	$(DC) -f docker_compose/django/docker-compose.yml $(ENV) up -d

up-django-db:
	$(DC) -f docker_compose/db/docker-compose.yml $(ENV) up -d
	$(DC) -f docker_compose/django/docker-compose.yml $(ENV) up -d

up-django-db-pgadmin-adminer:
	$(DC) -f docker_compose/db/docker-compose.yml $(ENV) up -d
	$(DC) -f docker_compose/django/docker-compose.yml $(ENV) up -d
	$(DC) -f docker_compose/pgadmin/docker-compose.yml $(ENV) up -d
	$(DC) -f docker_compose/adminer/docker-compose.yml $(ENV) up -d

up-pgadmin:
	$(DC) -f docker_compose/pgadmin/docker-compose.yml $(ENV) up -d

up-db:
	$(DC) -f docker_compose/db/docker-compose.yml $(ENV) up -d

up-adminer:
	$(DC) -f docker_compose/adminer/docker-compose.yml $(ENV) up -d

down-all:
	$(DC) -f docker_compose/db/docker-compose.yml down
	$(DC) -f docker_compose/django/docker-compose.yml down
	$(DC) -f docker_compose/pgadmin/docker-compose.yml down
	$(DC) -f docker_compose/adminer/docker-compose.yml down

down-all-2:
	$(DC) -f docker_compose/db/docker-compose.yml \
	      -f docker_compose/django/docker-compose.yml \
	      -f docker_compose/pgadmin/docker-compose.yml \
	      -f docker_compose/adminer/docker-compose.yml \
	      down

down-django:
	$(DC) -f docker_compose/django/docker-compose.yml down

down-django-db:
	$(DC) -f docker_compose/db/docker-compose.yml down
	$(DC) -f docker_compose/django/docker-compose.yml down

down-pgadmin:
	$(DC) -f docker_compose/pgadmin/docker-compose.yml down

down-db:
	$(DC) -f docker_compose/db/docker-compose.yml down

down-adminer:
	$(DC) -f docker_compose/adminer/docker-compose.yml down

migrations:
	$(EXEC) $(APP_CONTAINER) ${MANAGE_PY} makemigrations

migrate:
	$(EXEC) $(APP_CONTAINER) ${MANAGE_PY} migrate

superuser:
	$(EXEC) $(APP_CONTAINER) ${MANAGE_PY} createsuperuser

test:
	$(EXEC) $(APP_CONTAINER) ${MANAGE_PY} test

collectstatic:
	$(EXEC) $(APP_CONTAINER) ${MANAGE_PY} collectstatic --noinput
