# Auditoria de Consistencia Multi-Agente

Al ser invocado, ejecutar estos pasos:

1. Listar todos los agentes en `agents/` y sus archivos `CLAUDE.md`
2. Cruzar referencias de skills — marcar skills mencionados en algun `CLAUDE.md` pero ausentes en `.claude/skills/`
3. Verificar paridad de features entre bot Telegram y web UI (comparar handlers)
4. Reportar inconsistencias como checklist; **NO auto-corregir sin aprobacion explicita del usuario**
