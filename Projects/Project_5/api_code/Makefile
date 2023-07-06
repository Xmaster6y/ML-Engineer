#Docker
.PHONY: build
build:
	docker compose -f docker/docker-compose.yml build

.PHONY: start
start:
	docker compose -f docker/docker-compose.yml up

.PHONY: deploy
deploy:
	docker compose -f docker/docker-compose.yml -d --build

.PHONY: tty
tty:
	docker compose -f docker/docker-compose.yml exec web bash
