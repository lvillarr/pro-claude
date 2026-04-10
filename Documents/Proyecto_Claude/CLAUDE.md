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
