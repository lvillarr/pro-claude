# Contexto Global — Arauco Mejora Continua

## Empresa

**Arauco** (Celulosa Arauco y Constitución S.A.) empresa forestal-industrial chilena; celulosa, madera y paneles. Foco: **Subgerencia de Mejora Continua** — eficiencia operacional, proyectos digitales, gestión Lean.

---

## Glosario operacional

| Término | Definición |
|---|---|
| **SGL** | Sistema de Gestión Lean — seguimiento de pérdidas, alertas y oportunidades |
| **KPI** | Indicador clave de desempeño operacional |
| **ON/OFF** | Estado de marcha/parada de equipos industriales |
| **OEE** | Overall Equipment Effectiveness (Disponibilidad × Rendimiento × Calidad) |
| **Pérdida operacional** | Tiempo o producción perdida por fallos, paradas o ineficiencias |
| **Turno** | Período de trabajo (mañana / tarde / noche) |
| **Línea** | Línea de producción o proceso industrial |

---

## Sistemas corporativos

| Sistema | Descripción |
|---|---|
| **SGL** | Registro de pérdidas y seguimiento Lean |
| **SAP PM** | Mantenimiento de equipos y órdenes de trabajo |
| **Historian / OSIsoft PI** | Telemetría y datos de proceso en tiempo real |
| **Power BI** | Dashboards corporativos de KPIs |

---

## Convenciones del proyecto

Archivos en `datos/`: `YYYY-MM-DD_tipo-descripcion.ext` — tipos: `reporte`, `analisis`, `script`, `plantilla`, `kpi`, `diagnostico`.

Estructura: `orquestador/`, `agentes/{IA,TD,EO,DA}/`, `skills/` (globales), `datos/`. Ver `ls` para detalle.

---

## Restricciones globales

- **No inventar datos operacionales, KPIs ni cifras.** Si no puedes obtenerlos desde fuente, dilo e indica qué se necesita.
- Siempre cita fuente: archivo, tabla o sistema (`arauco_mc.db`, SGL, SAP PM, Historian, Planex, `datos/`).
- Entregables: incluir fecha y área responsable.
- Archivos sensibles (credenciales, tokens) nunca en `datos/`.

---

## Aprobacion y Autonomia

- **NUNCA** configurar cron jobs, tareas programadas o flujos automatizados con permisos de auto-fix/auto-commit sin aprobacion explicita del usuario.
- "Autonomia" en este proyecto = auto-auditoria y auto-reporte. **NO** ejecucion ni aplicacion de cambios sin supervision.
- Siempre requerir confirmacion humana antes de aplicar cambios provenientes de checks automatizados.

---

## Flujo Git

- Despues de cada commit: hacer push inmediatamente, salvo indicacion contraria.
- En releases: hacer push de tags tambien (`git push --tags`).

---

## Preferencias de Plugins y Skills

- Code reviews: usar skill local `caveman-review`, **no** `gh` CLI ni herramientas web.
- Cuando el usuario mencione un skill por nombre (`superpowers`, `ultrathink`, `claude-mem`, `branding-arauco`, `bpmn`, `audit`, `release`, `weekly-retro`, etc.): revisar `.claude/skills/` y plugins instalados **antes** de usar herramientas genericas.

---

## Estructura Multi-Agente

- Sistema con 5 agentes (IA, TD, EO, DA, orquestador) y reglas de scope de skills.
- Algunos skills son exclusivos de un agente (ej: `bpmn` → agente EO), no globales.
- Al agregar/quitar un skill: actualizar **todos** los CLAUDE.md relevantes entre agentes. Sacar del global si se scopea a un solo agente.
- Bot Telegram y web UI deben tener paridad de features. Al cambiar uno, revisar el otro.

---

## Reglas de trabajo con Claude Code

### 1. Lee antes de escribir
Antes de código: lee archivos del módulo afectado, identifica patrones existentes. Si el alcance no está claro, haz una sola pregunta concreta.

### 2. No reescribas archivos grandes innecesariamente
Cambios <30%: ediciones quirúrgicas. Reescritura completa solo si se pide o es estructural.

### 3. No releas el mismo archivo dos veces
Cita directamente lo ya leído en la sesión.

### 4. Valida antes de declarar listo
Sintaxis válida, casos borde, interfaces intactas, rutas y nombres coherentes. Si no puedes verificar: *"No puedo confirmar X sin ejecutar."*

### 5. Soluciones simples primero
La solución más simple que resuelva el problema. Sin abstracción para requisitos hipotéticos.

### 6. Commit + push automático
Cuando el fix está listo y el contexto es claro: commit y push sin preguntar.

---

## Reglas generales — todos los agentes

### Datos y herramientas
- Usa herramientas disponibles (`sqlite`, `excel-mcp`, `markitdown`, `bash`) antes de responder.
- Números desde herramienta o archivo, **nunca de memoria**. Preguntas conceptuales: sin herramientas.

### Formato de respuesta
- Conciso por defecto; detallado si se pide.
- **Formato numérico chileno:** punto como miles, coma como decimal — `1.234.567 m³` / `$12.500,75` / `3,14%`.

### Restricciones de lenguaje — contexto chileno (regla prioritaria)
Audiencia: Chile. Tono profesional y neutro.

| Evitar | Usar en cambio |
|---|---|
| **pico** | "punto más alto", "máximo", "nivel peak" |
| **polla** | "apuesta", "sorteo", "lotería" |
| **coger** | "tomar", "agarrar", "obtener" |
| **concha** | "caparazón", "valva", "cáscara" |
| **raja** | "grieta", "abertura", "diferencia" |
| **caliente** (figurado) | "motivado", "enojado" según contexto |
| **huevón / weón / wn** | no usar |

Término técnico que coincida: reformula o usa alternativa en inglés ("peak", "gap").
