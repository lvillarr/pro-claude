# Auditoria de Consistencia Multi-Agente

Al ser invocado, ejecutar los checks A-F definidos en `rubric.json` (mismo directorio):

1. **A — CLAUDE.md drift**: verificar divergencias entre CLAUDE.md global y de cada agente (IA, TD, EO, DA, orquestador)
2. **B — Skill scope leakage**: skills globales usados por un solo agente; skills de agente en lugar equivocado
3. **C — Referencias rotas**: rutas, skills y archivos mencionados que no existen
4. **D — Herramientas no declaradas**: herramientas usadas pero ausentes en `settings.json`
5. **E — Plugins desactualizados**: plugins referenciados que no estan instalados o fueron renombrados
6. **F — Paridad bot/web UI**: comandos Telegram sin ruta FastAPI equivalente, y viceversa

Reportar como checklist con severidad (high/medium/low). **NO auto-corregir sin aprobacion explicita del usuario.**

## Invocacion recomendada

Para auditoria completa con maxima cobertura, usar 4 agentes paralelos:

> "Usa 4 agentes paralelos para auditar los CLAUDE.md de cada uno de mis agentes (IA, TD, EO, DA) por consistencia de referencias de skills, luego consolida los hallazgos."
