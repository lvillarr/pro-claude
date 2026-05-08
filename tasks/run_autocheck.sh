#!/bin/bash
# Autocheck semanal del sistema multiagente Arauco MC
# Invocado por crontab: 3 8 * * 1

set -euo pipefail

PROJECT_DIR="/Users/lucianovillarroelparra/telegram-bot/proyecto_claude"
LOG_DIR="$PROJECT_DIR/tasks/logs"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
LOG_FILE="$LOG_DIR/autocheck_$TIMESTAMP.log"

mkdir -p "$LOG_DIR"

PROMPT="Eres el Orquestador — Subgerente de Mejora Continua de Arauco. Ejecuta el skill autocheck siguiendo el protocolo completo en \`orquestador/skills/autocheck/SKILL.md\`:

1. Inventariar todos los agentes (EO, TD, IA, DA) y sus skills reales vs. declarados en CLAUDE.md
2. Ejecutar los 6 checks (A al F)
3. Aplicar correcciones automáticas seguras y commitear cada una
4. Generar reporte en \`datos/YYYY-MM-DD_autocheck-sistema.md\` (usar fecha de hoy)
5. Registrar alertas en \`tasks/lessons.md\`

Trabaja de forma autónoma. No preguntes al usuario salvo que un check produzca resultado ambiguo. Al finalizar, muestra resumen de: correcciones aplicadas, alertas escaladas, checks OK."

/Users/lucianovillarroelparra/.local/bin/claude \
    --print \
    --dangerously-skip-permissions \
    "$PROMPT" \
    2>&1 | tee "$LOG_FILE"

# Mantener solo los últimos 12 logs (3 meses)
ls -t "$LOG_DIR"/autocheck_*.log 2>/dev/null | tail -n +13 | xargs rm -f 2>/dev/null || true
