***Запуск проект 
docker compose up --build -d

**Запуск миграции
make migrate-create MESSAGE="описание миграции"

**Применения миграции
make migrate-upgrade
**Применения определенной миграции
make migrate-upgrade REVISION=head
**Откат миграции
make migrate-downgrade
**Откат до определенной миграции
make migrate-downgrade REVISION=-1
