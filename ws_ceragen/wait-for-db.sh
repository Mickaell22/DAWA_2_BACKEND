#!/bin/bash
# 🕐 Script de espera para PostgreSQL
set -e

host="$1"
port="$2"
shift 2
cmd="$@"

echo "⏳ Esperando a que PostgreSQL esté disponible en $host:$port..."

until pg_isready -h "$host" -p "$port" -U postgres; do
  >&2 echo "🔄 PostgreSQL no está disponible - esperando..."
  sleep 2
done

>&2 echo "✅ PostgreSQL está listo - ejecutando comando"
exec $cmd