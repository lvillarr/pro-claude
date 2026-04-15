# Skill: office-files — Lectura y Edición de Archivos de Oficina (IA)

## Propósito

Leer, extraer contenido y editar archivos `.xlsx`, `.docx`, `.pptx` y `.pdf` relevantes para proyectos de inteligencia artificial forestal. Permite al agente IA consumir especificaciones técnicas, exportaciones de datos, reportes de benchmark y producir entregables en formatos de oficina para audiencias no técnicas.

> Para el protocolo completo de edición (Python, MCP tools, plantillas), referirse al skill `office-files` del agente EO. Este skill documenta los **casos de uso específicos del área IA**.

---

## Capacidades

| Formato | Leer | Editar | Crear | Herramienta |
|---|---|---|---|---|
| `.xlsx` | ✅ | ✅ | ✅ | `excel-mcp` + `openpyxl` / `pandas` |
| `.docx` | ✅ | ✅ | ✅ | `markitdown` + `python-docx` |
| `.pptx` | ✅ | ✅ | ✅ | `markitdown` + `python-pptx` |
| `.pdf`  | ✅ | — | — | `markitdown` + `pdfplumber` |

---

## Casos de uso IA — por formato

### XLSX — Datos operacionales para modelos
```python
import pandas as pd

# Leer exportación de SGL o SAP para entrenamiento de modelo
df = pd.read_excel("datos/exportacion-sgl-2024.xlsx", sheet_name="Pérdidas")

# Exportar resultados de modelo a Excel para validación con EO
resultados = pd.DataFrame({
    "equipo": equipos,
    "productividad_real": y_real,
    "productividad_predicha": y_pred,
    "error_abs": abs(y_real - y_pred)
})
resultados.to_excel("datos/YYYY-MM-DD_validacion-modelo-productividad.xlsx", index=False)
```

**Uso típico en IA:**
- Leer datos históricos de operaciones para training/testing de modelos
- Exportar tabla de métricas de evaluación para revisión con EO
- Leer parámetros de configuración de experimentos en Excel
- Generar reporte de importancia de features en formato tabla

### DOCX — Especificaciones técnicas y reportes
```python
from docx import Document

# Leer especificación de requerimientos de un sistema para construir integración
doc = Document("datos/especificacion-api-forest-data.docx")
for para in doc.paragraphs:
    if para.style.name.startswith("Heading"):
        print(para.text)

# Generar informe técnico de modelo para revisión
doc = Document()
doc.add_heading("Reporte Técnico — Modelo Predictivo de Productividad", 0)
doc.add_heading("1. Resumen ejecutivo", level=1)
doc.add_paragraph(f"El modelo alcanzó un RMSE de {rmse:.2f} horas, mejorando en un {mejora:.1f}% respecto al baseline.")
doc.save("datos/YYYY-MM-DD_reporte-tecnico-modelo.docx")
```

**Uso típico en IA:**
- Leer specs técnicas de sistemas para entender datos disponibles
- Generar documentación técnica de modelos para el área TD
- Crear resúmenes ejecutivos de análisis para el orquestador
- Leer papers o reportes de benchmark en formato Word

### PPTX — Presentaciones de resultados IA
```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()

# Diapositiva de resultados del modelo
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Resultados — Modelo de Productividad de Cosecha"
tf = slide.placeholders[1].text_frame
tf.text = f"RMSE: {rmse:.2f} horas ({mejora:.1f}% sobre baseline)"
tf.add_paragraph().text = f"Equipo con mayor error: {equipo_max_error}"
tf.add_paragraph().text = "Recomendación: priorizar datos de turno noche"

# Insertar imagen de feature importance
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
slide2.shapes.add_picture("datos/[proyecto]/outputs/feature_importance.png",
                          Inches(1), Inches(1), Inches(8), Inches(5))

prs.save("datos/YYYY-MM-DD_presentacion-modelo-productividad.pptx")
```

**Uso típico en IA:**
- Presentar resultados de modelo ML a gerencia u operaciones
- Generar deck de cierre de proyecto IA con métricas y recomendaciones
- Actualizar presentación de avance del proyecto con gráficos generados en Python
- Crear material de capacitación para usuarios del dashboard o modelo

### PDF — Extracción de datos técnicos
```python
import pdfplumber

# Extraer tabla de benchmark de productividad de informe PDF
with pdfplumber.open("datos/informe-benchmark-cosecha-2023.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            print(df)

# Extraer texto de paper técnico o informe regulatorio
with pdfplumber.open("datos/paper-productividad-terreno.pdf") as pdf:
    texto = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    
# Usar markitdown-mcp para conversión rápida a Markdown
# Tool: markitdown_convert → file_path: datos/paper-productividad-terreno.pdf
```

**Uso típico en IA:**
- Leer papers técnicos o informes de benchmark para contexto del modelo
- Extraer tablas de reportes SAP exportados como PDF
- Procesar informes de certificación de equipos o proveedores
- Leer fichas técnicas de maquinaria para features de modelos de falla

---

## Convención de archivos

| Acción | Patrón |
|---|---|
| Datos para modelo extraídos de Excel | `datos/[proyecto]/raw/YYYY-MM-DD_[nombre].csv` |
| Reporte técnico de modelo | `datos/YYYY-MM-DD_reporte-tecnico-[nombre].docx` |
| Presentación de resultados | `datos/YYYY-MM-DD_presentacion-[nombre].pptx` |
| Tabla extraída de PDF | `datos/YYYY-MM-DD_[nombre]-extraido.xlsx` |

---

## Dependencias Python

```bash
pip install openpyxl pandas python-docx python-pptx pdfplumber pypdf
```

---

## Restricciones

- Nunca sobreescribir el archivo de datos original: guardar en `raw/` sin modificar
- Los modelos no se guardan en Excel: usar `.pkl` o `.joblib` para modelos, Excel para resultados tabulares
- Los PDF son solo lectura: extraer → procesar → generar entregable en otro formato
