#!/bin/sh
# Arranca Ollama y precarga el modelo si no está ya en el volumen.
set -e
ollama serve &
PID=$!

until ollama list >/dev/null 2>&1; do sleep 1; done

if ollama list | grep -q "^${OLLAMA_MODEL} "; then
  echo "Modelo ${OLLAMA_MODEL} ya presente en el volumen"
else
  echo "Descargando ${OLLAMA_MODEL} (solo la primera vez)..."
  ollama pull "${OLLAMA_MODEL}"
fi

wait $PID
