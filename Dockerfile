FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
EXPOSE 8080

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "barestho_backend.asgi:application"]
