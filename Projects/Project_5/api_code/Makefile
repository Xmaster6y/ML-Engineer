#Docker
.PHONY: build
build:
	docker compose -f docker/docker-compose.yml -p api_code build

.PHONY: start
start:
	docker compose -f docker/docker-compose.yml -p api_code up

.PHONY: deploy
deploy:
	docker compose -f docker/docker-compose.yml -p api_code up -d --build

.PHONY: tty
tty:
	docker compose -f docker/docker-compose.yml -p api_code exec web bash
