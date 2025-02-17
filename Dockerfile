# Используем официальный образ Python
FROM python:3.11-alpine

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код проекта
COPY . .

# Открываем порт
EXPOSE 8000

# Запускаем бота
CMD ["python", "-m", "app.run"]
