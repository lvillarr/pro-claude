# Skill: office-files — Lectura y Edición de Archivos de Oficina

## Propósito

Leer, extraer contenido y editar archivos en formatos `.docx`, `.xlsx`, `.pptx` y `.pdf` usados en operaciones forestales: informes de Planex, plantillas SAP, reportes de KPI en Excel, procedimientos operacionales en Word, presentaciones Kaizen y PDFs regulatorios. Permite al agente EO consumir y producir documentos en los formatos reales del negocio.

---

## Capacidades por formato

| Formato | Leer | Editar | Crear | MCP / Librería |
|---|---|---|---|---|
| `.xlsx` | ✅ | ✅ | ✅ | `excel-mcp` + `openpyxl` |
| `.docx` | ✅ | ✅ | ✅ | `markitdown-mcp` + `python-docx` |
| `.pptx` | ✅ | ✅ | ✅ | `markitdown-mcp` + `python-pptx` |
| `.pdf`  | ✅ | ❌ | ❌ | `markitdown-mcp` + `pdfplumber` |

> Los PDF son de solo lectura. Para modificar un PDF, exportar el contenido, editar en el formato origen y regenerar.

---

## Cuándo usar este skill

- Se recibe un `.xlsx` con datos de SGL, SAP o Planex para analizar KPIs
- Se solicita editar o completar una plantilla de procedimiento en `.docx`
- Se debe generar o actualizar una presentación `.pptx` de Kaizen o cierre de proyecto
- Se recibe un informe en `.pdf` de proveedor, contratista o regulador para extraer datos
- Se necesita exportar un entregable EO al formato de oficina correspondiente

---

## Protocolo de ejecución

---

### XLSX — Leer y editar hojas de cálculo

#### Leer con `excel-mcp`
El MCP `excel-mcp` expone herramientas nativas para leer hojas y rangos:
```
Tool: excel_read_sheet
Parámetros:
  file: datos/2024-01-15_kpi-oee-linea3.xlsx
  sheet: "KPIs Semana"
  range: "A1:H50"   ← opcional, omitir para leer toda la hoja
```

#### Leer y editar con Python (openpyxl)
```python
import openpyxl

# LEER
wb = openpyxl.load_workbook("datos/2024-01-15_kpi-oee-linea3.xlsx")
ws = wb["KPIs Semana"]
for row in ws.iter_rows(min_row=2, values_only=True):
    print(row)

# EDITAR CELDA
ws["B5"] = 87.3        # escribir valor
ws["C5"] = "=B5/B4"   # escribir fórmula

# GUARDAR
wb.save("datos/2024-01-15_kpi-oee-linea3-actualizado.xlsx")
```

#### Crear plantilla nueva con pandas + openpyxl
```python
import pandas as pd

df = pd.DataFrame({
    "KPI":        ["OEE", "Disponibilidad", "Rendimiento", "Calidad"],
    "Fórmula":    ["D×R×C", "TU/TP", "PR/PN", "PB/PP"],
    "Línea base": [None, None, None, None],
    "Meta":       [85, 92, 95, 98],
    "Unidad":     ["%", "%", "%", "%"]
})
df.to_excel("datos/plantillas/STD-KPI-OEE-v1.0.xlsx", index=False, sheet_name="KPIs")
```

#### Casos de uso forestales comunes
- Leer exportación de pérdidas del SGL en `.xlsx`
- Completar plantilla de OEE por equipo y turno
- Agregar columna de análisis a reporte de Planex
- Generar diccionario de KPIs en formato tabla Excel

---

### DOCX — Leer y editar documentos Word

#### Leer con markitdown-mcp
El MCP `markitdown` convierte el `.docx` a Markdown para lectura:
```
Tool: markitdown_convert
Parámetros:
  file_path: datos/procedimiento-cosecha-v2.docx
```
Retorna el contenido completo como texto Markdown, incluyendo tablas, listas y encabezados.

#### Leer con Python (python-docx)
```python
from docx import Document

doc = Document("datos/procedimiento-cosecha-v2.docx")

# Leer párrafos
for para in doc.paragraphs:
    print(para.style.name, ":", para.text)

# Leer tablas
for table in doc.tables:
    for row in table.rows:
        print([cell.text for cell in row.cells])
```

#### Editar documento existente
```python
from docx import Document

doc = Document("datos/plantillas/STD-POE-cosecha-v1.0.docx")

# Modificar texto en párrafos
for para in doc.paragraphs:
    if "VERSIÓN" in para.text:
        para.runs[0].text = para.runs[0].text.replace("v1.0", "v1.1")

# Agregar párrafo al final
doc.add_paragraph("Nota: procedimiento actualizado post-Kaizen 2024-01.")

# Agregar tabla
tabla = doc.add_table(rows=1, cols=3)
tabla.style = "Table Grid"
hdr = tabla.rows[0].cells
hdr[0].text = "Actividad"
hdr[1].text = "Responsable"
hdr[2].text = "Plazo"

doc.save("datos/plantillas/STD-POE-cosecha-v1.1.docx")
```

#### Crear documento nuevo
```python
from docx import Document
from docx.shared import Pt, RGBColor

doc = Document()
doc.add_heading("Procedimiento Operacional Estándar", 0)
doc.add_heading("1. Objetivo", level=1)
doc.add_paragraph("Estandarizar el proceso de [nombre] en faena [nombre].")
doc.add_heading("2. Alcance", level=1)
doc.add_paragraph("Aplica a todos los turnos de [área].")
doc.save("datos/plantillas/STD-POE-nuevo-v1.0.docx")
```

#### Casos de uso forestales comunes
- Leer procedimientos operacionales para extraer actividades a modelar en BPMN
- Editar plantillas de charter de proyecto con datos de la especificación
- Crear documentos A3 o informes de cierre en formato Word corporativo
- Actualizar versión de un POE tras un evento Kaizen

---

### PPTX — Leer y editar presentaciones PowerPoint

#### Leer con markitdown-mcp
```
Tool: markitdown_convert
Parámetros:
  file_path: datos/presentacion-kaizen-cosecha.pptx
```
Retorna el texto de todas las diapositivas en Markdown.

#### Leer con Python (python-pptx)
```python
from pptx import Presentation

prs = Presentation("datos/presentacion-kaizen-cosecha.pptx")
for i, slide in enumerate(prs.slides):
    print(f"\n--- Diapositiva {i+1} ---")
    for shape in slide.shapes:
        if shape.has_text_frame:
            print(shape.text_frame.text)
```

#### Editar diapositiva existente
```python
from pptx import Presentation
from pptx.util import Pt

prs = Presentation("datos/presentacion-kaizen-cosecha.pptx")

# Editar texto en diapositiva 0 (portada)
slide = prs.slides[0]
for shape in slide.shapes:
    if shape.has_text_frame:
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                if "FECHA" in run.text:
                    run.text = run.text.replace("FECHA", "2024-06-15")

prs.save("datos/presentacion-kaizen-cosecha-v2.pptx")
```

#### Agregar diapositiva nueva
```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation("datos/presentacion-kaizen-cosecha.pptx")

# Usar layout de diapositiva de contenido (índice 1 en la mayoría de plantillas)
slide_layout = prs.slide_layouts[1]
slide = prs.slides.add_slide(slide_layout)

# Título y contenido
slide.shapes.title.text = "Resultados KPI — OEE Línea 3"
tf = slide.placeholders[1].text_frame
tf.text = "OEE: 84.2% → Meta: 85%"
tf.add_paragraph().text = "Disponibilidad: 92.1%"
tf.add_paragraph().text = "Rendimiento: 95.4%"

prs.save("datos/presentacion-kaizen-cosecha-v2.pptx")
```

#### Casos de uso forestales comunes
- Crear presentación de resultados Kaizen para gerencia
- Actualizar diapositivas de KPIs semanales con datos frescos del SGL
- Leer presentación de briefing de contratista para extraer compromisos
- Generar deck de cierre de proyecto con datos de la iniciativa de mejora

---

### PDF — Leer y extraer contenido

> Los PDF **no se editan**. Flujo correcto: extraer → procesar → generar nuevo archivo en formato editable.

#### Leer con markitdown-mcp (recomendado)
```
Tool: markitdown_convert
Parámetros:
  file_path: datos/informe-sag-2024.pdf
```

#### Leer con Python (pdfplumber) — para tablas complejas
```python
import pdfplumber

with pdfplumber.open("datos/informe-sag-2024.pdf") as pdf:
    # Texto de todas las páginas
    for page in pdf.pages:
        print(page.extract_text())

    # Extraer tablas (si las hay)
    page = pdf.pages[2]
    tables = page.extract_tables()
    for table in tables:
        for row in table:
            print(row)
```

#### Leer con Python (pypdf) — para PDFs simples o encriptados
```python
import pypdf

reader = pypdf.PdfReader("datos/certificado-proveedor.pdf")
for page in reader.pages:
    print(page.extract_text())
```

#### Flujo: PDF → Excel (extracción de tabla)
```python
import pdfplumber
import pandas as pd

with pdfplumber.open("datos/reporte-sap-exportado.pdf") as pdf:
    tabla = pdf.pages[1].extract_table()

df = pd.DataFrame(tabla[1:], columns=tabla[0])
df.to_excel("datos/2024-01-15_tabla-extraida-sap.xlsx", index=False)
```

#### Casos de uso forestales comunes
- Extraer datos de certificados de proveedor o contratista
- Leer informes regulatorios de CONAF, SAG o SEREMI para extraer compromisos
- Procesar reportes SAP exportados como PDF para alimentar análisis de KPIs
- Extraer tablas de informes técnicos para cruzar con datos del SGL

---

## Dependencias Python requeridas

Instalar antes de usar las capacidades de edición:

```bash
pip install openpyxl pandas python-docx python-pptx pdfplumber pypdf
```

---

## Convención de archivos procesados

| Acción | Patrón de nombre |
|---|---|
| Archivo leído y analizado | `datos/YYYY-MM-DD_analisis-[nombre-archivo].[ext]` |
| Archivo editado | `datos/[nombre-original]-actualizado.[ext]` |
| Estándar generado | `datos/plantillas/STD-[codigo]-[nombre]-v[N.n].[ext]` |
| Extracción de PDF | `datos/YYYY-MM-DD_[nombre]-extraido.xlsx` |

---

## Restricciones de este skill

- Nunca sobreescribir el archivo original: siempre guardar como nueva versión o en `datos/plantillas/`
- Los PDF son solo lectura: extraer contenido, no intentar modificar el archivo
- Al editar un `.docx` o `.pptx`, verificar el layout y estilos del archivo original antes de agregar contenido nuevo para mantener consistencia visual
- Los `.xlsx` con macros VBA no son compatibles con openpyxl: usar la extensión `.xlsm` y advertir al usuario
- Siempre confirmar la ruta del archivo con `read_file` o `list_directory` antes de intentar abrirlo
