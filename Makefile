DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file env/.env.docker
API_PROFILE = --profile api
DC_FILE = deploy/docker-compose.yml

APP_CONTAINER = url_alias.api
DB_CONTAINER = url_alias.db

.PHONY: lint
lint:
	@echo "Run ruff check..." && ruff check --exit-non-zero-on-fix
	@echo "Run ruff format..." && ruff format
	@echo "Run codespell..." && codespell

.PHONY: static
static:
	@echo "Run bandit..." && bandit -c pyproject.toml -r src

.PHONY: alembic
alembic:
	alembic revision --autogenerate -m "$(m)"

.PHONY: bootstrap
bootstrap:
	@cp env/.env.dist env/.env
	@cp env/.env.dist env/.env.docker
	@sed -i 's/^DB__HOST=localhost$$/DB__HOST=db/' env/.env.docker
	@. ./deploy/url_alias/generate_jwt_keys.sh
	@pre-commit
	@pre-commit install --hook-type commit-msg

.PHONY: up
up:
	$(DC) -f $(DC_FILE) $(ENV) $(API_PROFILE) up --build -d

.PHONY: infra
infra:
	$(DC) -f $(DC_FILE) $(ENV) up -d db

.PHONY: serve
serve:
	@make infra
	@. ./deploy/url_alias/entrypoint.sh

.PHONY: stop
stop:
	$(DC) -f $(DC_FILE) $(ENV) $(API_PROFILE) stop

.PHONY: down
down:
	@$(DC) -f $(DC_FILE) $(ENV) $(API_PROFILE) down
	@docker image prune -f

.PHONY: api-shell
api-shell:
	$(EXEC) $(APP_CONTAINER) bash

.PHONY: api-logs
api-logs:
	$(LOGS) $(APP_CONTAINER) -f

.PHONY: db-shell
db-shell:
	$(EXEC) $(DB_CONTAINER) bash

.PHONY: db-logs
db-logs:
	$(LOGS) $(DB_CONTAINER) -f
