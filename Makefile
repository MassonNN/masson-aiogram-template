.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  run		Start the bot (for docker-compose usage)"
	@echo "  project-start Start with docker-compose"
	@echo "  project-stop  Stop docker-compose"
	@echo "  lint		Reformat code"
	@echo "  requirements  Export poetry.lock to requirements.txt"

.PHONY:	blue
blue:
	poetry run blue src/ tests/

.PHONY:	mypy
mypy:
	poetry run mypy --strict --pretty --explicit-package-bases --install-types src/ tests/

.PHONY: isort
isort:
	poetry run isort src/ tests/

.PHONY: ruff
ruff:
	poetry run ruff check src/ tests/ --fix --respect-gitignore

.PHONY: lint
lint: blue isort ruff mypy

.PHONY: run
run:
	migrate
	poetry run python -m src.bot

# Poetry and environments utils
REQUIREMENTS_FILE := requirements.txt

.PHONY: requirements
requirements:
	# Export poetry.lock to requirements.txt if needed
	poetry check
	poetry export -o ${REQUIREMENTS_FILE} --without-hashes


# Alembic utils
.PHONY: generate
generate:
	source .env
	poetry run alembic revision --m="$(NAME)" --autogenerate

.PHONY: migrate
migrate:
	source .env
	poetry run alembic upgrade head

# Docker utils
.PHONY: project-start
project-start:
	docker-compose up --force-recreate ${MODE}

.PHONY: project-stop
project-stop:
	docker-compose down --remove-orphans ${MODE}
