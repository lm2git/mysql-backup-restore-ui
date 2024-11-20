FROM python:3.9-slim

# Aggiungi il repository e installa il client MySQL
RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./app /app
COPY requirements.txt /app

# Installa le dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]