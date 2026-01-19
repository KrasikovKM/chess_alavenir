# --- Stage 1: Builder ---
FROM python:3.10-slim AS builder

# Устанавливаем uv для быстрого управления зависимостями
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Копируем только файл зависимостей для кэширования
COPY app/requirements.txt .

# Устанавливаем зависимости с помощью uv
RUN uv pip install --no-cache --system --target /install -r requirements.txt

# --- Stage 2: Final ---
FROM python:3.10-slim

WORKDIR /app

# Устанавливаем только необходимые системные библиотеки
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Копируем установленные пакеты из builder
COPY --from=builder /install /usr/local/lib/python3.10/site-packages

# Копируем код приложения
COPY app /app

# Создаем папку для медиафайлов
RUN mkdir -p /app/media

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

EXPOSE 80

CMD ["python", "main.py"]
