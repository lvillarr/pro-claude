# Guía de Template — Sistema Multiagente Arauco + Bot Telegram

Guía completa para replicar desde cero el sistema de agentes Claude Code y el bot de Telegram con artefactos. Cubre arquitectura, configuración, skills, tools, MCP servers y convenciones.

---

## Índice

1. [Visión general](#1-visión-general)
2. [Estructura de archivos](#2-estructura-de-archivos)
3. [Claude Code — configuración](#3-claude-code--configuración)
4. [Jerarquía de CLAUDE.md](#4-jerarquía-de-claudemd)
5. [Agentes — perfil y capacidades](#5-agentes--perfil-y-capacidades)
6. [Skills por agente](#6-skills-por-agente)
7. [MCP Servers](#7-mcp-servers)
8. [Protocolo de orquestación](#8-protocolo-de-orquestación)
9. [Convenciones de datos](#9-convenciones-de-datos)
10. [Bot de Telegram — arquitectura](#10-bot-de-telegram--arquitectura)
11. [Planner MC — arquitectura](#11-planner-mc--arquitectura)
12. [Web UI — arquitectura](#12-web-ui--arquitectura)
13. [Checklist para nuevo proyecto](#13-checklist-para-nuevo-proyecto)
14. [Adaptaciones por cliente](#14-adaptaciones-por-cliente)

---

## 1. Visión general

Sistema multiagente en Claude Code donde un **Orquestador** coordina cuatro sub-agentes especializados (EO, TD, IA, DA) para resolver problemas de negocio en Arauco. El sistema se usa en dos modalidades:

| Modalidad | Contexto | Cómo se activa |
|---|---|---|
| **Claude Code** | Análisis estratégico, generación de entregables, diagnóstico de procesos | Sesiones en VSCode / CLI |
| **Bot Telegram** | Consultas rápidas, generación de artefactos, análisis de documentos desde el celular | Bot Python en Railway |

El bot carga los CLAUDE.md de los agentes como SYSTEM_PROMPT y llama a la API de Claude directamente. El sistema de agentes en Claude Code usa los mismos CLAUDE.md pero opera con herramientas (MCP, bash, Python) y puede generar archivos reales.

---

## 2. Estructura de archivos

```
telegram-bot/
├── bot.py                          ← bot completo en un solo archivo
├── rag.py                          ← búsqueda semántica (ChromaDB + VoyageAI)
├── requirements.txt
└── proyecto_claude/                ← raíz del proyecto Claude Code
    ├── CLAUDE.md                   ← contexto corporativo + reglas globales
    ├── TEMPLATE_GUIDE.md           ← este archivo
    ├── README.md
    ├── .claude/
    │   ├── settings.json           ← MCP servers + permisos
    │   └── settings.local.json     ← permisos adicionales locales
    ├── orquestador/
    │   ├── CLAUDE.md               ← identidad + protocolo Orquestador
    │   └── skills/
    │       ├── spec/SKILL.md       ← encuadre estratégico MECE
    │       ├── plan/SKILL.md       ← delegación por agente
    │       ├── review/SKILL.md     ← validación Paso 3.5 + síntesis Minto
    │       └── ship/SKILL.md       ← entregable ejecutivo final
    ├── agentes/
    │   ├── EO/
    │   │   ├── CLAUDE.md           ← Jefe Excelencia Operacional
    │   │   └── skills/
    │   │       ├── bpmn/SKILL.md   ← modelado AS-IS / TO-BE (EO-exclusivo)
    │   │       ├── spec/SKILL.md
    │   │       ├── plan/SKILL.md
    │   │       ├── build/SKILL.md
    │   │       ├── test/SKILL.md
    │   │       ├── review/SKILL.md
    │   │       └── ship/SKILL.md
    │   ├── TD/
    │   │   ├── CLAUDE.md           ← Jefe Transformación Digital
    │   │   └── skills/
    │   │       ├── spec/SKILL.md
    │   │       ├── plan/SKILL.md
    │   │       ├── build/SKILL.md
    │   │       ├── test/SKILL.md
    │   │       ├── review/SKILL.md
    │   │       └── ship/SKILL.md
    │   ├── IA/
    │   │   ├── CLAUDE.md           ← Jefe Inteligencia Artificial
    │   │   └── skills/
    │   │       ├── spec/SKILL.md
    │   │       ├── plan/SKILL.md
    │   │       ├── build/SKILL.md
    │   │       ├── test/SKILL.md
    │   │       ├── review/SKILL.md
    │   │       └── ship/SKILL.md
    │   └── DA/
    │       ├── CLAUDE.md           ← Analista de Datos (reactivo)
    │       └── skills/
    │           ├── spec/SKILL.md
    │           ├── plan/SKILL.md
    │           ├── build/SKILL.md
    │           ├── test/SKILL.md
    │           ├── review/SKILL.md
    │           └── ship/SKILL.md
    ├── skills/                     ← skills globales (todos los agentes)
    │   ├── branding-arauco/SKILL.md
    │   └── office-files/SKILL.md
    ├── datos/                      ← todos los archivos de trabajo
    │   ├── arauco_mc.db            ← SQLite con históricos operacionales
    │   ├── fuentes/                ← archivos de entrada (Excel, PDF, etc.)
    │   ├── procesos/               ← BPMN, análisis de proceso
    │   ├── reportes/               ← HTML, dashboards generados
    │   └── scripts/                ← Python ETL y utilitarios
    └── tasks/
        └── lessons.md              ← lecciones aprendidas del Orquestador
```

---

## 3. Claude Code — configuración

### `.claude/settings.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "./datos", "./agentes", "./orquestador", "./skills", "./tasks"]
    },
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite",
               "./datos/arauco_mc.db"]
    },
    "excel-mcp": {
      "command": "npx",
      "args": ["-y", "@negokaz/excel-mcp-server"],
      "env": {
        "EXCEL_MCP_PAGING_CELLS_LIMIT": "4000"
      }
    },
    "markitdown": {
      "command": "uvx",
      "args": ["markitdown-mcp"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  },
  "permissions": {
    "allow": [
      "Bash(python3:*)",
      "Bash(pip:*)",
      "Bash(pip3:*)",
      "Bash(git:*)",
      "Bash(uvx:*)"
    ],
    "deny": ["Bash(rm -rf *)"]
  }
}
```

### `.claude/settings.local.json`

Permisos adicionales para uso local (no commitear con credenciales):

```json
{
  "permissions": {
    "allow": [
      "Bash(git add:*)",
      "Bash(git commit -m ':*)",
      "Bash(git push:*)",
      "Bash(python3 -c ':*)",
      "Bash(pip install:*)"
    ]
  }
}
```

---

## 4. Jerarquía de CLAUDE.md

Claude Code carga los CLAUDE.md en este orden (de más general a más específico):

```
~/.claude/CLAUDE.md                     ← reglas globales del usuario
proyecto_claude/CLAUDE.md               ← contexto Arauco + convenciones
orquestador/CLAUDE.md                   ← (cuando se trabaja como Orquestador)
agentes/{EO,TD,IA,DA}/CLAUDE.md        ← (cuando se trabaja como agente)
```

### `proyecto_claude/CLAUDE.md` — secciones clave

| Sección | Contenido |
|---|---|
| Empresa | Descripción de Arauco y foco en Mejora Continua |
| Glosario operacional | SGL, KPI, OEE, pérdida operacional, turno, línea |
| Sistemas corporativos | SGL, SAP PM, Historian/OSIsoft PI, Power BI |
| Convenciones del proyecto | Nomenclatura `datos/`, estructura de carpetas |
| Restricciones globales | No inventar datos, citar fuente siempre |
| Reglas Claude Code | Leer antes de escribir, no reescribir en exceso, validar antes de declarar listo, commit+push automático |
| Reglas de formato | Formato numérico chileno (punto miles, coma decimal) |
| Restricciones de lenguaje | Evitar términos con doble sentido en Chile (pico, coger, etc.) |

---

## 5. Agentes — perfil y capacidades

### 5.1 Orquestador — Subgerente de Mejora Continua

**Modelo:** `claude-sonnet-4-6`

**Rol:** Líder estratégico. Diagnóstica, delega, integra resultados y entrega al usuario.

**Estilo:** McKinsey/BCG — hipótesis, impacto cuantificado, comunicación ejecutiva (pirámide Minto).

**Cuándo activa cada sub-agente:**

| Sub-agente | Criterio de activación |
|---|---|
| EO | Diagnóstico de proceso, pérdidas operacionales, KPIs, rediseño Lean |
| TD | Telemetría, integración de sistemas, automatización, arquitectura de datos |
| IA | Análisis histórico, modelos predictivos, dashboards, agentes GenAI |
| DA | Hay un archivo de datos (Excel, PDF, Word) que procesar — transversal y reactivo |

**Secuencias de orquestación:**

| Patrón | Cuándo | Ejemplo |
|---|---|---|
| Único agente | 1 área, causa clara | Análisis de fallas → solo IA |
| Paralelo puro | Áreas independientes | EO (KPIs) + TD (telemetría) simultáneos |
| Secuencial | Cada agente necesita el output del anterior | IA → EO (plan Lean con los datos) |
| Paralelo + convergencia | Paralelo luego síntesis | EO + IA paralelo → Orquestador integra → TD implementa |
| Reactivo con DA | Hay archivo sin procesar | DA primero → agente que usa esos datos |

---

### 5.2 EO — Excelencia Operacional

**Modelo:** `claude-sonnet-4-6`

**Rol:** Diagnóstico de procesos, mejora continua Lean, KPIs operacionales, rediseño con BPMN.

**Expertise:** SGL, GEMBA, KAIZEN, VSM, A3/PDCA, 5S, OEE, BPMN 2.0, D.A.M.A., PMBoK.

**Dominio de conocimiento:**

| Área | Capacidades clave |
|---|---|
| Lean Management | SGL, GEMBA, KAIZEN, VSM, A3/PDCA, 5S, OEE |
| BPMN 2.0 | Diagramación AS-IS y TO-BE, análisis de valor, integración con SGL/SAP/Planex |
| D.A.M.A. | Gobierno de datos, calidad, arquitectura, diccionarios de KPIs |
| PMBoK | Charter, EDT/WBS, cronogramas, riesgos, control y cierre |

**Protocolo de entrega:**
```
ENTREGA EO:
Archivo(s): datos/YYYY-MM-DD_descripcion.ext
Hallazgos clave: [máximo 3 puntos operacionales cuantificados]
Causa raíz: [hipótesis principal con evidencia]
Limitaciones: [datos faltantes, supuestos, períodos sin cobertura]
Plan de acción: [próximos pasos con responsable, plazo y criterio de cierre]
```

**Paralelismo:** Puede ejecutarse en paralelo con TD y DA. Depende de IA cuando requiere análisis histórico previo.

---

### 5.3 TD — Transformación Digital

**Modelo:** `claude-sonnet-4-6`

**Rol:** Telemetría de equipos, sistemas de planificación forestal, integración ERP, pipelines ETL.

**Expertise:** Planex, Planex NOM, Opticort, Opti-Maq, Forest Gantt, LAMDA, Forest Data 2.0, Datalake, SAP, telemetría de dealers (Tigercat, John Deere, Develon, Liebherr, Ecoforst, Caterpillar, Volvo), Historian/OSIsoft PI.

**Principio rector:** Primero el proceso, luego la herramienta.

**Cadena de sistemas que conoce:**

| Sistema | Rol |
|---|---|
| Planex | Red de caminos, habilitación de cosecha largo plazo (1-2 años) |
| Planex NOM | Actualización última milla (1 mes antes), alternativas volteo/madereo |
| Opti-Cliente | Optimización abastecimiento al mínimo costo, plan anual mensualizado |
| Opticort | Asignación máquinas por pendiente: Terrestre / Asistido / Torre |
| Opti-Maq | Maximiza productividad, asigna equipos por zona con geo-espaciales |
| Forest Gantt | Tiempo de ejecución por proceso, minimiza tiempo total de cosecha |
| LAMDA | Trazado de líneas de madereo, optimización de soportes |
| Forest Data 2.0 | Plataforma de datos operacionales forestales |
| Datalake | Repositorio centralizado analítico |

**Protocolo de entrega:**
```
ENTREGA TD:
Archivo(s): datos/scripts/YYYY-MM-DD_script-descripcion.py
Estado: funcional / requiere credenciales / en desarrollo
Dependencias: [librerías, accesos, variables de entorno]
Limitaciones: [conectividad, integraciones pendientes, supuestos de infraestructura]
Impacto esperado: [qué habilita en el negocio forestal]
```

**Paralelismo:** Puede ejecutarse en paralelo con EO y DA. Depende de IA cuando requiere arquitectura previa.

---

### 5.4 IA — Inteligencia Artificial

**Modelo:** `claude-sonnet-4-6`

**Rol:** GenAI, agentes LangGraph/Claude API, modelos predictivos, análisis geo-espacial, dashboards interactivos.

**Expertise:** LangGraph, Claude Code/API, ML operacional (scikit-learn, XGBoost), análisis de series de tiempo, cartografía con IA (QGIS, GeoPandas, imágenes satelitales Sentinel/Landsat/Planet).

**Dominio de conocimiento:**

| Área | Capacidades clave |
|---|---|
| GenAI | Claude API, LangGraph, Agent SDK, tool use, thinking adaptativo |
| ML | Modelos predictivos de productividad, detección de anomalías, clustering |
| Geo-IA | Análisis vectorial/raster, segmentación de rodales, detección de caminos |
| Visualización | Chart.js, Plotly, dashboards HTML sin dependencias externas |

**Protocolo de entrega:**
```
ENTREGA IA:
Archivo(s): datos/YYYY-MM-DD_analisis-descripcion.ext
Hallazgos clave: [máximo 3 puntos cuantificados]
Limitaciones: [datos faltantes, supuestos, confianza del modelo]
Impacto esperado: [qué decisión o proceso mejora este entregable]
```

**Paralelismo:** Puede ejecutarse en paralelo con EO y DA. Depende de DA cuando el análisis requiere procesamiento previo de archivos externos.

---

### 5.5 DA — Analista de Datos (reactivo)

**Modelo:** `claude-sonnet-4-6`

**Rol:** Convierte archivos crudos (Excel, PDF, Word) en análisis accionables y reportes HTML interactivos. No forma parte de los flujos estándar de orquestación — se invoca cuando hay un archivo de datos o cuando cualquier flujo requiere análisis de datos estructurados.

**Protocolo de análisis:**

1. **Inspección inicial** — shape, columnas, tipos, muestra 5 filas, nulos por columna
2. **Limpieza** — nulos, duplicados, tipos incorrectos; documentar cambios
3. **Análisis** — numérico: suma/prom/min/max/distribución; categórico: frecuencias/top-10
4. **Reporte HTML** — dashboard con branding Arauco, filtros dinámicos, Chart.js, tabla filtrable

**Datos disponibles desde Telegram (formato estructurado):**

- **Excel:** JSON con `headers`, `total_filas`, `muestra_top20` (solo para tabla de detalle), `stats` por columna (para KPIs y gráficos — totalidad del archivo)
- **PDF:** texto por página con marcadores `[Página N/M]`
- **Word:** párrafos con jerarquía de secciones y tablas en markdown

**Dos contextos de operación:**

| Contexto | Datos | Responde |
|---|---|---|
| Bot Telegram | JSON pre-procesado recibido de bot.py | Texto + HTML inline |
| Claude Code (Orquestador) | Lee archivos directamente desde `datos/` | Archivos en `datos/` + bloque ENTREGA DA |

**Protocolo de entrega:**
```
ENTREGA DA:
Archivo(s): datos/YYYY-MM-DD_reporte-descripcion.html
Fuente: [archivo, hoja y columnas usadas]
Hallazgos clave: [máximo 3 puntos cuantificados]
Caveats de muestra: [total de registros vs. registros mostrados, datos faltantes]
Limitaciones: [columnas sin datos, supuestos de limpieza]
```

---

## 6. Skills por agente

### 6.1 Skills globales (todos los agentes)

| Skill | Ruta | Descripción |
|---|---|---|
| `office-files` | `skills/office-files/SKILL.md` | Leer/editar `.xlsx`, `.docx`, `.pptx`, `.pdf` con openpyxl, python-docx, python-pptx, pdfplumber |
| `branding-arauco` | `skills/branding-arauco/SKILL.md` | Identidad visual Arauco — colores, tipografía Lato, logo; aplicar silenciosamente en HTML |

**Paleta branding-arauco:**

| Nombre | HEX | Uso |
|---|---|---|
| Gris Tierra | `#696158` | Color principal, headers, fondos oscuros |
| Verde Oliva | `#BFB800` | Acentos, indicadores positivos |
| Naranja | `#EA7600` | Alertas, energía |
| Crema | `#DFD1A7` | Fondos cálidos, filas alternas |

**Logo:**
- Fondo claro: `https://arauco.com/chile/wp-content/themes/arauco/assets/img/logo-arauco.png`
- Fondo oscuro: `https://arauco.com/chile/wp-content/themes/arauco/assets/img/logo-arauco-blanco.png`

---

### 6.2 Skills del Orquestador

| Skill | Ruta | Cuándo invocar |
|---|---|---|
| `spec` | `orquestador/skills/spec/SKILL.md` | Al recibir cualquier encargo antes de activar sub-agentes; convierte solicitud ambigua en brief estratégico MECE |
| `plan` | `orquestador/skills/plan/SKILL.md` | Con brief APROBADO; produce bloques `TAREA PARA [AGENTE]:` ejecutables |
| `review` | `orquestador/skills/review/SKILL.md` | Al recibir ENTREGAs; aplica checklist Paso 3.5 y produce síntesis Minto |
| `ship` | `orquestador/skills/ship/SKILL.md` | Con review APROBADA; genera entregable ejecutivo final para el usuario |

**Flujo obligatorio del Orquestador:**
```
spec (brief APROBADO) → plan (bloques de delegación) → [sub-agentes] → review (Paso 3.5) → ship (entregable)
```

**Checklist Paso 3.5 por agente (antes de sintetizar):**

| Agente | Campos obligatorios | Señal de alerta |
|---|---|---|
| EO | Hallazgos + Causa raíz + Limitaciones + Plan de acción | Falta causa raíz o plan sin responsable |
| TD | Estado + Dependencias + Limitaciones + Impacto esperado | Estado "en desarrollo" sin plazo ni bloqueador |
| IA | Hallazgos + Limitaciones + Impacto esperado | Limitaciones vacías o confianza no declarada |
| DA | Fuente del archivo + Caveats de muestra | Cifras sin origen o sin indicar total de registros |

---

### 6.3 Skills de EO

| Skill | Descripción |
|---|---|
| `bpmn` | AS-IS y TO-BE en BPMN 2.0 con análisis de valor — **exclusivo de EO** |
| `spec` | Definición del problema operacional, KPIs y criterios de éxito |
| `plan` | EDT, cronograma, recursos, riesgos y hitos |
| `build` | BPMN TO-BE, KPIs, dashboards, scripts ETL, herramientas Lean |
| `test` | Piloto en terreno, validación de datos, KPI vs. línea base |
| `review` | GEMBA de verificación, análisis de resultados, desviaciones |
| `ship` | Lecciones aprendidas, estandarización, hand-off, registro en SGL |

---

### 6.4 Skills de TD

| Skill | Descripción |
|---|---|
| `spec` | Especificación TD: proceso, sistemas, MVP y KPIs |
| `plan` | Arquitectura de integración, fases, dependencias TI y riesgos |
| `build` | ETL, conectores API, telemetría de dealers, sincronización |
| `test` | Integridad de datos, errores, conectividad adversa |
| `review` | Seguridad, idempotencia, calidad en producción |
| `ship` | Documentación operacional, hand-off a TI, versionado |

---

### 6.5 Skills de IA

| Skill | Descripción |
|---|---|
| `spec` | Especificación de proyectos IA: datos, métricas, MVP |
| `plan` | Fases EDA → modelado → evaluación → entrega |
| `build` | EDA, feature engineering, modelos ML, agentes GenAI, dashboards |
| `test` | Métricas vs. meta, explicabilidad, validación operacional |
| `review` | Generalización, data leakage, adopción, mantenibilidad |
| `ship` | Documentación, versionado, plan de reentrenamiento, hand-off |

---

### 6.6 Skills de DA

| Skill | Descripción |
|---|---|
| `spec` | Pregunta de negocio, archivo fuente, métricas, audiencia |
| `plan` | Plan: inspección → limpieza → análisis → visualización |
| `build` | Dashboard HTML interactivo con branding Arauco y filtros dinámicos |
| `test` | Coherencia KPIs vs. fuente, caveats completos, filtros funcionales |
| `review` | Alineación con negocio forestal, cifras verificables, terminología |
| `ship` | Nombre de archivo, ENTREGA DA completo, guardar en datos/ |

---

## 7. MCP Servers

| MCP | Comando | Propósito | Quién lo usa |
|---|---|---|---|
| `filesystem` | `npx @modelcontextprotocol/server-filesystem` | Acceso completo a `datos/`, `agentes/`, `orquestador/`, `skills/`, `tasks/` | Todos |
| `sqlite` | `npx @modelcontextprotocol/server-sqlite` | Consultas sobre `datos/arauco_mc.db` — históricos operacionales | Todos |
| `excel-mcp` | `npx @negokaz/excel-mcp-server` | Leer rangos y hojas `.xlsx` sin Python (4000 celdas por página) | EO, TD, IA, DA |
| `markitdown` | `uvx markitdown-mcp` | Convertir `.docx`, `.xlsx`, `.pptx`, `.pdf` a Markdown para lectura | Todos |
| `fetch` | `npx @modelcontextprotocol/server-fetch` | Consumir APIs REST externas con autenticación (POST, headers) | TD, IA, EO |

**Nota:** El MCP `fetch` es necesario porque `WebFetch` solo soporta GET sin headers de autenticación. TD y IA necesitan `fetch` para APIs de dealers (Tigercat, JD), SGL y SAP.

---

## 8. Protocolo de orquestación

### Paso 1 — Diagnóstico estratégico (spec)

Antes de delegar, el Orquestador encuadra el problema:

```
- ¿Cuál es el problema de negocio subyacente (no el síntoma)?
- ¿Qué hipótesis iniciales tengo? (deben ser falseables)
- ¿Qué áreas están involucradas y en qué secuencia?
- ¿Qué datos existen en datos/ y cuáles faltan?
- ¿Cuál es el entregable, su audiencia y formato?
- ¿Hay dependencias entre agentes?
```

Produce: `datos/YYYY-MM-DD_spec-orq-[area]-[tipo].md` con estado APROBADO.

### Paso 2 — Delegación con contexto estratégico (plan)

```
TAREA PARA [AGENTE]:
Contexto estratégico: [por qué importa para Arauco]
Hipótesis a validar: [qué esperamos encontrar]
Objetivo: [qué debe producir el agente]
Insumos disponibles: datos/YYYY-MM-DD_archivo.ext
Entregable esperado: [formato + nombre de archivo]
Criterio de calidad: [campos obligatorios del Paso 3.5]
Plazo: inmediato / iteración siguiente
```

Produce: `datos/YYYY-MM-DD_plan-orq-[area]-[tipo].md`.

### Paso 3 — Integración y síntesis (review)

Al recibir ENTREGAs:
1. Verificar cada campo del checklist Paso 3.5 por agente
2. Si falta un campo: solicitar complemento al agente (no inferir)
3. Detectar inconsistencias entre agentes (cifras, supuestos, períodos)
4. Traducir técnico a lenguaje de negocio forestal
5. Estructurar síntesis con pirámide Minto: Situación → Complicación → Respuesta → Argumentos

Produce: `datos/YYYY-MM-DD_review-orq-[area]-[tipo].md` (interno).

### Paso 4 — Entrega ejecutiva (ship)

Con review APROBADA:
1. Seleccionar formato según audiencia: `.docx` gerencial, `.md` técnico, `.pptx` para comité
2. Estructura obligatoria: Contexto → Hallazgos clave → Recomendaciones → Próximos pasos → Limitaciones
3. Cada hallazgo: cifra + fuente real (nunca estimación de relleno)
4. Cada recomendación: acción + impacto + responsable (cargo) + plazo
5. Limitaciones: siempre presentes (cobertura, supuestos, precisión)

Produce: `datos/YYYY-MM-DD_[tipo]-[descripcion].[ext]`.

---

## 9. Convenciones de datos

### Nomenclatura de archivos

```
YYYY-MM-DD_tipo-descripcion.ext
```

| Tipo | Uso |
|---|---|
| `reporte` | Informes ejecutivos o gerenciales |
| `analisis` | Análisis técnicos o de datos |
| `script` | Python u otro código |
| `plantilla` | Plantillas reutilizables |
| `kpi` | Definiciones o cálculos de KPIs |
| `diagnostico` | Diagnósticos operacionales |
| `spec` | Briefs estratégicos |
| `plan` | Planes de delegación |
| `review` | Revisiones internas del Orquestador |
| `proceso-bpmn` | Diagramas BPMN (`.bpmn`, `.png`) |
| `arquitectura` | Documentos de arquitectura técnica |

### Subdirectorios de `datos/`

| Directorio | Contenido |
|---|---|
| `datos/` | Raíz — archivos finales y outputs de agentes |
| `datos/fuentes/` | Archivos de entrada sin modificar (Excel, PDF, Word originales) |
| `datos/procesos/` | BPMN, análisis de procesos |
| `datos/reportes/` | Dashboards HTML y reportes visuales |
| `datos/scripts/` | Scripts Python generados por TD o IA |

### Base de datos

`datos/arauco_mc.db` — SQLite con históricos operacionales. Accesible vía MCP `sqlite`. No leer completo: siempre con queries específicas.

---

## 10. Bot de Telegram — arquitectura

### Stack

| Componente | Tecnología |
|---|---|
| Bot | `python-telegram-bot==21.3` |
| IA | `anthropic` (`claude-sonnet-4-6`) |
| Transcripción | `groq` (whisper-large-v3) |
| Búsqueda semántica | `chromadb` + `voyageai` |
| Artefactos | `openpyxl`, `reportlab`, `python-pptx`, `pdfplumber`, `python-docx` |
| Email | `requests` → SendGrid API |
| Deploy | Railway |

### Variables de entorno

```
TELEGRAM_TOKEN          token del bot (@BotFather)
ANTHROPIC_API_KEY       clave Anthropic
GROQ_API_KEY            clave Groq (audio)
VOYAGE_API_KEY          clave VoyageAI (RAG)
SENDGRID_API_KEY        clave SendGrid (email)
SENDER_EMAIL            correo verificado en SendGrid
RAILWAY_PUBLIC_DOMAIN   dominio público (lo genera Railway)
PORT                    puerto HTTP (Railway lo asigna automáticamente)
```

### Arquitectura interna

#### Servidor HTTP para artefactos HTML

El bot levanta un servidor HTTP en hilo de fondo para servir HTML generado por Claude como URLs públicas:

```python
_HTML_STORE: OrderedDict = OrderedDict()
_MAX_STORE = 100
PUBLIC_BASE = f"https://{os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')}"

class _HTMLHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._respond(200, b"ok", "text/plain")
        elif self.path == "/arauco.css":
            self._respond(200, _ARAUCO_CSS.encode(), "text/css; charset=utf-8")
        elif self.path.startswith("/g/"):
            gid = self.path[3:]
            html = _HTML_STORE.get(gid)
            if html: self._respond(200, html.encode("utf-8"), "text/html; charset=utf-8")
            else:    self._respond(404, b"No encontrado.", "text/plain")

def store_html(html: str) -> str:
    gid = uuid.uuid4().hex
    _HTML_STORE[gid] = html
    if len(_HTML_STORE) > _MAX_STORE:
        _HTML_STORE.popitem(last=False)
    return f"{PUBLIC_BASE}/g/{gid}"

threading.Thread(target=_start_http_server, daemon=True).start()
```

#### Carga de agentes como SYSTEM_PROMPT

```python
def load_agent(path): return open(path).read() if os.path.exists(path) else ""

SYSTEM_PROMPT = f"""
## REGLA ABSOLUTA
NUNCA generes código en el chat. Deriva a los botones de artefactos.

{IDENTIDAD}
{load_agent("proyecto_claude/orquestador/CLAUDE.md")}
{load_agent("proyecto_claude/agentes/IA/CLAUDE.md")}
{load_agent("proyecto_claude/agentes/TD/CLAUDE.md")}
{load_agent("proyecto_claude/agentes/EO/CLAUDE.md")}
{REGLAS_GENERALES}
"""
```

**Nota:** DA no se carga en el SYSTEM_PROMPT del bot — su lógica es pre-procesamiento en Python antes de llamar a Claude.

#### Llamada a la API sin bloquear el event loop

```python
_tokens_map = {
    "html":         8000,
    "pdf":          6000,
    "pptx":         6000,
    "gantt":        4000,
    "excel":        3000,
    "email":        2000,
    "notas_onenote": 12000,
}

_effort_map = {
    "notas_onenote": "low",  # evita extended thinking + límite de streaming
}

async def _render_artifact(artifact_type, description, reply_fn, context):
    prompt = ARTIFACT_PROMPTS[artifact_type].replace("{CSS_URL}", f"{PUBLIC_BASE}/arauco.css")
    loop = asyncio.get_event_loop()
    raw = ""
    try:
        raw = await loop.run_in_executor(
            None,
            lambda: claude_response(
                prompt, description,
                max_tokens=_tokens_map.get(artifact_type, 4000),
                model="claude-sonnet-4-6",
                effort=_effort_map.get(artifact_type, "high")
            ),
        )
        # switch por artifact_type → build_excel / build_pdf / etc.
    except (json.JSONDecodeError, ValueError) as e:
        await reply_fn(f"Error al parsear: {e}")
    except Exception as e:
        await reply_fn(f"Error generando artefacto: {_safe_err(e)}")
    await reply_fn("¿Generar otro artefacto?", reply_markup=ARTIFACT_KEYBOARD)
```

**Por qué `run_in_executor`:** `claude_response()` es síncrona. Llamarla directamente dentro de un handler `async` bloquea el event loop de Telegram, congelando el bot. `run_in_executor` la corre en un thread pool sin bloquear.

**Por qué `effort="low"` en `notas_onenote`:** `effort="high"` + `claude-sonnet-4-6` activa extended thinking. Si la operación puede tardar >10 minutos, la API exige streaming. Como el bot no usa streaming, se produce error. `effort="low"` deshabilita extended thinking para este artefacto.

#### Procesamiento de documentos (DA en bot)

```python
SUPPORTED_DOCS = {".pdf", ".docx", ".xlsx", ".pptx"}

async def handle_document(update, context):
    ext = Path(doc.file_name).suffix.lower()
    if ext == ".xlsx":
        content, structured_data = extract_excel(file_bytes)
        # structured_data = JSON con stats completas por columna
    elif ext == ".pdf":
        content = extract_pdf(file_bytes)
    elif ext == ".docx":
        content = extract_docx(file_bytes)
    elif ext == ".pptx":
        content = extract_pptx(file_bytes)

    context.user_data["doc_content"]     = content[:10000]
    context.user_data["structured_data"] = structured_data  # solo Excel
    context.user_data["doc_tipo"]        = ext.upper()
```

El `structured_data` de Excel incluye stats sobre **todas las filas** (`sum`, `min`, `max`, `mean`, `frecuencias`) más `muestra_top20`. Claude usa `stats` para KPIs y gráficos; `muestra_top20` solo para tabla de detalle.

#### Detección de intención por mensaje

```python
_ARTIFACT_INTENT = {
    "html":  ["dashboard", "html", "interactivo"],
    "excel": ["excel", "tabla", "spreadsheet"],
    "pdf":   ["pdf", "informe", "reporte"],
    "gantt": ["gantt", "cronograma", "carta gantt"],
    "pptx":  ["ppt", "presentación", "powerpoint"],
    "email": ["correo", "email", "mail"],
}

def _detect_artifact_intent(text: str) -> str | None:
    lower = text.lower()
    for artifact_type, keywords in _ARTIFACT_INTENT.items():
        if any(kw in lower for kw in keywords):
            return artifact_type
    return None
```

#### RAG — búsqueda semántica

```python
# En rag.py: ChromaDB + embeddings VoyageAI
rag_ctx = rag.build_context(user_msg)   # busca fragmentos relevantes
system  = SYSTEM_PROMPT + rag_ctx       # agrega al system prompt de la llamada
```

#### Email via SendGrid

Flujo con confirmación de 4 pasos:
1. Claude genera JSON `{para, cc, asunto, cuerpo}`
2. Bot pregunta el destinatario
3. Bot muestra preview con teclado `[Enviar] [Editar] [Cancelar]`
4. "Editar" muestra sub-teclado `[Destinatario] [Asunto] [Cuerpo]`

---

## 11. Planner MC — arquitectura

Herramienta de gestión de proyectos Arauco. Dos versiones HTML autocontenidas servidas por el bot.

### Archivos

| Archivo | Descripción |
|---|---|
| `templates/planner_mc.html` | Versión desktop (sidebar + topbar + vistas) |
| `templates/planner_mc_mobile.html` | Versión mobile (header fijo + bottom nav) |

Ambos se sirven via `/planner` en Telegram y `GET /` en la web. Se cargan al inicio del bot y se despachan con `store_html()`.

### Áreas y subareas

```javascript
const AREAS = {
  eo: { name:'Excelencia Operacional', hex:'#059669', icon:'🏭' },
  td: { name:'Transformación Digital', hex:'#2563eb', icon:'💻' },
  ai: { name:'Inteligencia Artificial', hex:'#7c3aed', icon:'🤖' },
  id: { name:'I+D en IA',              hex:'#0891b2', icon:'🔬' },
  im: { name:'Implementación IA',      hex:'#d97706', icon:'⚙️'  },
};
```

`ai`, `id` e `im` se agregan como un bloque unificado en KPIs y resumen. En home, cada una tiene su propio botón de carga Excel.

### Fuente de datos

Solo Excel de Microsoft Planner (exportado como `.xlsx`). La librería XLSX.js parsea el archivo client-side. No hay backend involucrado — todo es JavaScript puro. Los datos viven en memoria mientras la pestaña está abierta.

### Vistas (desktop)

| Vista | ID | Descripción |
|---|---|---|
| Ejecutiva | `view-exec` | KPIs globales + cards por área + resumen semanal |
| Plan/Board | `view-plan` + `pview-board` | Tablero Kanban por bucket |
| Plan/Grid | `view-plan` + `pview-grid` | Tabla ordenable con todos los campos |
| Plan/Timeline | `view-plan` + `pview-gantt` | Gantt con toggle Semanas/Meses + filtro por área |

### Vistas (mobile)

| Vista | ID | Descripción |
|---|---|---|
| Inicio | `view-exec` | KPIs + cards por área |
| Tablero | `view-plan` > `plan-board-content` | Grupos por bucket colapsables |
| Timeline | `view-plan` > `plan-gantt-content` | Gantt mobile con toggle Semanas/Meses |
| Alertas | `view-alerts` | Vencidas + tareas de la semana |

### Gantt / Timeline

Implementado en ambas versiones. Características:

- **Toggle escala**: Semanas (columnas de 7 días) o Meses
- **Fecha inicio**: campo `Inicio`/`Start Date` del Excel; si falta → fecha_fin - 14 días
- **Hoy**: columna con fondo rojo semitransparente + borde rojo
- **Barras**: color del área, opacidad reducida si `done`, borde rojo si `late`
- **Desktop**: filtro por área (Todas / EO / TD / IA / I+D / Impl.) en topbar del Gantt
- **Desktop**: en vista "Todas las áreas", filas agrupadas con encabezado por área
- **Mobile**: Gantt filtra automáticamente por `curArea` (subagente activo en bottom nav)

```javascript
// Derivar fecha inicio si no existe en el Excel
let start = pDate(r['Inicio'] || r['Start Date'] || r['Fecha inicio'] || null);
if(!start){ start = new Date(end); start.setDate(start.getDate() - 14); }
```

### Resumen semanal

Modal "OneNote" con tareas marcadas `Week` o con campo `Abordaría esta Semana? = Sí`.

- **Títulos de área**: `font-size:15px; font-weight:700` — subtítulos visibles, sin uppercase
- **Secciones**: agrupadas por área con borde izquierdo de color
- **Copiar texto**: genera markdown para pegar en Telegram/WhatsApp con `*negrita*` por sección
- Excluye: `Finalizado`, `Stand By (Congelado)`, tareas al 100%

### Carga de Excel en home — card IA

La card IA en home tiene 3 botones de carga independientes:

| Botón | `openModalFor()` | Qué carga |
|---|---|---|
| IA General | `'ai'` | Planner principal de IA |
| I+D en IA | `'id'` | Planner de investigación |
| Implementación IA | `'im'` | Planner de implementación |

`updateAreaCards()` actualiza el estado de los 3 botones cada vez que se carga cualquier Excel.

### Agregar nuevo artefacto al bot desde planner

```python
# bot.py — endpoint existente
@_web_app.post("/api/artifact")
async def web_api_artifact(request: Request):
    art_type = body.get("type", "")
    if art_type == "planner":
        url = store_html(_PLANNER_HTML)
        return {"result_type": "url", "url": url}
    if art_type == "planner_mobile":
        url = store_html(_PLANNER_MOBILE_HTML)
        return {"result_type": "url", "url": url}
```

---

## 12. Web UI — arquitectura

Interfaz web en `templates/web_chat.html`. Se sirve en `GET /` del servidor FastAPI.

### Stack frontend

- HTML/CSS/JS vanilla (sin frameworks)
- Streaming SSE desde `/api/chat`
- Fuente Lato (Google Fonts)
- Sin bundler — un solo archivo HTML

### Endpoints del backend (FastAPI)

| Endpoint | Método | Descripción |
|---|---|---|
| `/` | GET | Sirve `web_chat.html` |
| `/api/chat` | POST | Chat general con streaming SSE. Inyecta RAG automáticamente si hay docs. |
| `/api/rag/chat` | POST | Chat RAG especializado — responde SOLO desde documentos indexados. Sistema RAG sin restricciones del SYSTEM_PROMPT general. |
| `/api/rag/docs` | GET | Lista documentos indexados en ChromaDB |
| `/api/rag/query` | POST | Búsqueda semántica directa (retorna chunks, no respuesta Claude) |
| `/api/rag/index` | POST | Indexa un archivo (PDF, DOCX, XLSX, PPTX, TXT) en ChromaDB |
| `/api/artifact` | POST | Genera artefacto (html, excel, pdf, pptx, gantt, email, planner) |
| `/api/upload` | POST | Sube archivo adjunto para adjuntar al mensaje de chat |
| `/api/history` | GET | Historial de conversaciones del día |
| `/api/send-email` | POST | Envía correo via SendGrid |
| `/g/{gid}` | GET | Sirve HTML generado (artefactos, planner) |

### Diferencia `/api/chat` vs `/api/rag/chat`

| | `/api/chat` | `/api/rag/chat` |
|---|---|---|
| Sistema | `SYSTEM_PROMPT` general (prohíbe generar contenido directo) | Sistema RAG especializado (genera respuestas completas desde docs) |
| RAG | Inyecta contexto automáticamente pero Claude no genera | Responde ÚNICAMENTE desde documentos indexados |
| Streaming | Sí (SSE) | No (respuesta JSON) |
| Equivalente Telegram | Conversación normal | `_handle_nlm_query` + `nlm_mode` |

### Modo RAG en web (paridad con Telegram)

Tres formas de activar el modo RAG:

1. **Sidebar "Base RAG"** → abre panel + activa modo automáticamente
2. **Panel RAG → "🤖 Preguntar con IA"** → consulta directa en el panel lateral
3. **Banner "Modo RAG"** → toggle manual, los mensajes del chat van a `/api/rag/chat`

```javascript
// Intercept en send() cuando ragMode=true
if(ragMode){
  const resp = await fetch('/api/rag/chat', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({question: text, history: history.slice(-6), model})
  });
  const data = await resp.json();
  appendAI(data.answer);
}
```

### RAG — flujo de indexado

1. Usuario sube archivo con botón 📚 (input bar) o "📥 Indexar documento" (panel RAG)
2. `POST /api/rag/index` → extrae texto según extensión → `rag.index_document()`
3. `index_document()` chunkea a 400 palabras con overlap 60, embede con VoyageAI en lotes de 8, persiste en ChromaDB (`/data/chroma`)
4. Cada mensaje de chat llama `rag.build_context(message)` → top-4 chunks por similitud coseno → inyectado en system prompt

```python
# rag.py — parámetros clave
CHROMA_PATH  = "/data/chroma"        # persiste en Railway /data
EMBED_MODEL  = "voyage-3"
TOP_K        = 4
MAX_DISTANCE = 0.55                  # umbral similitud coseno
BATCH        = 8                     # chunks por llamada VoyageAI
```

**Nota:** ChromaDB persiste en `/data/chroma` en Railway. Los documentos indexados desde Telegram son accesibles desde la web y viceversa — comparten la misma colección.

---

## 13. Checklist para nuevo proyecto

### Sistema de agentes (Claude Code)

- [ ] Crear repositorio con estructura de carpetas del Punto 2
- [ ] Escribir `CLAUDE.md` del proyecto con contexto corporativo, glosario y sistemas del cliente
- [ ] Crear `orquestador/CLAUDE.md` adaptando identidad y dominio al cliente
- [ ] Crear `agentes/{EO,TD,IA,DA}/CLAUDE.md` adaptando expertise al cliente
- [ ] Copiar skills globales (`branding-[cliente]`, `office-files`)
- [ ] Adaptar `branding-[cliente]/SKILL.md` con colores, tipografía y logo del cliente
- [ ] Crear `agentes/{EO,TD,IA,DA}/skills/{spec,plan,build,test,review,ship}/SKILL.md`
- [ ] Crear `orquestador/skills/{spec,plan,review,ship}/SKILL.md`
- [ ] Configurar `.claude/settings.json` con MCP servers relevantes
- [ ] Crear `datos/` con subdirectorios y `README.md`
- [ ] Crear `tasks/lessons.md` vacío
- [ ] Inicializar SQLite si hay base de datos histórica

### Bot de Telegram

- [ ] Crear bot en @BotFather → obtener `TELEGRAM_TOKEN`
- [ ] Obtener `ANTHROPIC_API_KEY`
- [ ] Obtener `GROQ_API_KEY` (audio — opcional)
- [ ] Obtener `VOYAGE_API_KEY` (RAG — opcional)
- [ ] Crear cuenta SendGrid → verificar sender → `SENDGRID_API_KEY` + `SENDER_EMAIL`
- [ ] Crear proyecto en Railway → conectar repo GitHub
- [ ] Agregar todas las variables de entorno en Railway
- [ ] Generar dominio público en Railway → copiar a `RAILWAY_PUBLIC_DOMAIN`
- [ ] Adaptar `IDENTIDAD` y `REGLAS_GENERALES` en `bot.py`
- [ ] Adaptar colores de marca en `_ARAUCO_CSS` y funciones `build_pdf` / `build_pptx`
- [ ] Adaptar logo en los prompts HTML
- [ ] Ajustar `ARTIFACT_PROMPTS` al dominio del cliente
- [ ] Revisar `_tokens_map` y `_effort_map` según complejidad esperada de cada artefacto

---

## 12. Adaptaciones por cliente

### Qué cambiar por cliente

| Componente | Qué adaptar |
|---|---|
| `CLAUDE.md` del proyecto | Empresa, glosario operacional, sistemas corporativos, restricciones de lenguaje |
| `orquestador/CLAUDE.md` | Cargo, años de experiencia, dominio de industria, glosario corporativo |
| `agentes/*/CLAUDE.md` | Expertise específico, sistemas del cliente (en lugar de Planex/SGL/SAP), dominio de conocimiento |
| `skills/branding-*/SKILL.md` | Colores HEX, tipografía, URLs del logo |
| `ARTIFACT_PROMPTS` en bot.py | Contexto de negocio en cada prompt |
| `_ARAUCO_CSS` en bot.py | Variables CSS con colores del cliente |
| `IDENTIDAD` en bot.py | Nombre de la empresa, área y rol |

### Qué NO cambiar

- Estructura del protocolo de orquestación (spec → plan → review → ship)
- Checklist Paso 3.5 y campos obligatorios por agente
- Patrón `run_in_executor` para llamadas Claude en handlers async
- Formato de ENTREGA por agente
- Jerarquía de CLAUDE.md
- Convención `YYYY-MM-DD_tipo-descripcion.ext` para archivos

### Escalar el sistema

**Agregar un nuevo agente:**
1. Crear `agentes/NUEVO/CLAUDE.md` con identidad, dominio, skills, tools, MCP, protocolo de entrega y paralelismo
2. Crear `agentes/NUEVO/skills/{spec,plan,build,test,review,ship}/SKILL.md`
3. Agregar el agente a la tabla de sub-agentes en `orquestador/CLAUDE.md`
4. Definir cuándo el Orquestador lo activa y sus dependencias con otros agentes
5. Si se usa en el bot: agregar `load_agent("proyecto_claude/agentes/NUEVO/CLAUDE.md")` al SYSTEM_PROMPT

**Agregar un nuevo artefacto al bot:**
1. Agregar `"tipo": ["keyword1", "keyword2"]` en `_ARTIFACT_INTENT`
2. Agregar `"tipo": N` en `_tokens_map`
3. Agregar entrada en `ARTIFACT_PROMPTS` con el prompt específico
4. Agregar case en el switch de `_render_artifact` con la función `build_tipo()`
5. Agregar botón en `ARTIFACT_KEYBOARD`
6. Si puede activar extended thinking: agregar `"tipo": "low"` en `_effort_map`
