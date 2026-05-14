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
CLAUDE_BIN="/Users/lucianovillarroelparra/.local/bin/claude"
CRON_ENV="$HOME/.claude/.arauco_cron.env"

mkdir -p "$LOG_DIR"

[ -x "$CLAUDE_BIN" ] || { echo "ERROR: claude no encontrado en $CLAUDE_BIN" | tee "$LOG_FILE"; exit 1; }

# ── Auth: API key tiene precedencia sobre OAuth ───────────────────────────────
# Si existe el archivo de credenciales, sourcea la API key.
# Esto evita la expiracion de tokens OAuth cuando el cron corre sin sesion activa.
if [ -f "$CRON_ENV" ]; then
    set -a
    # shellcheck source=/dev/null
    source "$CRON_ENV"
    set +a
fi

# Pre-flight: verificar autenticacion Claude (API key o OAuth)
AUTH_STATUS=$("$CLAUDE_BIN" auth status 2>/dev/null)
if ! echo "$AUTH_STATUS" | grep -q '"loggedIn": true'; then
    {
        echo "ERROR $(date): Claude no autenticado."
        echo "  Opciones:"
        echo "  1. Agregar ANTHROPIC_API_KEY real en ~/.claude/.arauco_cron.env"
        echo "  2. O ejecutar 'claude login' para renovar sesion OAuth"
    } | tee "$LOG_FILE"
    exit 1
fi

PROMPT="Eres el Orquestador — Subgerente de Mejora Continua de Arauco. Ejecuta el skill autocheck en MODO DIAGNÓSTICO siguiendo orquestador/skills/autocheck/SKILL.md:

RESTRICCIÓN MODO DIAGNÓSTICO: NO escribas archivos, NO hagas git commits, NO modifiques nada.
Solo leer, analizar y reportar por stdout.

1. Inventariar agentes (EO, TD, IA, DA) y sus skills reales vs. declarados en CLAUDE.md
2. Ejecutar los 6 checks (A al F) del rubric.json en .claude/skills/audit/
3. Para cada anomalía encontrada: describir qué está mal y qué corrección se requiere
4. Mostrar resumen final: checks OK / alertas / correcciones pendientes

El usuario revisará este log y decidirá qué aplicar abriendo Claude Code manualmente."

cd "$PROJECT_DIR"

"$CLAUDE_BIN" \
    --print \
    "$PROMPT" \
    2>&1 | tee "$LOG_FILE"

echo "" >> "$LOG_FILE"
echo "--- Log generado: $TIMESTAMP ---" >> "$LOG_FILE"
echo "--- Para aplicar correcciones: abrir Claude Code en proyecto_claude y ejecutar /autocheck ---" >> "$LOG_FILE"

# Mantener solo los últimos 12 logs (3 meses)
ls -t "$LOG_DIR"/autocheck_*.log 2>/dev/null | tail -n +13 | xargs rm -f 2>/dev/null || true
