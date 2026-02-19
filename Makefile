COMPOSE_FILE := docker-compose.yml
SERVICE_NAME := app
ALEMBIC_INI := src/alembic.ini
REVISION ?= head

up:
	docker compose -f $(COMPOSE_FILE) up -d $(SERVICE_NAME)

migrate-create: up
	@if [ -z "$(MESSAGE)" ]; then echo "Ошибка: укажите MESSAGE='описание миграции'"; exit 1; fi
	docker compose -f $(COMPOSE_FILE) exec -T $(SERVICE_NAME) bash -c "cd /app && alembic -c $(ALEMBIC_INI) revision --autogenerate -m '$(MESSAGE)'"

migrate-upgrade: up
	docker compose -f $(COMPOSE_FILE) exec -T $(SERVICE_NAME) bash -c "cd /app && alembic -c $(ALEMBIC_INI) upgrade $(REVISION)"

migrate-downgrade: up
	@REVISION=$${REVISION:--1}; \
	docker compose -f $(COMPOSE_FILE) exec -T $(SERVICE_NAME) bash -c "cd /app && alembic -c $(ALEMBIC_INI) downgrade $$REVISION"
