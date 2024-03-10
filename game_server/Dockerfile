FROM ubuntu:latest
LABEL authors="shara"

FROM python:3.11-slim

# Устанавливаем зависимости
RUN pip install Flask

# Копируем приложение в контейнер
WORKDIR /app
COPY . /app

# Указываем команду для запуска приложения
CMD ["python", "app.py"]

ENTRYPOINT ["top", "-b"]