# Skill: build — Desarrollo e Implementación IA

## Propósito

Ejecutar el desarrollo técnico del proyecto IA: ingesta y exploración de datos, feature engineering, entrenamiento de modelos o construcción de agentes GenAI, generación de dashboards y empaquetado del entregable. Es la fase de producción técnica que transforma el plan en código y resultados.

---

## Cuándo usar este skill

- El plan IA está aprobado (skill `plan` completado)
- Se necesita desarrollar: análisis exploratorio, modelo ML, agente LangGraph, dashboard HTML, script geo-espacial
- Se solicita generar un prototipo funcional (POC) para validar una hipótesis

**Prerequisito:** `agentes/IA/skills/plan/SKILL.md` aprobado con entorno técnico definido y datos accesibles.

---

## Protocolo de ejecución

### Paso 1 — Ingesta y EDA
```python
import pandas as pd
import sqlite3

# Cargar datos desde SGL o SQLite
conn = sqlite3.connect("datos/arauco_mc.db")
df = pd.read_sql("SELECT * FROM perdidas WHERE fecha >= '2024-01-01'", conn)

# Perfil de calidad
print(df.info())
print(df.describe())
print(df.isnull().sum())  # completitud
print(df.duplicated().sum())  # duplicados

# Guardar datos limpios
df.to_csv("datos/[proyecto]/processed/perdidas_clean.csv", index=False)
```

### Paso 2 — Feature engineering
```python
# Variables derivadas relevantes para el negocio forestal
df["hora_turno"] = pd.to_datetime(df["timestamp"]).dt.hour
df["dia_semana"] = pd.to_datetime(df["timestamp"]).dt.dayofweek
df["duracion_min"] = (df["fin"] - df["inicio"]).dt.total_seconds() / 60
df["es_equipo_critico"] = df["equipo"].isin(["HAR01", "HAR02", "PRO01"])
```

### Paso 3 — Modelado ML
```python
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
import joblib

X = df[feature_cols]
y = df["target"]

model = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42)
scores = cross_val_score(model, X, y, cv=5, scoring="neg_root_mean_squared_error")
print(f"RMSE CV: {-scores.mean():.3f} ± {scores.std():.3f}")

model.fit(X, y)
joblib.dump(model, "datos/[proyecto]/models/YYYY-MM-DD_modelo-[nombre]-v1.pkl")
```

### Paso 4 — Agentes GenAI (Claude API)
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=2048,
    system="Eres un experto en operaciones forestales de Arauco...",
    messages=[{"role": "user", "content": prompt}]
)
```

Para agentes con tool use, usar el skill `genai-agents`.

### Paso 5 — Dashboard HTML (sin dependencias externas)
```python
import json

data = df.groupby("fecha")["perdida_min"].sum().reset_index()
chart_data = data.to_dict(orient="list")

html = f"""<!DOCTYPE html>
<html><head><title>KPI Dashboard — {area}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script></head>
<body>
<canvas id="chart"></canvas>
<script>
const data = {json.dumps(chart_data)};
new Chart(document.getElementById('chart'), {{
  type: 'line',
  data: {{ labels: data.fecha, datasets: [{{
    label: 'Pérdidas (min)', data: data.perdida_min
  }}]}}
}});
</script></body></html>"""

with open("datos/YYYY-MM-DD_dashboard-[nombre].html", "w") as f:
    f.write(html)
```

### Paso 6 — Cartografía IA
```python
import geopandas as gpd
from shapely.geometry import Point

# Cargar capa de predios
predios = gpd.read_file("datos/[proyecto]/raw/predios.geojson")
predios = predios.to_crs("EPSG:32719")  # UTM zona 19S (Chile sur)

# Cruzar con productividad de equipos
resultado = predios.merge(df_productividad, on="id_predio")
resultado.to_file("datos/YYYY-MM-DD_mapa-productividad.geojson", driver="GeoJSON")
```

### Paso 7 — Log de construcción
Registrar en el log:
- Experimentos corridos y resultados
- Decisiones de diseño tomadas
- Desviaciones respecto al plan

### Paso 8 — Entregar
```
datos/YYYY-MM-DD_analisis-eda-[proyecto].html
datos/[proyecto]/models/YYYY-MM-DD_modelo-[nombre]-v1.pkl
datos/YYYY-MM-DD_dashboard-[nombre].html
datos/YYYY-MM-DD_mapa-[nombre].geojson
datos/YYYY-MM-DD_build-log-ia-[proyecto].md
```

---

## Restricciones de este skill

- Guardar datos crudos en `raw/` sin modificarlos: todos los procesamientos van en `processed/`
- No evaluar el modelo en el mismo conjunto de entrenamiento: respetar el protocolo definido en `plan`
- Los dashboards HTML deben funcionar sin servidor local (abrir directo en browser)
- Todo modelo debe incluir importancia de features y métricas de evaluación en el log
- Las capas geográficas deben especificar el CRS (sistema de referencia de coordenadas)
