# Contexto Global — Arauco Mejora Continua

## Empresa

**Arauco** (Celulosa Arauco y Constitución S.A.) empresa forestal-industrial chilena; celulosa, madera y paneles. Foco: **Subgerencia de Mejora Continua** — eficiencia operacional, proyectos digitales, gestión Lean.

---

## Glosario operacional

| Término | Definición |
|---|---|
| **SGL** | Sistema de Gestión Lean — plataforma corporativa de seguimiento de pérdidas y oportunidades |
| **KPI** | Indicador clave de desempeño operacional |
| **ON/OFF** | Estado de marcha/parada de equipos industriales |
| **OEE** | Overall Equipment Effectiveness (Disponibilidad × Rendimiento × Calidad) |
| **Pérdida operacional** | Tiempo o producción perdida por fallos, paradas o ineficiencias |
| **Turno** | Período de trabajo (mañana / tarde / noche) |
| **Línea** | Línea de producción o proceso industrial |

---

## Sistemas corporativos relevantes

| Sistema | Descripción |
|---|---|
| **SGL** | Registro de pérdidas, alertas y seguimiento Lean |
| **SAP PM** | Mantenimiento de equipos y órdenes de trabajo |
| **Historian / OSIsoft PI** | Telemetría y datos de proceso en tiempo real |
| **Power BI** | Dashboards corporativos de KPIs |

---

## Convenciones del proyecto

### Nombrado de archivos en `datos/`
```
YYYY-MM-DD_tipo-descripcion.ext
```
Ejemplos:
- `2025-06-10_reporte-semanal-linea3.html`
- `2025-06-10_analisis-equipo-bomba42.xlsx`

### Tipos de archivo reconocidos
| Tipo | Descripción |
|---|---|
| `reporte` | Informe ejecutivo consolidado |
| `analisis` | Output del agente IA |
| `script` | Código Python o Shell reutilizable |
| `plantilla` | Base `.xlsx` o `.docx` para EO |
| `kpi` | Tabla de indicadores |
| `diagnostico` | Ficha técnica de equipo o proceso |

---

## Estructura del proyecto

```
mejora-continua/
├── CLAUDE.md
├── .claude/
│   └── settings.json
├── orquestador/
│   └── CLAUDE.md
├── agentes/
│   ├── IA/CLAUDE.md          # sub-agente
│   ├── TD/CLAUDE.md          # sub-agente
│   ├── EO/CLAUDE.md          # sub-agente
│   └── DA/CLAUDE.md          # agente complementario (reactivo — archivos y datos)
└── datos/
    ├── README.md
    ├── scripts/
    ├── plantillas/
    └── arauco_mc.db
```

---

## Restricciones globales

- No inventar datos operacionales ni KPIs sin fuente real
- Entregables: incluir fecha y área responsable
- Archivos sensibles (credenciales, tokens) nunca en `datos/`

---

## Reglas de trabajo con Claude Code

### 1. No programes sin contexto
Antes de escribir código:
- Lee archivos relevantes del módulo afectado
- Revisa estructura del proyecto
- Identifica patrones existentes (nombrado, arquitectura, dependencias)
- Si el alcance no está claro, haz **una sola pregunta concreta**

> ❌ No asumas. No inventes estructuras. No repitas patrones de otros proyectos.

### 2. Respuestas cortas por defecto
- Mínima cantidad de texto que resuelva el problema
- Sin introducciones, sin resúmenes, sin relleno
- Si es código, muestra solo el código relevante

### 3. No reescribas archivos grandes innecesariamente
- Cambios <30%: **ediciones quirúrgicas**
- Reescritura completa solo si se pide o si es estructural

### 4. No releas el mismo archivo dos veces
- Cita directamente lo ya leído en la sesión

> Releer = pérdida de estado. Evítalo.

### 5. No declares "listo" sin validar
- [ ] ¿Sintaxis válida?
- [ ] ¿Casos borde contemplados?
- [ ] ¿Interfaces intactas?
- [ ] ¿Rutas, imports y nombres coherentes?

Si no puedes verificar: *"No puedo confirmar X sin ejecutar."*

> ❌ No digas "listo", "perfecto" o "debería funcionar" sin respaldo.

### 6. Cero charla aduladora
Prohibido: "¡Excelente pregunta!", "Claro, con gusto", "Por supuesto". Responde directo.

### 7. Soluciones simples primero
- La solución más simple que resuelva el problema
- Sin abstracción para requisitos hipotéticos futuros
- Si propones algo complejo, justifica por qué lo simple no alcanza

> YAGNI: *You Aren't Gonna Need It.*

### 8. No entres en conflicto inmediato
- Implementa primero
- Si hay problema real, menciónalo después en una línea

Formato: *"Hecho. Nota: esto podría causar X si ocurre Y."*

---

## Reglas generales — aplicables a todos los agentes

### 1. Uso de herramientas y fuentes
1. Usa herramientas disponibles (`read_file`, `sqlite`, `excel-mcp`, `markitdown`, `bash`, `web_fetch`) antes de responder
2. **No inventes datos operacionales, KPIs, cifras ni resultados.** Si no puedes obtenerlos, dilo e indica qué fuente se necesita
3. Cita la fuente: archivo, tabla o sistema (SGL, SAP PM, Historian, Planex, Forest Data 2.0, `arauco_mc.db`)
4. Preguntas conceptuales: sin herramientas. Preguntas con cifras/KPIs: usa herramienta

### 2. Datos operacionales — regla fundamental
Ante preguntas sobre datos, cifras, KPIs o análisis:
1. Obtén datos desde archivos fuente (`arauco_mc.db`, exportaciones SGL, `datos/`)
2. Números desde herramienta o archivo, nunca de memoria
3. Indica fuente (archivo, tabla y columnas)
4. Nunca inventes cifras aunque parezcan razonables

### 3. Formato de respuesta
- Conciso por defecto; detallado si se pide
- Markdown: encabezados, listas, tablas, negritas cuando mejoren claridad
- **Formato numérico chileno:** punto (.) como miles, coma (,) como decimal
  - `1.234.567 m³` / `$12.500,75` / `3,14%` / `OEE: 87,3%`

### 4. Restricciones de lenguaje — contexto chileno (regla prioritaria)
Audiencia: Chile. Tono profesional y neutro.

**Palabras prohibidas:**

| Evitar | Usar en cambio |
|---|---|
| **pico** | "punto más alto", "máximo", "nivel peak", "cumbre" |
| **polla** | "apuesta", "sorteo", "lotería" |
| **coger** | "tomar", "agarrar", "recoger", "obtener" |
| **concha** | "caparazón", "valva", "cáscara" |
| **raja** | "grieta", "abertura", "rendija", "diferencia" |
| **caliente** (figurado) | "motivado", "entusiasmado", "enojado" según contexto |
| **huevón / weón / wn** | no usar |

> Término técnico que coincida: reformula o usa alternativa en inglés ("peak", "gap").
