# Билд-стадия
FROM python:3.12-slim as builder

WORKDIR /app

# Установка системных зависимостей для сборки
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Создание виртуального окружения
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копирование и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Финальная стадия
FROM python:3.12-slim

WORKDIR /app

# Копирование виртуального окружения из билд-стадии
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Создание непривилегированного пользователя
RUN groupadd -r fastapi && useradd -r -g fastapi fastapi && \
    chown -R fastapi:fastapi /app

# Копирование приложения
COPY --chown=fastapi:fastapi . .

USER fastapi

EXPOSE 8000

# Для корректной работы контейнера его следует собрать
# через команду "docker build -t task3-app ."
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]