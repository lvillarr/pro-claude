# Skill: test — Validacion de coherencia del output analitico

> **Agente:** DA — Analisis de Datos

## Proposito

Verificar que el dashboard y los calculos son internamente coherentes antes de entregar. Detectar KPIs calculados desde la muestra en lugar del total, caveats ausentes, graficos que no renderizan y filtros que no actualizan los graficos. Produce un veredicto: VALIDADO o RECHAZADO.

## Cuando usar

- Build completado: el archivo HTML existe en `datos/`
- Antes de ejecutar el skill `review` o `ship`
- Cuando el orquestador solicita verificacion de calidad del reporte

**Prerequisito:** Archivo HTML generado en `datos/YYYY-MM-DD_reporte-*.html`. Script Python o JSON de datos fuente disponible para verificar cifras.

## Protocolo

### Paso 1 — Verificar coherencia de KPIs vs. totales del archivo

Los KPIs de las cards deben coincidir con las estadisticas del dataframe completo. Recalcular desde el archivo fuente y comparar.

```python
import pandas as pd

# Cargar archivo fuente original
df = pd.read_excel('datos/archivo.xlsx', sheet_name='NombreHoja')

# Recalcular KPIs que deberian aparecer en el dashboard
verificacion = {
    'total_registros': len(df),
    'total_minutos': df['MINUTOS'].sum(),
    'top_equipo': df.groupby('EQUIPO')['MINUTOS'].sum().idxmax(),
    'top_equipo_minutos': df.groupby('EQUIPO')['MINUTOS'].sum().max(),
    'tipos_unicos': df['TIPO_PERDIDA'].nunique()
}

print("=== VERIFICACION KPIs ===")
for k, v in verificacion.items():
    print(f"{k}: {v}")

# Comprobar que no se usaron solo los top-20 para calcular los KPIs
muestra_top20 = df.nlargest(20, 'MINUTOS')
total_desde_muestra = muestra_top20['MINUTOS'].sum()
total_real = df['MINUTOS'].sum()
pct_muestra = total_desde_muestra / total_real * 100

if pct_muestra < 99:  # Si la muestra no cubre el 99%+ del total, hay diferencia significativa
    print(f"ALERTA: Total muestra top-20 ({total_desde_muestra:.1f}) ≠ Total real ({total_real:.1f})")
    print(f"La muestra representa solo el {pct_muestra:.1f}% del total — KPIs deben venir del total")
```

Extraer los valores del HTML y comparar:
```python
from bs4 import BeautifulSoup

with open('datos/YYYY-MM-DD_reporte-descripcion.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

cards = soup.select('.kpi-valor')
print("Valores en cards del HTML:")
for c in cards:
    print(f"  {c.text.strip()}")
```

Si BeautifulSoup no esta disponible, revisar el HTML manualmente buscando los valores de `.kpi-valor` y compararlos con los calculos de Python.

### Paso 2 — Verificar caveats de muestra

El HTML debe contener un bloque `.caveat` con este texto (o equivalente):

```
"Tabla de detalle muestra top-20 de [N] registros totales. KPIs y graficos incluyen la totalidad."
```

Checklist de caveats obligatorios:

| Caveat | Obligatorio si | Presente |
|---|---|---|
| Top-N vs. N total | Tabla de detalle con menos filas que el total | [ ] |
| Columnas con nulos criticos | Alguna columna clave tiene > 5% nulos | [ ] |
| Periodo cubierto | Siempre | [ ] |
| Fuente citada | Siempre | [ ] |
| Supuestos de limpieza | Si se eliminaron o imputaron filas | [ ] |

### Paso 3 — Verificar fuente citada en el HTML

El footer del HTML debe contener:
- Nombre del archivo fuente
- Nombre de la hoja o seccion
- Fecha de generacion del reporte

Buscar en el HTML:
```bash
grep -i "fuente\|source\|archivo\|sheet" datos/YYYY-MM-DD_reporte-descripcion.html | head -5
```

Si no hay referencia a la fuente, el test falla en este punto.

### Paso 4 — Verificar que los graficos tienen datos validos

```bash
# Buscar canvas sin datos o con errores comunes
grep -c '<canvas' datos/YYYY-MM-DD_reporte-descripcion.html
grep -c 'new Chart' datos/YYYY-MM-DD_reporte-descripcion.html
# Los dos conteos deben ser iguales
```

Verificar en el JSON embebido que no hay arrays vacios ni `null`:
```python
import re, json

with open('datos/YYYY-MM-DD_reporte-descripcion.html', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Extraer el objeto DATOS
match = re.search(r'const DATOS = ({.*?});', contenido, re.DOTALL)
if match:
    datos = json.loads(match.group(1))
    for key, val in datos.items():
        if isinstance(val, dict):
            if 'data' in val and len(val['data']) == 0:
                print(f"ALERTA: {key}.data esta vacio — grafico no renderizara")
            if 'labels' in val and len(val['labels']) != len(val.get('data', [])):
                print(f"ALERTA: {key} — labels ({len(val['labels'])}) != data ({len(val.get('data', []))})")
else:
    print("ALERTA: No se encontro const DATOS en el HTML")
```

### Paso 5 — Verificar filtros dinamicos

El HTML debe tener:
- Al menos un `<select class="filtro-select">` con `data-filtro` definido
- Funcion `aplicarFiltros()` que llama `chart.update()` para cada grafico
- Boton `btn-limpiar` que resetea todos los selectores

```bash
grep -c 'filtro-select' datos/YYYY-MM-DD_reporte-descripcion.html
grep -c 'chart\.update()' datos/YYYY-MM-DD_reporte-descripcion.html
grep -c 'btn-limpiar' datos/YYYY-MM-DD_reporte-descripcion.html
```

Resultado esperado: cada conteo >= 1. Si `chart.update()` aparece menos veces que el numero de graficos, algun grafico no se actualiza al filtrar.

### Paso 6 — Verificar formato numerico chileno

```python
# Buscar formatos incorrectos en el HTML (notacion anglosajona dentro de valores visibles)
with open('datos/YYYY-MM-DD_reporte-descripcion.html', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Patron: numero con coma como miles (anglosajona) en contexto visible — ej "1,234" sin decimales
import re
anglosajones = re.findall(r'>(\d{1,3},\d{3}[^,<])', contenido)
if anglosajones:
    print(f"POSIBLE ERROR formato: {anglosajones[:5]} — verificar si son miles anglosajones")

# Verificar que Intl.NumberFormat usa 'es-CL'
if 'es-CL' not in contenido:
    print("ALERTA: No se encontro Intl.NumberFormat con es-CL — formato numerico puede ser incorrecto")
```

### Paso 7 — Verificar que el HTML es standalone

```bash
# Verificar ausencia de CDN externos activos
grep -E 'src="https?://' datos/YYYY-MM-DD_reporte-descripcion.html
grep -E 'href="https?://' datos/YYYY-MM-DD_reporte-descripcion.html | grep -v 'canonical\|favicon'
```

Si aparecen URLs externas para scripts o estilos criticos (Chart.js, fonts), el test falla. El HTML debe funcionar sin conexion.

### Paso 8 — Emitir veredicto

| Veredicto | Criterio |
|---|---|
| VALIDADO | Todos los checks pasan |
| VALIDADO CON OBSERVACIONES | Fallas menores (formato, texto de caveat incompleto) — puede pasar a review con nota |
| RECHAZADO | KPI calculado desde muestra, grafico vacio, filtros no actualizan graficos, o sin fuente citada |

Si RECHAZADO: documentar que check fallo, volver a `build` con la correccion especifica.

## Checklist de Validacion DA

```
CHECKLIST TEST — DA
Archivo: datos/YYYY-MM-DD_reporte-descripcion.html
Fuente: datos/[archivo.ext] / hoja [nombre]
Fecha test: YYYY-MM-DD

COHERENCIA DE DATOS
[ ] KPI cards coinciden con totales del dataframe completo (no con muestra top-N)
[ ] Graficos usan datos de la totalidad del archivo (no solo top-20)
[ ] Tabla de detalle tiene caveat "top-N de M totales"
[ ] Ninguna cifra inventada o estimada sin fuente

CAVEATS Y FUENTE
[ ] Fuente citada: archivo, hoja, columnas usadas
[ ] Periodo cubierto indicado en header o footer
[ ] Nulos criticos documentados (si aplica)
[ ] Supuestos de limpieza documentados (si aplica)

TECNICO — HTML
[ ] Canvas count == new Chart count (ningun grafico sin inicializar)
[ ] DATOS.*.data y DATOS.*.labels tienen la misma longitud
[ ] Ningun array de datos vacio en la inicializacion de graficos
[ ] filtro-select count >= 1
[ ] chart.update() count >= numero de graficos del dashboard
[ ] btn-limpiar presente y funcional
[ ] Sin URLs externas en src= o href= (standalone verificado)
[ ] Intl.NumberFormat con 'es-CL' en el JS

FORMATO
[ ] Formato numerico chileno: 1.234,5 (no 1,234.5)
[ ] Branding Arauco: header #696158, borde-izq amarillo #BFB800, boton naranja #EA7600
[ ] Fuente Lato o sistema sans-serif declarada

VEREDICTO: VALIDADO | VALIDADO CON OBSERVACIONES | RECHAZADO
Observaciones: [lista de fallas si aplica]
```

## Restricciones

- No emitir VALIDADO si algun KPI de card proviene de `muestra_top20` en lugar del dataframe completo
- No emitir VALIDADO si la fuente no esta citada en el HTML
- No emitir VALIDADO si algun `<canvas>` no tiene su `new Chart` correspondiente
- Verificar el HTML con datos reales del archivo fuente — no confiar solo en inspeccion visual del HTML
- Si el archivo fuente no esta disponible para re-calcular (solo Telegram JSON), usar los `stats` del JSON como referencia de verificacion
- VALIDADO CON OBSERVACIONES solo para fallas menores de presentacion — cualquier error de datos o filtro es RECHAZADO
