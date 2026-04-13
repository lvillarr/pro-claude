# Skill: ship — Entrega Ejecutiva Final (Orquestador)

## Propósito

Generar y entregar el entregable ejecutivo consolidado al usuario: informe, presentación o plan de acción que integra los outputs de todos los agentes en un documento de nivel directivo. Asegura que el trabajo del equipo se traduce en valor visible para la organización.

---

## Cuándo usar este skill

- El skill `review` fue completado y la síntesis ejecutiva está lista
- Se necesita generar el entregable final en el formato solicitado (docx, pptx, html, md)
- El usuario debe presentar los resultados a gerencia o a un equipo externo

**El orquestador entrega: documenta el trabajo del equipo en lenguaje de negocio.**

---

## Protocolo de ejecución

### Paso 1 — Confirmar formato del entregable
Según la audiencia definida en `spec`:
| Audiencia | Formato preferido | Herramienta |
|---|---|---|
| Directorio / Gerencia General | Presentación `.pptx` | python-pptx |
| Subgerencia / Jefatura | Informe ejecutivo `.docx` | python-docx |
| Equipo técnico | Markdown `.md` o HTML | write_file |
| Dashboard operacional | `.html` interactivo | Chart.js |

### Paso 2 — Generar el entregable en el formato correspondiente

**Informe ejecutivo en DOCX:**
```python
from docx import Document
from docx.shared import Pt, RGBColor

doc = Document()
# Portada
doc.add_heading("Informe Ejecutivo — [Nombre Iniciativa]", 0)
doc.add_paragraph(f"Arauco — Subgerencia Mejora Continua | {fecha}")

# Resumen ejecutivo (max media página)
doc.add_heading("Resumen Ejecutivo", level=1)
doc.add_paragraph(resumen_ejecutivo)

# Hallazgos clave
doc.add_heading("Hallazgos Clave", level=1)
for i, hallazgo in enumerate(hallazgos, 1):
    doc.add_paragraph(f"{i}. {hallazgo}", style="List Number")

# Recomendaciones
doc.add_heading("Recomendaciones", level=1)
tabla = doc.add_table(rows=1, cols=4)
tabla.style = "Table Grid"
for celda, header in zip(tabla.rows[0].cells,
                          ["Acción", "Responsable", "Plazo", "Criterio"]):
    celda.text = header
for accion in recomendaciones:
    fila = tabla.add_row().cells
    fila[0].text = accion["que"]
    fila[1].text = accion["quien"]
    fila[2].text = accion["cuando"]
    fila[3].text = accion["criterio"]

# Próximos pasos
doc.add_heading("Próximos Pasos", level=1)
doc.add_paragraph(proximos_pasos)

doc.save(f"datos/{fecha}_informe-ejecutivo-{nombre_iniciativa}.docx")
```

**Presentación ejecutiva en PPTX:**
```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()

# Diapositiva 1: Portada
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = nombre_iniciativa
slide.placeholders[1].text = f"Arauco — Subgerencia Mejora Continua | {fecha}"

# Diapositiva 2: Resumen ejecutivo
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Resumen Ejecutivo"
tf = slide.placeholders[1].text_frame
tf.text = situacion
for punto in [complicacion, pregunta_clave]:
    tf.add_paragraph().text = punto

# Diapositiva 3: Hallazgos clave (máximo 3)
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Hallazgos Clave"
tf = slide.placeholders[1].text_frame
for hallazgo in hallazgos[:3]:
    tf.add_paragraph().text = f"→ {hallazgo}"

# Diapositiva 4: Recomendaciones
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Recomendaciones"
tf = slide.placeholders[1].text_frame
for rec in recomendaciones[:3]:
    tf.add_paragraph().text = f"→ {rec['que']} — {rec['quien']} — {rec['cuando']}"

prs.save(f"datos/{fecha}_presentacion-{nombre_iniciativa}.pptx")
```

### Paso 3 — Versionar el entregable en git
```bash
git add datos/YYYY-MM-DD_[entregable-final].[ext]
git add datos/YYYY-MM-DD_spec-orq-[iniciativa].md
git add datos/YYYY-MM-DD_plan-orq-[iniciativa].md
git add datos/YYYY-MM-DD_review-orq-[iniciativa].md
git commit -m "ship: [nombre-iniciativa] — entregable ejecutivo consolidado"
```

### Paso 4 — Presentar al usuario
Reportar con estructura ejecutiva:
```
ENTREGA CONSOLIDADA — [Nombre Iniciativa]

Situación: [contexto en 1 línea]
Complicación: [por qué importa ahora]
Hallazgos clave:
  1. [hallazgo cuantificado — área responsable]
  2. [hallazgo cuantificado — área responsable]
  3. [hallazgo cuantificado — área responsable]
Recomendaciones:
  1. [acción] — [responsable] — [plazo]
  2. [acción] — [responsable] — [plazo]
Próximos pasos: [qué debe aprobar o decidir el usuario]
Archivo: datos/YYYY-MM-DD_[nombre].[ext]
```

### Paso 5 — Registrar lecciones del ciclo de orquestación
```
datos/YYYY-MM-DD_lecciones-orq-[nombre-iniciativa].md
```

---

## Restricciones de este skill

- El resumen ejecutivo no puede superar media página: si cabe en dos, está mal redactado
- Máximo 3 hallazgos y 3 recomendaciones: más diluye el mensaje
- Cada recomendación debe tener responsable real (cargo + nombre), no "el área de EO"
- Los entregables consolidados se versionan en git: son el registro formal del trabajo del equipo
- Nunca entregar sin haber pasado por `review`: el usuario recibe el mejor trabajo del equipo, no el primero
