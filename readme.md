# Team Finder - Платформа для поиска команды

Team Finder - это веб-приложение для поиска и создания проектных команд. Пользователи могут создавать проекты, добавлять свои навыки и присоединяться к другим проектам.

## Требования

- Python 3.8+
- Django 5.2.4
- PostgreSQL 16
- Docker и Docker Compose

## Установка и запуск

### 1. Виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

docker run -d --name team_finder_postgres -e POSTGRES_DB=team_finder -e POSTGRES_USER=team_finder -e POSTGRES_PASSWORD=team_finder -p 5436:5432 postgres:16