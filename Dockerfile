# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл requirements и устанавливаем зависимости
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы бэкенда в контейнер
COPY backend/ .

# Указываем порт, который будет использоваться приложением
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "app.py"]
