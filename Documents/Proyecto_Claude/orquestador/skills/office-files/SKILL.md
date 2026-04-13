# Skill: office-files — Lectura y Generación de Documentos Ejecutivos (Orquestador)

## Propósito

Leer archivos de entrada del usuario (informes, datos, presentaciones) y generar entregables ejecutivos consolidados en formatos de oficina. El orquestador usa este skill para consumir inputs y producir el output final que se presenta a gerencia.

> Para el protocolo completo de edición técnica (Python, MCP tools), referirse al skill `office-files` del agente EO. Este skill documenta los **casos de uso específicos del orquestador**.

---

## Capacidades

| Formato | Leer | Editar | Crear | Herramienta |
|---|---|---|---|---|
| `.xlsx` | ✅ | ✅ | ✅ | `excel-mcp` + `openpyxl` |
| `.docx` | ✅ | ✅ | ✅ | `markitdown` + `python-docx` |
| `.pptx` | ✅ | ✅ | ✅ | `markitdown` + `python-pptx` |
| `.pdf`  | ✅ | — | — | `markitdown` + `pdfplumber` |

---

## Casos de uso del orquestador — por formato

### XLSX — Leer datos y generar tablas de consolidación
```python
import pandas as pd

# Leer outputs de agentes en Excel
df_eo = pd.read_excel("datos/YYYY-MM-DD_kpi-oee-linea3.xlsx")
df_ia = pd.read_excel("datos/YYYY-MM-DD_validacion-modelo.xlsx")

# Tabla de consolidación ejecutiva para el informe
consolidado = pd.DataFrame({
    "Iniciativa": ["Reducción pérdidas Línea 3", "Modelo predictivo OEE"],
    "Área": ["EO", "IA"],
    "KPI principal": ["OEE: 78% → 85%", "RMSE: 2.3 horas"],
    "Impacto CLP/año": ["$120M", "Por estimar"],
    "Estado": ["Piloto completado", "En validación"]
})
consolidado.to_excel("datos/YYYY-MM-DD_consolidado-iniciativas.xlsx", index=False)
```

**Uso típico del orquestador:**
- Leer KPIs entregados por EO para incluir en el informe ejecutivo
- Crear tabla resumen de iniciativas activas con estado y responsable
- Consolidar datos de múltiples agentes en una sola tabla para presentación

### DOCX — Generar informe ejecutivo consolidado
```python
from docx import Document

doc = Document()
doc.add_heading("Informe Ejecutivo — Mejora Continua Arauco", 0)
doc.add_heading("Subgerencia de Mejora Continua", level=2)

# Sección EO
doc.add_heading("Excelencia Operacional", level=1)
doc.add_paragraph(hallazgos_eo)

# Sección IA
doc.add_heading("Inteligencia Artificial", level=1)
doc.add_paragraph(hallazgos_ia)

# Sección TD
doc.add_heading("Transformación Digital", level=1)
doc.add_paragraph(hallazgos_td)

# Recomendaciones integradas
doc.add_heading("Recomendaciones Estratégicas", level=1)
for rec in recomendaciones_consolidadas:
    doc.add_paragraph(rec, style="List Bullet")

doc.save("datos/YYYY-MM-DD_informe-ejecutivo-mejora-continua.docx")
```

**Uso típico del orquestador:**
- Leer informes previos para dar continuidad a la narrativa ejecutiva
- Generar el informe semanal o mensual de mejora continua consolidado
- Crear documentos de business case para presentar a gerencia
- Leer solicitudes del usuario en formato Word para entender el mandato

### PPTX — Presentaciones gerenciales
```python
from pptx import Presentation

# Leer presentación de plantilla corporativa
prs = Presentation("datos/plantillas/plantilla-corporativa-arauco.pptx")

# Agregar diapositiva de hallazgos
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Hallazgos — Semana 23"
tf = slide.placeholders[1].text_frame
tf.text = f"OEE Línea 3: {oee_actual}% (+{mejora}% vs. semana anterior)"
tf.add_paragraph().text = f"Pérdidas evitadas: {perdidas_evitadas} horas"
tf.add_paragraph().text = f"Modelo predictivo en validación: RMSE {rmse:.1f}h"

prs.save("datos/YYYY-MM-DD_presentacion-gerencia-semana23.pptx")
```

**Uso típico del orquestador:**
- Generar presentaciones semanales de KPIs para gerencia
- Actualizar deck de roadmap estratégico de mejora continua
- Crear material para comités de dirección con hallazgos de los tres agentes
- Leer presentaciones del usuario para entender contexto estratégico

### PDF — Leer documentos de negocio
```python
# Usar markitdown-mcp para leer rápidamente
# Tool: markitdown_convert → file_path: datos/informe-gerencia-anterior.pdf

# Para extracción de tablas específicas
import pdfplumber
with pdfplumber.open("datos/board-report-q1-2024.pdf") as pdf:
    for page in pdf.pages:
        texto = page.extract_text()
        if "OEE" in texto or "pérdida" in texto.lower():
            print(f"Página {page.page_number}:\n{texto}")
```

**Uso típico del orquestador:**
- Leer informes de gerencia anteriores para dar continuidad
- Extraer compromisos o KPIs de actas de directorio en PDF
- Leer reportes de benchmark externo para contextualizar hallazgos
- Procesar documentos estratégicos enviados por el usuario

---

## Convención de archivos del orquestador

| Entregable | Patrón | Audiencia |
|---|---|---|
| Informe ejecutivo | `datos/YYYY-MM-DD_informe-ejecutivo-[tema].docx` | Gerencia |
| Presentación gerencial | `datos/YYYY-MM-DD_presentacion-[tema].pptx` | Directorio / Gerencia |
| Tabla consolidada | `datos/YYYY-MM-DD_consolidado-[tema].xlsx` | Equipo MC |
| Business case | `datos/YYYY-MM-DD_business-case-[iniciativa].docx` | Gerencia / Directorio |

---

## Restricciones

- Los entregables ejecutivos deben tener: fecha, área responsable (Subgerencia MC) y próximo paso accionable
- El resumen ejecutivo en cualquier formato no puede superar media página
- Máximo 3 hallazgos y 3 recomendaciones en presentaciones gerenciales
- Los PDF son solo lectura: nunca intentar editarlos, generar el nuevo entregable en DOCX o PPTX
