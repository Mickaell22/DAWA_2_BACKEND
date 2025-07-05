# 🐍 Backend Flask Dockerfile - Corregido para wait-for-db.sh
FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt desde la ubicación correcta
COPY src/utils/requirements.txt /app/requirements.txt

# Instalar dependencias Python
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Crear script wait-for-db.sh directamente en el contenedor (más confiable)
RUN echo '#!/bin/bash' > /usr/local/bin/wait-for-db.sh && \
    echo 'set -e' >> /usr/local/bin/wait-for-db.sh && \
    echo 'host="$1"' >> /usr/local/bin/wait-for-db.sh && \
    echo 'port="$2"' >> /usr/local/bin/wait-for-db.sh && \
    echo 'shift 2' >> /usr/local/bin/wait-for-db.sh && \
    echo 'cmd="$@"' >> /usr/local/bin/wait-for-db.sh && \
    echo 'echo "Esperando PostgreSQL en $host:$port..."' >> /usr/local/bin/wait-for-db.sh && \
    echo 'until pg_isready -h "$host" -p "$port" -U postgres; do' >> /usr/local/bin/wait-for-db.sh && \
    echo '  echo "PostgreSQL no disponible - esperando..."' >> /usr/local/bin/wait-for-db.sh && \
    echo '  sleep 2' >> /usr/local/bin/wait-for-db.sh && \
    echo 'done' >> /usr/local/bin/wait-for-db.sh && \
    echo 'echo "PostgreSQL listo - ejecutando comando"' >> /usr/local/bin/wait-for-db.sh && \
    echo 'exec $cmd' >> /usr/local/bin/wait-for-db.sh && \
    chmod +x /usr/local/bin/wait-for-db.sh

# Copiar código fuente
COPY . /app/

# Variables de entorno
ENV PYTHONPATH=/app
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Crear directorio de logs
RUN mkdir -p /app/LOGS

# Exponer puerto
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Comando usando script creado directamente en el contenedor
CMD ["/usr/local/bin/wait-for-db.sh", "postgres-db", "5432", "--", "python", "app.py"]