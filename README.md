make migrate-create MESSAGE="описание миграции"
make migrate-upgrade

make migrate-upgrade REVISION=head

make migrate-downgrade
make migrate-downgrade REVISION=-1
