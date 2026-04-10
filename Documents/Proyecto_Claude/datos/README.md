# datos/ — Archivos compartidos del sistema multiagente

Este directorio es el espacio de trabajo común para todos los agentes (IA, TD, EO)
y el orquestador. Todos los agentes tienen permisos de lectura y escritura.

---

## Convención de nombrado

```
YYYY-MM-DD_tipo-descripcion.ext
```

### Tipos reconocidos

| Tipo | Descripción | Extensiones típicas |
|---|---|---|
| `reporte` | Informe ejecutivo consolidado | `.html`, `.docx`, `.pdf` |
| `analisis` | Output del agente IA | `.html`, `.csv`, `.json` |
| `script` | Código reutilizable (IA o TD) | `.py`, `.sh` |
| `plantilla` | Base para documentos EO | `.xlsx`, `.docx` |
| `kpi` | Tabla de indicadores | `.xlsx`, `.csv` |
| `diagnostico` | Ficha técnica de equipo o proceso | `.md`, `.html` |
| `config` | Configuraciones técnicas (TD) | `.json`, `.yaml` |

---

## Subdirectorios

| Directorio | Contenido |
|---|---|
| `scripts/` | Scripts `.py` y `.sh` reutilizables generados por IA y TD |
| `plantillas/` | Archivos base `.xlsx` y `.docx` para EO |

---

## Base de datos

**`arauco_mc.db`** — SQLite local para históricos operacionales.

Tablas previstas:
- `equipos` — catálogo de equipos y líneas
- `kpis` — histórico de indicadores por período
- `perdidas` — registro de pérdidas operacionales
- `acciones` — plan de acciones y seguimiento

---

## Notas

- No guardar credenciales, tokens ni datos personales en este directorio
- Los archivos temporales o de trabajo deben eliminarse al finalizar cada tarea
- Mantener el historial de reportes; no sobreescribir — usar fecha en el nombre
