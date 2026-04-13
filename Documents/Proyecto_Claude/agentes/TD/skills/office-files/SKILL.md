# Skill: office-files — Lectura y Edición de Archivos de Oficina (TD)

## Propósito

Leer, extraer contenido y editar archivos `.xlsx`, `.docx`, `.pptx` y `.pdf` relevantes para iniciativas de transformación digital forestal. Permite al agente TD consumir especificaciones de sistemas, exportaciones de configuración, contratos de proveedores y documentos de arquitectura, y producir entregables técnicos en formatos de oficina.

> Para el protocolo completo de edición (Python, MCP tools, plantillas), referirse al skill `office-files` del agente EO. Este skill documenta los **casos de uso específicos del área TD**.

---

## Capacidades

| Formato | Leer | Editar | Crear | Herramienta |
|---|---|---|---|---|
| `.xlsx` | ✅ | ✅ | ✅ | `excel-mcp` + `openpyxl` / `pandas` |
| `.docx` | ✅ | ✅ | ✅ | `markitdown` + `python-docx` |
| `.pptx` | ✅ | ✅ | ✅ | `markitdown` + `python-pptx` |
| `.pdf`  | ✅ | — | — | `markitdown` + `pdfplumber` |

---

## Casos de uso TD — por formato

### XLSX — Configuraciones, esquemas y datos técnicos
```python
import pandas as pd

# Leer inventario de sistemas y APIs disponibles
df_sistemas = pd.read_excel("datos/inventario-sistemas-arauco.xlsx",
                             sheet_name="APIs disponibles")

# Leer mapeo de campos entre sistemas (crosswalk)
df_mapeo = pd.read_excel("datos/mapeo-campos-sgl-sap.xlsx")
print(df_mapeo[["campo_fuente", "campo_destino", "transformacion"]])

# Exportar reporte de estado de pipelines
estado = pd.DataFrame({
    "Pipeline": ["ETL SGL→SQLite", "Telemetría Tigercat", "Sync Forest Data"],
    "Estado":   ["Operacional", "En desarrollo", "Planificado"],
    "Completitud (%)": [100, 65, 0],
    "Responsable": ["TD", "TD", "TD"]
})
estado.to_excel("datos/YYYY-MM-DD_estado-pipelines.xlsx", index=False)
```

**Uso típico en TD:**
- Leer inventario de sistemas corporativos con estado de APIs
- Editar mapeo de campos entre sistemas (crosswalk tables)
- Generar reporte de estado de integraciones para el orquestador
- Leer configuraciones de dealers o proveedores en formato tabla

### DOCX — Especificaciones técnicas y arquitecturas
```python
from docx import Document

# Leer especificación de API de sistema forestal
doc = Document("datos/spec-api-forest-data-2.0.docx")
for table in doc.tables:
    print("=== Tabla ===")
    for row in table.rows:
        print([cell.text for cell in row.cells])

# Generar documento de arquitectura de integración
doc = Document()
doc.add_heading("Arquitectura de Integración — [Nombre Iniciativa]", 0)
doc.add_heading("1. Visión general", level=1)
doc.add_paragraph("Esta integración conecta [Sistema A] con [Sistema B] mediante ...")
doc.add_heading("2. Diagrama de flujo", level=1)
doc.add_paragraph("[Ver diagrama adjunto o descripción textual del flujo]")
doc.save("datos/YYYY-MM-DD_arquitectura-[nombre].docx")
```

**Uso típico en TD:**
- Leer documentación técnica de APIs de sistemas forestales (Planex, Forest Data, SGL)
- Leer contratos técnicos de dealers de maquinaria para entender las APIs
- Generar documentos de arquitectura de integración para revisión con TI
- Crear procedimientos de operación de pipelines para el equipo de TI

### PPTX — Presentaciones técnicas y de avance
```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()

# Diapositiva de arquitectura
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Arquitectura de Integración — Telemetría Forestal"
tf = slide.placeholders[1].text_frame
tf.text = "Fuente: APIs Tigercat + John Deere"
tf.add_paragraph().text = "Transformación: Python ETL normalizado"
tf.add_paragraph().text = "Destino: Forest Data 2.0 + Datalake"
tf.add_paragraph().text = "Frecuencia: polling cada 5 minutos"

prs.save("datos/YYYY-MM-DD_presentacion-arquitectura-telemetria.pptx")
```

**Uso típico en TD:**
- Presentar arquitectura de integración a TI o gerencia técnica
- Generar deck de avance de iniciativas digitales para el orquestador
- Actualizar presentación de roadmap digital con estado actual de proyectos
- Crear material técnico para capacitación de operadores en nuevos sistemas

### PDF — Extracción de especificaciones técnicas
```python
import pdfplumber

# Extraer endpoints y parámetros de API de manual de dealer
with pdfplumber.open("datos/manual-api-tigercat-2024.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        texto = page.extract_text()
        if texto and "endpoint" in texto.lower():
            print(f"--- Página {i+1} ---")
            print(texto)

# Usar markitdown-mcp para conversión rápida
# Tool: markitdown_convert → file_path: datos/manual-api-tigercat-2024.pdf
```

**Uso típico en TD:**
- Leer manuales técnicos de APIs de dealers de maquinaria forestal
- Extraer especificaciones de integración de documentos de TI corporativa
- Procesar contratos de proveedores para extraer compromisos de niveles de servicio
- Leer documentación de sistemas (SAP, SGL, Historian) en formato PDF

---

## Convención de archivos

| Acción | Patrón |
|---|---|
| Especificación técnica leída | `datos/YYYY-MM-DD_spec-[sistema]-extraida.md` |
| Arquitectura generada | `datos/YYYY-MM-DD_arquitectura-[nombre].docx` |
| Reporte de estado pipelines | `datos/YYYY-MM-DD_estado-pipelines.xlsx` |
| Presentación técnica | `datos/YYYY-MM-DD_presentacion-[nombre].pptx` |

---

## Dependencias Python

```bash
pip install openpyxl pandas python-docx python-pptx pdfplumber pypdf
```

---

## Restricciones

- Nunca guardar credenciales en archivos Excel o Word aunque sea "temporal"
- Los PDF de manuales técnicos son solo lectura: extraer → documentar en Markdown → referencia para el código
- Al crear documentos de arquitectura en DOCX, incluir siempre: fecha, versión, responsable y estado (borrador / revisado / aprobado)
