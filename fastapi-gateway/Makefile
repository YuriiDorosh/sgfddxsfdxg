ENV = --env-file .env
LOGS = docker logs
EXEC = docker exec -it
APP_CONTAINER = fastapi-gateway
RABBITMQ_CONTAINER = rabbitmq
DC = docker compose
NETWORK_NAME = gateway-network


.PHONY: check-network up-all up-all-no-cache up-gateway up-rabbitmq down-all down-gateway down-rabbitmq logs-gateway logs-rabbitmq logs-all

check-network:
	@echo "Checking for network $(NETWORK_NAME)..."
	@if ! docker network ls | grep -q $(NETWORK_NAME); then \
		echo "Network $(NETWORK_NAME) does not exist. Creating..."; \
		docker network create $(NETWORK_NAME); \
	else \
		echo "Network $(NETWORK_NAME) already exists."; \
	fi

up-all: check-network
	$(DC) -f docker_compose/rabbitmq/docker-compose.yml $(ENV) up -d
	$(DC) -f docker_compose/gateway/docker-compose.yml $(ENV) up -d

up-all-no-cache: check-network
	$(DC) -f docker_compose/rabbitmq/docker-compose.yml $(ENV) build --no-cache
	$(DC) -f docker_compose/gateway/docker-compose.yml $(ENV) build --no-cache
	$(DC) -f docker_compose/rabbitmq/docker-compose.yml $(ENV) up -d
	$(DC) -f docker_compose/gateway/docker-compose.yml $(ENV) up -d

up-gateway:
	$(DC) -f docker_compose/gateway/docker-compose.yml $(ENV) up -d

up-rabbitmq:
	$(DC) -f docker_compose/rabbitmq/docker-compose.yml $(ENV) up -d

down-all:
	$(DC) -f docker_compose/gateway/docker-compose.yml down
	$(DC) -f docker_compose/rabbitmq/docker-compose.yml down

down-gateway:
	$(DC) -f docker_compose/gateway/docker-compose.yml down

down-rabbitmq:
	$(DC) -f docker_compose/rabbitmq/docker-compose.yml down

logs-gateway:
	$(LOGS) -f $(APP_CONTAINER)

logs-rabbitmq:
	$(LOGS) -f $(RABBITMQ_CONTAINER)

logs-all:
	$(LOGS) -f $(APP_CONTAINER) & \
	$(LOGS) -f $(RABBITMQ_CONTAINER)
