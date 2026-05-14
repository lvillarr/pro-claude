#!/bin/bash
# Autocheck semanal del sistema multiagente Arauco MC
# Invocado por crontab: 3 8 * * 1
# MODO DIAGNÓSTICO: solo lee y reporta. No escribe archivos ni commitea.
# Para aplicar correcciones: abrir Claude Code y ejecutar /autocheck manualmente.

set -euo pipefail

PROJECT_DIR="/Users/lucianovillarroelparra/telegram-bot/proyecto_claude"
LOG_DIR="$PROJECT_DIR/tasks/logs"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
LOG_FILE="$LOG_DIR/autocheck_$TIMESTAMP.log"

mkdir -p "$LOG_DIR"

# Pre-flight: verificar autenticacion Claude antes de correr
AUTH_STATUS=$(/Users/lucianovillarroelparra/.local/bin/claude auth status 2>/dev/null)
if ! echo "$AUTH_STATUS" | grep -q '"loggedIn": true'; then
    echo "ERROR $(date): Claude no autenticado. Ejecutar 'claude login' manualmente y reintentar." | tee "$LOG_FILE"
    exit 1
fi

PROMPT="Eres el Orquestador — Subgerente de Mejora Continua de Arauco. Ejecuta el skill autocheck en MODO DIAGNÓSTICO siguiendo orquestador/skills/autocheck/SKILL.md:

RESTRICCIÓN MODO DIAGNÓSTICO: NO escribas archivos, NO hagas git commits, NO modifiques nada.
Solo leer, analizar y reportar por stdout.

1. Inventariar agentes (EO, TD, IA, DA) y sus skills reales vs. declarados en CLAUDE.md
2. Ejecutar los 6 checks (A al F)
3. Para cada anomalía encontrada: describir qué está mal y qué corrección se requiere
4. Mostrar resumen final: checks OK / alertas / correcciones pendientes

El usuario revisará este log y decidirá qué aplicar abriendo Claude Code manualmente."

cd "$PROJECT_DIR"

/Users/lucianovillarroelparra/.local/bin/claude \
    --print \
    "$PROMPT" \
    2>&1 | tee "$LOG_FILE"

echo "" >> "$LOG_FILE"
echo "--- Log generado: $TIMESTAMP ---" >> "$LOG_FILE"
echo "--- Para aplicar correcciones: abrir Claude Code en proyecto_claude y ejecutar /autocheck ---" >> "$LOG_FILE"

# Mantener solo los últimos 12 logs (3 meses)
ls -t "$LOG_DIR"/autocheck_*.log 2>/dev/null | tail -n +13 | xargs rm -f 2>/dev/null || true
