![template](https://user-images.githubusercontent.com/35528949/212500045-feb51ec0-e26a-45a6-bc8c-75d01379faf9.png)
![](https://img.shields.io/badge/version-0.1.3%20-brightgreen)
![](https://img.shields.io/github/license/MassonNN/masson-aiogram-template)
![](https://img.shields.io/github/forks/MassonNn/masson-aiogram-template)
![](https://img.shields.io/github/stars/MassonNn/masson-aiogram-template?style=flat-square)
[![telegram](https://img.shields.io/badge/Telegram-Join-blue)](https://t.me/massonnn_yt)

---
## Setup bot

1. Clone this repository

2. Change the name of `.env.dist` to `.env` and set all environment variables as you need

3. Change password for redis in build/redis.conf (`requirepass` and `masterauth`). Set same password in `.env` 
   (`REDIS_PASSWORD`).

4. Change project name and other information in `pyproject.toml`

5. `make project-start` to start project with docker-compose or `make help` if you want to know more about make commands

---
## Development

If you want to lint your code: \
```make lint``` \
This will start isort, blue and ruff to src and tests folders

You can manually run any instrument by: \
`make ruff`, `make blue` or `make isort`

### Migrations
`make generate NAME=<name>` \
Generate alembic revision for migration with given name

`make migrate` \
Apply migrations to the target database

---
## Roadmap

- Add Github Actions CI/CD
- Light (simplified) version without docker and CI/CD
- Highload version with NATS and Docker Swarm
- More tests kit and update factory

