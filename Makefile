compose:
	docker-compose up --build

install-dep:
	poetry install

start-server-dev:
	./scripts/start-dev.sh

run-tests:
	poetry run pytest -s -v -W ignore

alembic-revision:
	./scripts/create_revision.sh "$(MESSAGE)"

alembic-upgrade:
	poetry run alembic upgrade head

alembic-downgrade:
	alembic downgrade -1
