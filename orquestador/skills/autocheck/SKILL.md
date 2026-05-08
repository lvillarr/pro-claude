# Skill: autocheck — Diagnóstico y auto-corrección del sistema multiagente

> **Agente:** Orquestador — Subgerente de Mejora Continua

## Propósito

Revisar la integridad estructural del sistema multiagente y aplicar correcciones seguras sin intervención del usuario. Detecta inconsistencias en CLAUDE.md, skills, archivos de datos y configuración. Lo que puede corregir solo, lo corrige y commitea. Lo que requiere decisión humana, lo escala por `tasks/lessons.md`.

## Modos de operación

| Modo | Cuándo | Qué hace |
|---|---|---|
| **Diagnóstico** (cron automático) | Lunes 8:03am vía `tasks/run_autocheck.sh` | Solo lee y reporta. No escribe ni commitea. Log en `tasks/logs/`. |
| **Reparación** (manual) | Tú abres Claude Code y ejecutas `/autocheck` | Lee, analiza, aplica correcciones seguras con tu aprobación en cada paso, commitea. |

En modo diagnóstico el sistema actúa como auditor: encuentra el problema, lo documenta, espera que tú decidas. En modo reparación actúa como ejecutor: propone cada cambio, tú apruebas, commitea.

## Cuándo usar modo reparación

- Después de revisar el log del cron y ver anomalías
- Cuando agregás un nuevo agente o skill
- Antes de un trabajo de orquestación importante

---

## Protocolo

### Paso 1 — Inventario real del sistema

Usando `list_dir` y `read_file`, construir el mapa actual:

```
Para cada agente en agentes/{EO,TD,IA,DA}/:
  - Leer CLAUDE.md → extraer tabla "Skills invocables"
  - Listar agentes/{X}/skills/ → directorios reales

Para orquestador/:
  - Leer CLAUDE.md → extraer tabla "Skills invocables"
  - Listar orquestador/skills/ → directorios reales

Para skills/ (globales):
  - Listar skills/ → directorios reales
```

### Paso 2 — Checks estructurales

#### Check A — Skills invocables sin directorio real

Para cada skill en tabla "Skills invocables" de cada CLAUDE.md:
- Verificar que exista el directorio y SKILL.md indicado en columna "Ruta"
- Si no existe: **ALERTA** → escalar (no se puede auto-corregir sin saber el contenido)

#### Check B — Directorios de skills sin entrada en tabla

Para cada directorio en `agentes/{X}/skills/`:
- Verificar que aparezca en la tabla "Skills invocables" del CLAUDE.md correspondiente
- Si no aparece: **AUTO-CORREGIR** → agregar fila a la tabla con ruta correcta y descripción genérica

#### Check C — Skills globales referenciadas pero inexistentes

Buscar en todos los CLAUDE.md referencias a `skills/*/SKILL.md`:
- Verificar que el archivo existe
- Si no: **ALERTA** → escalar

#### Check D — Convención de archivos en `datos/`

Listar todos los archivos en `datos/` (no subdirectorios):
- Patrón válido: `YYYY-MM-DD_tipo-descripcion.ext`
- Tipos válidos: `reporte`, `analisis`, `script`, `plantilla`, `kpi`, `diagnostico`, `spec`, `plan`, `review`, `proceso-bpmn`, `arquitectura`, `autocheck`
- Si archivo no cumple: **REGISTRAR** en reporte (no renombrar — puede ser archivo fuente del usuario)

#### Check E — `tasks/lessons.md` con ítems sin resolver

Leer `tasks/lessons.md`:
- Si hay entradas con más de 30 días sin regla nueva asociada en `orquestador/CLAUDE.md`: **ALERTA** → escalar
- Si el archivo está vacío: registrar en reporte (no es error, es sistema nuevo)

#### Check F — TEMPLATE_GUIDE.md vs estructura real

Comparar la estructura de directorios documentada en `TEMPLATE_GUIDE.md` sección 2 con el árbol real:
- Si hay directorio real no documentado: **REGISTRAR** en reporte
- Si TEMPLATE_GUIDE menciona directorio/archivo que no existe: **ALERTA** → escalar

### Paso 3 — Aplicar correcciones automáticas

**Solo se auto-corrigen** cambios idempotentes y reversibles vía git:

| Corrección | Condición |
|---|---|
| Agregar fila faltante en tabla Skills invocables | Directorio existe con SKILL.md válido |
| Corregir nombre de skill en tabla (si directorio es inequívoco) | Solo 1 directorio candidato |
| Agregar entrada en `tasks/lessons.md` para cada alerta | Siempre |

Cada corrección aplicada: usar `bash` para `git add` + `git commit` con mensaje descriptivo.

### Paso 4 — Generar reporte

```
datos/YYYY-MM-DD_autocheck-sistema.md
```

Estructura del reporte:

```markdown
# Autocheck Sistema Multiagente — YYYY-MM-DD

**Ejecutado por:** Orquestador (automático)
**Agentes revisados:** EO, TD, IA, DA, Orquestador
**Resultado global:** OK / CON ALERTAS / CON CORRECCIONES

---

## Correcciones aplicadas

| Check | Agente | Detalle | Acción tomada |
|---|---|---|---|

## Alertas — requieren decisión humana

| Check | Agente | Detalle | Acción recomendada |
|---|---|---|---|

## Sin anomalías

| Check | Resultado |
|---|---|
| A — Skills sin directorio | OK |
| B — Directorios sin tabla | OK |
| C — Skills globales | OK |
| D — Convención datos/ | OK |
| E — lessons.md | OK |
| F — TEMPLATE_GUIDE | OK |
```

### Paso 5 — Escalar alertas

Si hay alertas (requieren decisión humana):
1. Agregar entrada en `tasks/lessons.md` con el patrón estándar
2. Si el cron tiene acceso a Telegram: enviar mensaje al usuario con resumen de alertas (máx 5 líneas)

Si no hay alertas ni correcciones: igual guardar reporte con estado OK.

---

## Límites — qué NO hace autocheck

- No modifica `settings.json` (riesgo de romper MCP servers)
- No edita contenido de SKILL.md (solo detecta ausencia)
- No renombra archivos en `datos/` (pueden ser archivos fuente del usuario)
- No toca `bot.py` ni archivos Python
- No elimina nada (solo agrega o corrige referencias en tablas)

---

## Restricciones

- Si un check produce resultado ambiguo (más de 1 candidato): ALERTA, no auto-corregir
- Toda corrección aplicada debe quedar en commit git con mensaje explicativo
- El reporte se guarda siempre, incluso si no hay anomalías (evidencia de ejecución)
- Si `datos/arauco_mc.db` no es accesible: registrar en reporte, continuar con checks restantes
