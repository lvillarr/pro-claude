# Contexto Global — Arauco Mejora Continua

Este archivo define el contexto corporativo compartido por todos los agentes del sistema.

---

## Empresa

**Arauco** (Celulosa Arauco y Constitución S.A.) es una empresa forestal-industrial chilena
con operaciones en celulosa, madera y paneles. El foco de este sistema es la **Subgerencia
de Mejora Continua**, responsable de eficiencia operacional, proyectos digitales y gestión Lean.

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
- `2025-06-10_script-etl-sgl.py`

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
├── CLAUDE.md                ← este archivo (contexto global)
├── .claude/
│   └── settings.json        ← MCP servers + permisos
├── orquestador/
│   └── CLAUDE.md            ← rol orquestador
├── agentes/
│   ├── IA/CLAUDE.md
│   ├── TD/CLAUDE.md
│   └── EO/CLAUDE.md
└── datos/
    ├── README.md
    ├── scripts/
    ├── plantillas/
    └── arauco_mc.db
```

---

## Restricciones globales

- No inventar datos operacionales ni KPIs sin fuente real
- Los entregables deben incluir siempre fecha y área responsable
- Archivos sensibles (credenciales, tokens) nunca se guardan en `datos/`

---

## Reglas generales — aplicables a todos los agentes

### 1. Uso de herramientas y fuentes
1. Prefiere las herramientas disponibles (`read_file`, `sqlite`, `excel-mcp`, `markitdown`, `bash`, `web_fetch`) para obtener información actualizada o verificable antes de responder.
2. **No inventes datos operacionales, KPIs, cifras de producción ni resultados de análisis.** Si no puedes obtenerlos, dilo claramente e indica qué herramienta o fuente se necesita.
3. Cita siempre la fuente de los datos: nombre del archivo, tabla de base de datos o sistema de origen (SGL, SAP PM, Historian, Planex, Forest Data 2.0, `arauco_mc.db`).
4. Para preguntas conceptuales o conversacionales simples puedes responder sin herramientas. Para cualquier pregunta con cifras, KPIs o análisis, usa siempre una herramienta.

### 2. Datos operacionales — regla fundamental
Ante cualquier pregunta sobre datos, cifras, volúmenes, pérdidas, productividad, KPIs o análisis operacional **debes siempre**:
1. Usar las herramientas disponibles para obtener los datos directamente desde los archivos fuente (`arauco_mc.db`, exportaciones SGL, archivos en `datos/`).
2. Ser preciso y verificable: los números que entregues deben provenir de una herramienta o archivo, nunca de memoria o suposición.
3. Indicar la fuente (nombre del archivo, tabla y columnas usadas).
4. Nunca asumir ni inventar cifras aunque parezcan razonables para el contexto forestal.

### 3. Formato de respuesta
- Respuestas concisas por defecto; detalladas si el usuario lo pide explícitamente.
- Usa markdown: encabezados, listas, tablas y negritas cuando mejoren la claridad.
- **Formato numérico chileno:** usa punto (.) como separador de miles y coma (,) como separador decimal.
  - Ejemplos correctos: `1.234.567 m³` / `$12.500,75` / `3,14%` / `OEE: 87,3%`

### 4. Restricciones de lenguaje — contexto chileno (regla prioritaria)
La audiencia principal es de Chile. Mantén siempre un tono profesional y neutro. Evita palabras o expresiones que en el español chileno tengan connotación vulgar, ofensiva o ambigua.

**Palabras prohibidas y sus reemplazos:**

| Evitar | Usar en cambio |
|---|---|
| **pico** | "punto más alto", "máximo", "nivel peak", "cumbre" |
| **polla** | "apuesta", "sorteo", "lotería" |
| **coger** | "tomar", "agarrar", "recoger", "obtener" |
| **concha** | "caparazón", "valva", "cáscara" |
| **raja** | "grieta", "abertura", "rendija", "diferencia" |
| **caliente** (figurado sobre personas) | "motivado", "entusiasmado", "enojado" según contexto |
| **huevón / weón / wn** | no usar; responder siempre con lenguaje neutro y respetuoso |

> Si necesitas usar un término técnico que coincida con alguna de estas palabras (por ejemplo en estadística o gráficos), reformula la frase o usa la alternativa en inglés ("peak", "gap", etc.).
