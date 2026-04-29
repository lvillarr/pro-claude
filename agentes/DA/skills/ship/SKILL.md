# Skill: ship — Entrega del reporte final

> **Agente:** DA — Analisis de Datos

## Proposito

Nombrar, guardar y entregar el reporte final al orquestador o al solicitante. Emitir el bloque `ENTREGA DA:` completo con archivo, fuente, hallazgos cuantificados, caveats de muestra y limitaciones. Sin este bloque, el ciclo no esta cerrado.

## Cuando usar

- Review emitio habilitacion HABILITADO (o HABILITADO CON CONDICIONES resueltas)
- El orquestador o usuario requiere el reporte final para tomar una decision operacional
- Contexto Claude Code: guardar en `datos/` y reportar al orquestador
- Contexto Telegram: entregar texto resumen + HTML inline al usuario

**Prerequisito:** `datos/YYYY-MM-DD_reporte-*.html` con review HABILITADO. Sin habilitacion del review, no hay ship.

## Protocolo

### Paso 1 — Definir el nombre del archivo final

Convencion obligatoria:
```
YYYY-MM-DD_reporte-[area-o-proceso]-[descripcion-corta].html
```

Reglas de nombrado:
- Fecha: la del dia de entrega, no la de generacion del build
- `reporte`: prefijo fijo para archivos HTML de analisis
- Area/proceso: slug sin espacios ni mayusculas — usar guion medio
- Descripcion: 2-4 palabras que describan el contenido, no la metodologia

Ejemplos validos:
```
2026-04-29_reporte-linea3-perdidas-mayo.html
2026-04-29_reporte-cosecha-q1-contratistas.html
2026-04-29_reporte-oee-planta-celulosa.html
2026-04-29_reporte-sgl-semana18-paradas.html
```

Ejemplos invalidos:
```
reporte.html                          (sin fecha)
2026-04-29_analisis-datos.html        (tipo incorrecto — analisis es para .xlsx no .html)
2026-04-29_dashboard-linea3.html      (usar reporte, no dashboard)
2026-04-29_Reporte Linea 3.html       (mayusculas y espacios)
```

### Paso 2 — Guardar en datos/

```python
import shutil
from datetime import date

# Si el archivo ya tiene el nombre correcto desde el build, solo verificar ubicacion
import os
archivo_build = 'datos/YYYY-MM-DD_reporte-descripcion-build.html'
archivo_final = f"datos/{date.today().strftime('%Y-%m-%d')}_reporte-[area]-[descripcion].html"

# Renombrar si la fecha del build es diferente a hoy
if archivo_build != archivo_final:
    shutil.copy(archivo_build, archivo_final)
    print(f"Guardado como: {archivo_final}")
else:
    print(f"Archivo ya en ubicacion correcta: {archivo_final}")

# Verificar que el archivo existe y tiene contenido
tamaño = os.path.getsize(archivo_final)
print(f"Tamaño: {tamaño:,} bytes")
if tamaño < 10_000:
    print("ALERTA: Archivo muy pequeno — verificar que el build se completo")
```

Si hay un script Python generado durante el build, guardarlo tambien:
```
datos/YYYY-MM-DD_script-[area]-[descripcion].py
```

### Paso 3 — Verificar accesibilidad del archivo

```python
# Verificar que el HTML abre sin errores basicos
with open(archivo_final, 'r', encoding='utf-8') as f:
    contenido = f.read()

assert '<html' in contenido, "ERROR: Archivo no es HTML valido"
assert '</html>' in contenido, "ERROR: HTML sin cierre"
assert 'ENTREGA' not in contenido, "ERROR: Bloque ENTREGA DA: no debe estar dentro del HTML"

# Contar elementos clave
n_canvas = contenido.count('<canvas')
n_charts = contenido.count('new Chart')
n_filtros = contenido.count('filtro-select')

print(f"Canvas: {n_canvas} | Charts: {n_charts} | Filtros: {n_filtros}")
print("Archivo listo para entrega" if n_canvas == n_charts else "REVISAR: canvas != charts")
```

### Paso 4 — Construir el bloque ENTREGA DA:

El bloque `ENTREGA DA:` es el protocolo de comunicacion con el orquestador. Estructura obligatoria:

```
ENTREGA DA:
Archivo(s): datos/YYYY-MM-DD_reporte-[area]-[descripcion].html
Fuente: [archivo.ext] / hoja "[NombreHoja]" / columnas usadas: [lista]
Hallazgos clave:
  1. [Hallazgo cuantificado — metrica, valor en formato chileno, periodo]
  2. [Hallazgo cuantificado — ranking o comparacion con cifras]
  3. [Hallazgo cuantificado — tendencia o caveat relevante para decision]
Caveats de muestra: [N registros totales analizados. Tabla de detalle muestra top-20. Columnas con nulos: lista si aplica]
Limitaciones: [columnas sin datos, supuestos de limpieza, periodos sin cobertura, datos no verificables]
```

Ejemplo completo:
```
ENTREGA DA:
Archivo(s): datos/2026-04-29_reporte-linea3-perdidas-abril.html
Fuente: SGL_Perdidas_Abril2026.xlsx / hoja "Detalle" / columnas: FECHA, EQUIPO, LINEA, TURNO, TIPO_PERDIDA, MINUTOS
Hallazgos clave:
  1. Total de 4.832 min de paradas no planificadas en abril (80,5 h), un 12,3% mas que marzo (4.304 min). Fuente: SUM(MINUTOS), N=1.247 registros.
  2. Equipo Descortezador L3-01 concentra el 34,7% del total (1.677 min), seguido de Bomba P-421 con 18,2% (880 min).
  3. El turno noche acumula el 41,3% de las perdidas (1.996 min), versus 29,8% en turno dia — brecha de 11,5 pp.
Caveats de muestra: 1.247 registros totales analizados. Tabla de detalle muestra top-20 ordenados por MINUTOS. KPIs y graficos calculados desde el total. TURNO: 23 nulos (1,8%) reemplazados por "Sin turno".
Limitaciones: Columna COSTO_HORA vacia en el 100% de los registros — impacto economico no calculable. Periodo cubre 2026-04-01 a 2026-04-28 (28 dias — faltan 2 dias del mes).
```

Reglas del bloque:
- Hallazgos: exactamente 3, con cifras reales del archivo, en formato numerico chileno
- Hallazgos: deben responder directamente la pregunta del spec
- Caveats de muestra: siempre incluir N total, top-N de tabla, y nulos criticos
- Limitaciones: columnas vacias, periodos incompletos, datos que se esperaban pero no estaban

### Paso 5 — Entregar en Telegram (si contexto bot)

En contexto Telegram, el ship emite:

**Texto resumen** (maximo 5 puntos, con cifras en formato chileno):
```
Analisis completado — [N] registros de [archivo] ([periodo])

Principales hallazgos:
1. [hallazgo con cifra]
2. [hallazgo con cifra]
3. [hallazgo con cifra]

Caveat: tabla de detalle muestra top-20 de [N] registros totales. KPIs calculados sobre la totalidad.
Fuente: [archivo] / hoja [nombre]
```

Seguido del archivo HTML adjunto (si el bot lo soporta) o del HTML inline.

### Paso 6 — Registrar en datos/ (contexto Claude Code solamente)

Guardar adicionalmente un archivo de registro del ciclo si el analisis es parte de un proyecto formal:
```
datos/YYYY-MM-DD_entrega-da-[area]-[descripcion].md
```

Con el contenido del bloque `ENTREGA DA:` y referencia al spec y plan del ciclo.

## Checklist de Ship

```
CHECKLIST SHIP — DA
Fecha entrega: YYYY-MM-DD
Archivo: datos/YYYY-MM-DD_reporte-[area]-[descripcion].html

NOMBRE DE ARCHIVO
[ ] Prefijo de fecha YYYY-MM-DD correcto
[ ] Tipo "reporte" (no "analisis", "dashboard" ni "kpi")
[ ] Slug sin espacios, sin mayusculas, con guiones medios
[ ] Extension .html

ARCHIVO
[ ] Guardado en datos/ (no en raiz ni en subcarpeta)
[ ] Tamaño > 10 KB (no truncado)
[ ] HTML abre sin error (html y /html presentes)
[ ] canvas count == new Chart count

BLOQUE ENTREGA DA:
[ ] Archivo(s): path completo en datos/
[ ] Fuente: archivo, hoja, columnas usadas
[ ] Hallazgos clave: exactamente 3, con cifras reales en formato chileno
[ ] Caveats de muestra: N total + top-N tabla + nulos criticos
[ ] Limitaciones: columnas vacias, periodos incompletos

PREREQUISITOS
[ ] Test: VALIDADO (o VALIDADO CON OBSERVACIONES resueltas)
[ ] Review: HABILITADO (o HABILITADO CON CONDICIONES resueltas)
```

## Restricciones

- No hacer ship sin review HABILITADO
- El bloque `ENTREGA DA:` es obligatorio en contexto Claude Code — sin el bloque, el ciclo no esta cerrado para el orquestador
- Hallazgos clave: exactamente 3, con cifras reales. No usar "varios", "muchos", "significativo" sin cuantificar
- Formato numerico chileno en el bloque ENTREGA DA: `1.247 registros`, `80,5 h`, `34,7%`, `$1.250.000`
- No incluir el bloque `ENTREGA DA:` dentro del archivo HTML — va solo en el mensaje al orquestador
- Si el script Python fue generado durante el build, incluirlo en `Archivo(s):` del bloque
- Nunca sobreescribir un reporte existente con el mismo nombre — agregar sufijo `-v2` si es una revision del mismo dia
