# Skill: test — Validación de Modelos y Soluciones IA

## Propósito

Verificar que la solución IA cumple las métricas de éxito definidas en `spec` y que sus outputs son correctos, interpretables y útiles para el equipo operacional. Combina evaluación técnica del modelo con validación humana de los resultados. No avanza a `review` si las métricas no están en rango o los outputs no son accionables.

---

## Cuándo usar este skill

- Los entregables del skill `build` están completos
- Se necesita evaluar si un modelo ML cumple las métricas definidas
- Se requiere validar que los outputs de un agente GenAI son correctos y seguros
- Se debe confirmar que un dashboard o mapa es interpretable y correcto antes de entregarlo

**Prerequisito:** `agentes/IA/skills/build/SKILL.md` completado con modelos entrenados y entregables generados.

---

## Protocolo de ejecución

### Paso 1 — Definir el plan de validación
Revisar métricas definidas en `spec` y preparar:
- Conjunto de test separado (datos no vistos durante entrenamiento)
- Casos de prueba representativos del contexto operacional
- Lista de validadores del equipo (quién aprueba que el output es útil)

### Paso 2 — Evaluación técnica de modelos ML

```python
import joblib
import numpy as np
from sklearn.metrics import (mean_squared_error, mean_absolute_error,
                              accuracy_score, f1_score, classification_report)

model = joblib.load("datos/[proyecto]/models/YYYY-MM-DD_modelo-[nombre]-v1.pkl")

# Regresión
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae  = mean_absolute_error(y_test, y_pred)
print(f"RMSE: {rmse:.3f} | MAE: {mae:.3f}")

# Clasificación
print(classification_report(y_test, y_pred))

# Comparar con baseline
rmse_baseline = np.sqrt(mean_squared_error(y_test, [y_train.mean()]*len(y_test)))
print(f"Mejora sobre baseline: {(rmse_baseline - rmse)/rmse_baseline*100:.1f}%")
```

### Paso 3 — Importancia de features y explicabilidad

```python
import pandas as pd
import matplotlib.pyplot as plt

# Feature importance (para modelos tree-based)
importances = pd.Series(model.feature_importances_, index=feature_cols)
importances.sort_values(ascending=False).head(10).plot(kind="bar")
plt.tight_layout()
plt.savefig("datos/[proyecto]/outputs/feature_importance.png")

# ¿Los features más importantes tienen sentido operacional?
# → Validar con supervisor o experto de terreno
```

### Paso 4 — Validación de agentes GenAI

Para cada caso de uso definido en `spec`:
```
Caso de prueba: [descripción del input]
Output esperado: [qué debería responder el agente]
Output real: [qué respondió]
Evaluación: Correcto / Parcial / Incorrecto
Riesgo de alucinación: Sí / No
```

Criterios de aprobación para GenAI:
- El agente no inventa datos forestales no proporcionados
- Las respuestas son accionables por el equipo operacional
- Los errores son detectables (el agente admite incertidumbre cuando corresponde)

### Paso 5 — Validación de dashboards y mapas

Verificar:
- [ ] Dashboard abre sin servidor local (doble clic en el `.html`)
- [ ] Los KPIs coinciden con los datos fuente (spot check manual)
- [ ] Las fechas y unidades son correctas
- [ ] El mapa usa el CRS correcto y las capas se superponen correctamente
- [ ] Un supervisor puede interpretarlo sin asistencia técnica

### Paso 6 — Validación con usuario operacional

Mostrar el entregable a al menos un usuario del perfil objetivo:
- ¿Entiende qué muestra?
- ¿Confía en los resultados?
- ¿Lo usaría para tomar decisiones?
- ¿Qué cambiaría?

### Paso 7 — Clasificar resultado
- **APROBADO**: métricas en rango, outputs validados por usuario → avanzar a `review`
- **APROBADO CON OBSERVACIONES**: métricas cumplidas, ajustes menores de presentación → documentar y avanzar
- **REPROBADO**: métrica crítica no cumplida o usuario no confía en el output → volver a `build`

### Paso 8 — Entregar
```
datos/YYYY-MM-DD_test-ia-[nombre-proyecto].md
```

---

## Plantilla de reporte de test IA

```markdown
# Reporte de Validación IA — [Nombre Proyecto]
**Fecha:** YYYY-MM-DD
**Responsable:** [Nombre]

## Métricas técnicas vs. meta
| Métrica | Meta (spec) | Resultado test | Baseline | Cumple |
|---|---|---|---|---|

## Explicabilidad
- Features más importantes: [lista con interpretación operacional]
- ¿El modelo tiene sentido para un experto forestal? Sí / No — [comentario]

## Validación de usuario
| Usuario | Perfil | ¿Entiende? | ¿Confía? | ¿Lo usaría? | Comentario |
|---|---|---|---|---|---|

## Problemas encontrados
| ID | Descripción | Impacto | Acción requerida |
|---|---|---|---|

## Resultado: APROBADO / APROBADO CON OBS. / REPROBADO
```

---

## Restricciones de este skill

- No se puede aprobar un modelo evaluado solo en datos de entrenamiento
- La validación de usuario es obligatoria: un modelo técnicamente correcto pero inutilizable es un modelo fallido
- Para series de tiempo, usar validación walk-forward, no split aleatorio
- Los agentes GenAI deben probarse con inputs adversariales (preguntas fuera de dominio, datos faltantes)
