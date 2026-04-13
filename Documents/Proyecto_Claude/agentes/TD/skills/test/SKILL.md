# Skill: test — Validación de Soluciones de Transformación Digital

## Propósito

Verificar que la integración, pipeline o automatización construida funciona correctamente bajo condiciones reales: datos íntegros, errores manejados, reconexión funcional y KPIs de éxito moviéndose en la dirección correcta. No avanza a `review` si hay pérdida de datos, errores no manejados o KPIs sin mejora.

---

## Cuándo usar este skill

- Los entregables del skill `build` están completos (scripts funcionan en entorno de desarrollo)
- Se necesita validar en entorno real o staging con datos reales
- Se requiere confirmar que los datos fluyen íntegros entre sistemas

**Prerequisito:** build completado con scripts y configuración listos.

---

## Protocolo de ejecución

### Paso 1 — Definir el plan de prueba
- ¿Qué se prueba? (integración, ETL, telemetría, sync offline)
- ¿En qué entorno? (staging con datos reales, subconjunto de producción)
- ¿Por cuánto tiempo? (al menos un ciclo completo: turno / día / semana)
- ¿Cuáles son los criterios de aprobación?

### Paso 2 — Pruebas de integridad de datos
Verificar que los datos llegan íntegros del sistema fuente al destino:

```python
import pandas as pd
import sqlite3

# Datos en fuente
df_fuente = extraer_de_api(fecha_inicio, fecha_fin)

# Datos en destino
conn = sqlite3.connect("datos/arauco_mc.db")
df_destino = pd.read_sql(f"""
    SELECT * FROM tabla WHERE fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
""", conn)

# Comparar
print(f"Fuente: {len(df_fuente)} registros")
print(f"Destino: {len(df_destino)} registros")
print(f"Diferencia: {len(df_fuente) - len(df_destino)}")

# Verificar campos clave
assert df_fuente["id_equipo"].nunique() == df_destino["id_equipo"].nunique(), \
    "Equipos faltantes en destino"

# Verificar valores numéricos
for campo in ["horas_operacion", "produccion_m3"]:
    diff = abs(df_fuente[campo].sum() - df_destino[campo].sum())
    print(f"{campo}: diferencia total = {diff:.2f}")
```

### Paso 3 — Pruebas de manejo de errores
Simular condiciones adversas:
```python
# Test: sin conectividad → datos se encolan
# → desconectar red, ejecutar pipeline
# → verificar que datos quedaron en sync_queue
# → reconectar, ejecutar sync
# → verificar que datos llegaron al destino

# Test: campo nulo en API → no falla, registra advertencia
# → enviar payload con campo_clave = null
# → verificar log: "WARNING — registro descartado por campo_clave nulo"

# Test: timeout de API → reintenta N veces antes de fallar
# → simular respuesta lenta
# → verificar comportamiento de retry
```

### Paso 4 — Pruebas de rendimiento
```python
import time

inicio = time.time()
pipeline_completo(fecha_inicio, fecha_fin)
duracion = time.time() - inicio

registros = len(df_destino)
print(f"Throughput: {registros/duracion:.1f} registros/segundo")
print(f"Duración total: {duracion:.1f}s para {registros} registros")

# Criterio: debe completar el volumen diario en < [N] minutos
```

### Paso 5 — Verificar KPIs de éxito
Para cada KPI definido en `spec`:
| KPI | Línea base | Meta | Valor durante test | ¿Cumple? |
|---|---|---|---|---|
| Latencia de datos (min entre evento y disponibilidad) | | | | |
| Completitud de registros (%) | | | | |
| Errores no manejados en 24h | | | | |

### Paso 6 — Clasificar resultado
- **APROBADO**: integridad 100%, errores manejados, KPIs en rango → avanzar a `review`
- **APROBADO CON OBS.**: integridad ≥ 98%, errores menores documentados → avanzar con ajustes pendientes
- **REPROBADO**: pérdida de datos, errores críticos no manejados, KPI principal no cumplido → volver a `build`

### Paso 7 — Entregar
```
datos/YYYY-MM-DD_test-td-[nombre-iniciativa].md
```

---

## Plantilla de reporte de test TD

```markdown
# Reporte de Test TD — [Nombre Iniciativa]
**Fecha:** YYYY-MM-DD | **Entorno:** staging / subconjunto producción
**Duración del test:** [N días / ciclos]

## Integridad de datos
| Fuente | Destino | Registros fuente | Registros destino | Completitud |
|---|---|---|---|---|

## Manejo de errores
| Escenario | Comportamiento esperado | Comportamiento real | ¿Correcto? |
|---|---|---|---|
| Sin conectividad | Encolar, reintentar | | |
| Campo nulo | Descartar + warning | | |
| Timeout API | Retry × 3, luego error | | |

## Rendimiento
| Métrica | Meta | Resultado |
|---|---|---|
| Throughput (registros/s) | | |
| Latencia fuente → destino | | |

## KPIs de éxito
| KPI | Meta | Resultado | ¿Cumple? |
|---|---|---|---|

## Resultado: APROBADO / APROBADO CON OBS. / REPROBADO
```

---

## Restricciones de este skill

- No aprobar con menos del 98% de completitud de datos: pérdida de registros en producción es inaceptable
- Las pruebas de falla de conectividad son obligatorias si el contexto es terreno forestal
- Los logs del pipeline deben mostrar evidencia clara de cada paso: si no está en el log, no se puede verificar
