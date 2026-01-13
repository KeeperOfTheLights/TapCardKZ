FROM python:3.11-slim

WORKDIR /app

# 1. Системные зависимости
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Обновление pip (убирает notice и фиксит ошибки разрешения зависимостей)
RUN pip install --no-cache-dir --upgrade pip

# 3. Подготовка к установке вашего пакета
COPY pyproject.toml .
RUN mkdir app && touch app/__init__.py

# 4. Установка зависимостей (включая aioboto3==13.2.0)
RUN pip install --no-cache-dir .

# 5. Копирование кода
COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]