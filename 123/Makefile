.PHONY: all backend frontend

all: network backend frontend

network:
	docker network inspect frontend-backend-net >/dev/null 2>&1 || docker network create frontend-backend-net

backend:
	cd backend && docker-compose up --build -d

frontend:
	cd frontend && docker-compose up --build
