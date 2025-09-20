FROM python:alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \ 
    POETRY_CACHE_DIR=/tmp/poetry_cache 

RUN apk add --no-cache \
    ffmpeg \
    && pip install poetry

    #pythondontbuffered - чтобы не создавались файлы кеша пайтон
    #pythonbuffered - чтоб логи были быстрее

    # POETRY_NO_INTERACTION=1 - отключает интерактивные запросы
    # POETRY_VENV_IN_PROJECT=1 - создает .venv в директории проекта
    # POETRY_CACHE_DIR=/tmp/poetry_cache - кеш в временной директори

RUN poetry config virtualenvs.create false

RUN mkdir -p /app/downloads && chmod 777 /app/downloads


COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости через Poetry
# --only=main - устанавливаем только production зависимости (не dev)
# --no-root - не устанавливаем сам пакет, только зависимости

RUN poetry install --no-root --only=main

ENV DOWNLOAD_DIR=/app/downloads

COPY . .

EXPOSE 8000

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000" ]