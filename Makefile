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

.PHONY:	black
black:
	$(python) -m black .

.PHONY: isort
isort:
	$(python) -m isort .

.PHONY: flake
flake:
	$(python) -m flake8 .

.PHONY: lint
lint: black isort flake

.PHONY: run
run:
	migrate
	poetry run python -m bot

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
	alembic revision --m="$(NAME)" --autogenerate

.PHONY: migrate
migrate:
	alembic upgrade head

# Docker utils
.PHONY: project-start
project-start:
	docker-compose up --force-recreate ${MODE}

.PHONY: project-stop
project-stop:
	docker-compose down --remove-orphans ${MODE}
