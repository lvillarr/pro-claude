# Skill: ship — Cierre y Entrega de Proyectos IA

## Propósito

Cerrar formalmente el proyecto IA: documentar la solución, transferir el conocimiento al área operacional, versionar el código y los modelos, y registrar lecciones aprendidas. Asegura que la solución sea mantenible y que su valor no se pierda cuando el equipo IA pase a la siguiente iniciativa.

---

## Cuándo usar este skill

- El skill `review` fue completado con decisión de aprobación
- Todos los ajustes críticos identificados en review fueron resueltos
- Se necesita hacer el hand-off formal al área operacional o a TI

**Prerequisito:** `agentes/IA/skills/review/SKILL.md` aprobado sin hallazgos críticos pendientes.

---

## Protocolo de ejecución

### Paso 1 — Verificar condiciones de cierre
- [ ] Métricas de éxito cumplidas y documentadas
- [ ] Código versionado en git con README
- [ ] Modelo con metadatos completos (fecha de entrenamiento, datos usados, métricas)
- [ ] Sin hallazgos críticos pendientes del review

### Paso 2 — Documentar la solución

**README del proyecto** (en `datos/[proyecto]/`):
```markdown
# [Nombre del Proyecto IA]
**Tipo:** ML / GenAI / Dashboard / Cartografía
**Fecha de entrega:** YYYY-MM-DD
**Versión:** v1.0

## Qué hace
[Descripción en 3 líneas. Sin jerga técnica.]

## Cómo usar
[Instrucciones paso a paso para el usuario final]

## Cómo reentrenar / actualizar
[Pasos para actualizar el modelo o los datos]

## Dependencias
pip install [lista de librerías con versión]

## Contacto
[Área IA — nombre del responsable técnico]
```

### Paso 3 — Versionar modelos y entregables
```bash
git add datos/[proyecto]/
git commit -m "ship: [nombre-proyecto] v1.0 — [descripción breve]"
git tag v1.0-[nombre-proyecto]
```

Registrar metadatos del modelo:
```python
metadata = {
    "modelo": "GradientBoostingRegressor",
    "version": "1.0",
    "fecha_entrenamiento": "YYYY-MM-DD",
    "datos_entrenamiento": "perdidas_2022_2024.csv",
    "n_registros": 15420,
    "features": feature_cols,
    "metricas": {"rmse": 2.34, "mae": 1.87},
    "responsable": "Área IA"
}
import json
with open("datos/[proyecto]/models/metadata_v1.0.json", "w") as f:
    json.dump(metadata, f, indent=2)
```

### Paso 4 — Transferir al área operacional
- Sesión de demostración con usuarios finales
- Entrega de documentación (README, guía de uso)
- Designar responsable de seguimiento de métricas post-entrega
- Definir plan de reentrenamiento o actualización (frecuencia, disparador)

### Paso 5 — Documentar lecciones aprendidas
- ¿Qué tipo de datos fue más valioso?
- ¿Qué modelo o enfoque funcionó mejor y por qué?
- ¿Qué haría diferente al inicio del proyecto?
- ¿Qué oportunidades adicionales se identificaron?

### Paso 6 — Entregar y reportar
```
datos/YYYY-MM-DD_ship-ia-[nombre-proyecto].md
datos/[proyecto]/README.md
datos/[proyecto]/models/metadata_v1.0.json
```

Reportar al Orquestador:
```
ENTREGA IA:
Archivo(s): datos/YYYY-MM-DD_[tipo]-ia-[proyecto].[ext]
Hallazgos clave: [máximo 3 puntos cuantificados]
Limitaciones: [supuestos, datos faltantes, restricciones de uso]
Impacto esperado: [qué decisión operacional habilita, con métrica]
```

---

## Plantilla de cierre IA

```markdown
# Cierre de Proyecto IA — [Nombre]
**Fecha:** YYYY-MM-DD | **PM:** [Nombre] | **Sponsor:** [Cargo]

## Resultados finales
| Métrica | Meta | Resultado | Mejora vs. baseline |
|---|---|---|---|

## Entregables versionados
| Entregable | Archivo | Versión |
|---|---|---|

## Plan de mantenimiento
- **Reentrenamiento:** [frecuencia o disparador]
- **Responsable técnico:** [nombre]
- **Responsable operacional:** [nombre]
- **Revisión a 90 días:** [fecha]

## Lecciones aprendidas
**Funcionó bien:** [lista]
**Difícil y cómo se resolvió:** [lista]
**Haría diferente:** [lista]
**Oportunidades identificadas:** [lista]

## Estado: CERRADO
```

---

## Restricciones de este skill

- No cerrar sin README comprensible para alguien que no participó en el proyecto
- El plan de reentrenamiento es obligatorio: los modelos se degradan sin datos nuevos
- Versionar el modelo con metadatos completos: en 6 meses nadie recordará con qué datos se entrenó
- La revisión de rendimiento a 90 días es obligatoria para detectar model drift
