FROM python:3.12-slim

WORKDIR /app

# 1. Системные зависимости (нужны для некоторых python-пакетов)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2. Устанавливаем Poetry напрямую
# Это надежнее, чем надеяться на то, что pip правильно распарсит все зависимости через '.'
RUN pip install --no-cache-dir poetry

# 3. Отключаем создание виртуальных окружений внутри контейнера
# В Docker контейнер сам по себе является изоляцией, лишняя папка .venv там не нужна
RUN poetry config virtualenvs.create false

# 4. Сначала копируем ТОЛЬКО файлы зависимостей
# Это критически важно: Docker закеширует этот слой. 
# Библиотеки не будут переустанавливаться, пока вы не измените pyproject.toml
COPY pyproject.toml poetry.lock* ./

# 5. Устанавливаем зависимости
# --no-root говорит не устанавливать сам проект (папку app), только библиотеки
RUN poetry install --no-interaction --no-ansi --no-root --only main

# 6. Копируем остальной код (ваше приложение)
COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]