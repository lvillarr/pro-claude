# Skill: build — Ejecucion del analisis y construccion del dashboard HTML

> **Agente:** DA — Analisis de Datos

## Proposito

Ejecutar el plan aprobado: limpiar los datos, calcular los KPIs y construir el dashboard HTML interactivo con branding Arauco. El output es un archivo `.html` standalone que funciona sin servidor ni conexion a internet.

## Cuando usar

- Plan en estado APROBADO
- Spec en estado APROBADO
- Se requiere un reporte HTML interactivo, script Python o tabla de analisis

**Prerequisito:** `datos/YYYY-MM-DD_plan-[area].md` en estado APROBADO. Sin plan aprobado no se construye. Si el build se ejecuta en contexto Telegram (JSON pre-procesado), el plan puede ser informal pero las preguntas de negocio deben estar claras.

## Protocolo

### Paso 1 — Inspeccion y carga del archivo

```python
import pandas as pd
import numpy as np
import json

# Contexto Claude Code: leer desde datos/
df = pd.read_excel('datos/archivo.xlsx', sheet_name='NombreHoja')
print(f"Shape cargado: {df.shape[0]:,} filas x {df.shape[1]} columnas")

# Contexto Telegram: datos ya en JSON
# data = json.loads(telegram_payload)
# stats = data['NombreHoja']['stats']
# muestra = data['NombreHoja']['muestra_top20']
# total_filas = data['NombreHoja']['total_filas']
```

### Paso 2 — Limpieza segun plan

Aplicar exactamente las limpiezas del plan. Documentar cada cambio con conteo de registros afectados.

```python
filas_original = len(df)

# Estandarizar nulos (strings vacios y placeholders)
df.replace(['<Null>', '<null>', 'NULL', '', ' ', 'N/A', 'n/a'], np.nan, inplace=True)

# Convertir fechas
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')
fechas_invalidas = df['FECHA'].isnull().sum()
if fechas_invalidas > 0:
    print(f"AVISO: {fechas_invalidas} fechas no convertibles — se trataran como NaT")

# Convertir columnas numericas mal formateadas
for col in ['MINUTOS', 'COSTO_HORA', 'TONELADAS']:
    if df[col].dtype == object:
        df[col] = df[col].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Eliminar duplicados exactos
df.drop_duplicates(inplace=True)
print(f"Duplicados eliminados: {filas_original - len(df)}")

# Registrar nulos criticos (columnas que son dimension o metrica del spec)
cols_criticas = ['EQUIPO', 'MINUTOS', 'TIPO_PERDIDA']
for col in cols_criticas:
    n = df[col].isnull().sum()
    if n > 0:
        pct = n / len(df) * 100
        print(f"CAVEAT: {col} — {n} nulos ({pct:.1f}%)")

print(f"Shape limpio: {len(df):,} filas x {df.shape[1]} columnas")
```

### Paso 3 — Calculos del analisis

Ejecutar los calculos definidos en el plan. Usar `stats` (totales) para KPIs; `muestra_top20` solo para tabla de detalle.

```python
# Stats generales (siempre desde el total del dataframe — nunca desde muestra)
total_registros = len(df)
total_minutos = df['MINUTOS'].sum()
total_horas = total_minutos / 60

# Agrupaciones
por_equipo = df.groupby('EQUIPO')['MINUTOS'].sum().sort_values(ascending=False)
por_tipo = df.groupby('TIPO_PERDIDA')['MINUTOS'].sum().sort_values(ascending=False)
por_turno = df.groupby('TURNO')['MINUTOS'].sum()
por_linea = df.groupby('LINEA')['MINUTOS'].sum()

# Evolucion temporal (semanal)
if pd.api.types.is_datetime64_any_dtype(df['FECHA']):
    evolucion = df.resample('W', on='FECHA')['MINUTOS'].sum()

# KPIs para cards
top_equipo = por_equipo.index[0]
top_equipo_min = por_equipo.iloc[0]
top_tipo = por_tipo.index[0]
pct_top_tipo = por_tipo.iloc[0] / total_minutos * 100

# Preparar datos para Chart.js (JSON serializable)
chart_equipos = {
    'labels': por_equipo.head(10).index.tolist(),
    'data': [round(v, 1) for v in por_equipo.head(10).values.tolist()]
}
chart_tipos = {
    'labels': por_tipo.index.tolist(),
    'data': [round(v, 1) for v in por_tipo.values.tolist()]
}

# Muestra para tabla de detalle (top-20 ordenado por impacto)
muestra_tabla = df.nlargest(20, 'MINUTOS')[['FECHA', 'EQUIPO', 'LINEA', 'TURNO', 'TIPO_PERDIDA', 'MINUTOS']].copy()
muestra_tabla['FECHA'] = muestra_tabla['FECHA'].dt.strftime('%d/%m/%Y')
```

### Paso 4 — Formateo numerico chileno

```python
def fmt_cl(valor, decimales=1):
    """Formatea numero en convencion chilena: punto miles, coma decimal."""
    if pd.isna(valor):
        return '—'
    partes = f"{valor:,.{decimales}f}".split('.')
    entero = partes[0].replace(',', '.')
    decimal = partes[1] if len(partes) > 1 else ''
    return f"{entero},{decimal}" if decimal else entero

# Uso: fmt_cl(1234567.5) → '1.234.567,5'
# Uso: fmt_cl(87.3) → '87,3'
```

### Paso 5 — Construccion del dashboard HTML

El HTML es un unico archivo standalone. Sin CDN externo. Chart.js embebido via `<script>` inline o desde una copia local.

```python
# Serializar datos para el HTML
import json

datos_js = json.dumps({
    'total': total_registros,
    'equipos': chart_equipos,
    'tipos': chart_tipos,
    'turno': {'labels': por_turno.index.tolist(), 'data': por_turno.values.tolist()},
    'tabla': muestra_tabla.to_dict(orient='records')
}, ensure_ascii=False)

# Generar filas de la tabla
filas_html = ''
for _, row in muestra_tabla.iterrows():
    badge = 'badge-ok' if row['MINUTOS'] < 60 else 'badge-alerta'
    filas_html += f"""
    <tr>
      <td>{row['FECHA']}</td>
      <td>{row['EQUIPO']}</td>
      <td>{row['LINEA']}</td>
      <td>{row['TURNO']}</td>
      <td><span class="badge {badge}">{row['TIPO_PERDIDA']}</span></td>
      <td class="text-right">{fmt_cl(row['MINUTOS'])}</td>
    </tr>"""
```

#### Sistema de diseno Arauco (HTML)

```html
<style>
  /* Paleta Arauco */
  :root {
    --arauco-cafe:    #696158;
    --arauco-amarillo:#BFB800;
    --arauco-naranja: #EA7600;
    --arauco-gris:    #EDEAE6;
    --arauco-blanco:  #FFFFFF;
    --arauco-texto:   #2C2A28;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Lato', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         background: #F5F4F2; color: var(--arauco-texto); font-size: 14px; }

  /* Header */
  .header { background: var(--arauco-cafe); color: #fff; padding: 20px 32px; }
  .header h1 { font-size: 1.4rem; font-weight: 700; letter-spacing: 0.5px; }
  .header .subtitulo { font-size: 0.85rem; opacity: 0.8; margin-top: 4px; }

  /* KPI cards */
  .grid { display: grid; gap: 16px; padding: 24px 32px; }
  .grid-4 { grid-template-columns: repeat(4, 1fr); }
  .kpi-card { background: #fff; border-radius: 8px; padding: 20px;
              box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
  .kpi-valor { font-size: 2rem; font-weight: 900; line-height: 1; }
  .kpi-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.8px;
               color: #888; margin-top: 6px; }
  .kpi-change { font-size: 0.8rem; margin-top: 8px; }
  .kpi-change.positive { color: #2E7D32; }
  .kpi-change.negative { color: #C62828; }
  .kpi-change.neutral  { color: #888; }

  /* Secciones */
  .section { padding: 0 32px 24px; }
  .section-title { font-size: 1rem; font-weight: 700; color: var(--arauco-cafe);
                   border-left: 4px solid var(--arauco-amarillo);
                   padding-left: 12px; margin-bottom: 16px; }

  /* Filtros */
  .filtros-bar { background: #fff; padding: 16px 32px; border-bottom: 1px solid #ddd;
                 display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
  .filtros-bar select { padding: 6px 10px; border: 1px solid #ccc; border-radius: 4px;
                        font-size: 13px; min-width: 140px; }
  .btn-limpiar { background: var(--arauco-naranja); color: #fff; border: none;
                 padding: 6px 14px; border-radius: 4px; cursor: pointer; font-size: 13px; }
  .btn-limpiar:hover { background: #c96500; }
  .registro-count { font-size: 12px; color: #666; margin-left: auto; }

  /* Graficos */
  .charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px;
                 padding: 0 32px 24px; }
  .chart-card { background: #fff; border-radius: 8px; padding: 20px;
                box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
  .chart-titulo { font-size: 0.85rem; font-weight: 600; margin-bottom: 12px;
                  color: var(--arauco-texto); }

  /* Tabla */
  .tabla-container { padding: 0 32px 32px; overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px;
          overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
  thead th { background: var(--arauco-cafe); color: #fff; padding: 10px 12px;
             text-align: left; font-size: 12px; font-weight: 600; white-space: nowrap; }
  tbody tr:nth-child(even) { background: var(--arauco-gris); }
  tbody td { padding: 8px 12px; font-size: 13px; border-bottom: 1px solid #E8E5E0; }
  tbody tr:hover { background: #E0DDD8; }
  td.text-right { text-align: right; font-variant-numeric: tabular-nums; }

  /* Badges */
  .badge { padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; }
  .badge-ok     { background: #E8F5E9; color: #2E7D32; }
  .badge-alerta { background: #FFF3E0; color: #E65100; }
  .badge-null   { background: #F5F5F5; color: #9E9E9E; }

  /* Caveat */
  .caveat { background: #FFF8E1; border-left: 3px solid var(--arauco-amarillo);
            padding: 10px 16px; margin: 0 32px 16px; font-size: 12px; color: #5D4037; }

  @media (max-width: 768px) {
    .grid-4 { grid-template-columns: 1fr 1fr; }
    .charts-grid { grid-template-columns: 1fr; }
  }
</style>
```

#### Filtros 100% dinamicos (JavaScript)

```javascript
// Datos embebidos desde Python
const DATOS = /* DATOS_JSON_AQUI */;

// Estado de filtros
let filtros = { linea: 'Todos', turno: 'Todos', tipo: 'Todos' };

function aplicarFiltros() {
  let registros = DATOS.tabla;

  if (filtros.linea !== 'Todos') {
    registros = registros.filter(r => r.LINEA === filtros.linea);
  }
  if (filtros.turno !== 'Todos') {
    registros = registros.filter(r => r.TURNO === filtros.turno);
  }
  if (filtros.tipo !== 'Todos') {
    registros = registros.filter(r => r.TIPO_PERDIDA === filtros.tipo);
  }

  // Actualizar contador
  document.getElementById('registro-count').textContent =
    `Mostrando ${registros.length} de ${DATOS.total} registros totales`;

  // Actualizar tabla
  const tbody = document.querySelector('#tabla-detalle tbody');
  tbody.innerHTML = registros.map(r => `
    <tr>
      <td>${r.FECHA}</td>
      <td>${r.EQUIPO}</td>
      <td>${r.LINEA}</td>
      <td>${r.TURNO}</td>
      <td><span class="badge ${r.MINUTOS < 60 ? 'badge-ok' : 'badge-alerta'}">${r.TIPO_PERDIDA}</span></td>
      <td class="text-right">${formatCL(r.MINUTOS)}</td>
    </tr>`).join('');

  // Actualizar graficos con datos filtrados
  actualizarGraficos(registros);
}

function actualizarGraficos(registros) {
  // Reagrupar por equipo con filtro aplicado
  const porEquipo = {};
  registros.forEach(r => {
    porEquipo[r.EQUIPO] = (porEquipo[r.EQUIPO] || 0) + r.MINUTOS;
  });
  const equiposOrdenados = Object.entries(porEquipo)
    .sort((a, b) => b[1] - a[1]).slice(0, 10);

  chartEquipos.data.labels = equiposOrdenados.map(e => e[0]);
  chartEquipos.data.datasets[0].data = equiposOrdenados.map(e => e[1]);
  chartEquipos.update();

  // Reagrupar por tipo
  const porTipo = {};
  registros.forEach(r => {
    porTipo[r.TIPO_PERDIDA] = (porTipo[r.TIPO_PERDIDA] || 0) + r.MINUTOS;
  });
  const tipos = Object.entries(porTipo);
  chartTipos.data.labels = tipos.map(t => t[0]);
  chartTipos.data.datasets[0].data = tipos.map(t => t[1]);
  chartTipos.update();
}

function formatCL(n) {
  if (n === null || n === undefined) return '—';
  return new Intl.NumberFormat('es-CL', { minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(n);
}

// Inicializar Chart.js
let chartEquipos, chartTipos;
document.addEventListener('DOMContentLoaded', () => {
  // Chart 1: Bar horizontal — equipos
  chartEquipos = new Chart(document.getElementById('chart-equipos'), {
    type: 'bar',
    data: {
      labels: DATOS.equipos.labels,
      datasets: [{
        label: 'Minutos perdidos',
        data: DATOS.equipos.data,
        backgroundColor: '#696158',
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { x: { grid: { color: '#eee' } } }
    }
  });

  // Chart 2: Doughnut — tipos de perdida
  chartTipos = new Chart(document.getElementById('chart-tipos'), {
    type: 'doughnut',
    data: {
      labels: DATOS.tipos.labels,
      datasets: [{
        data: DATOS.tipos.data,
        backgroundColor: ['#696158','#BFB800','#EA7600','#A0522D','#888','#CCC']
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'right', labels: { font: { size: 11 } } } }
    }
  });

  aplicarFiltros();
});

// Eventos de filtros
document.querySelectorAll('.filtro-select').forEach(sel => {
  sel.addEventListener('change', function() {
    filtros[this.dataset.filtro] = this.value;
    aplicarFiltros();
  });
});

document.getElementById('btn-limpiar').addEventListener('click', () => {
  document.querySelectorAll('.filtro-select').forEach(s => s.value = 'Todos');
  filtros = { linea: 'Todos', turno: 'Todos', tipo: 'Todos' };
  aplicarFiltros();
});
```

### Paso 6 — Guardar el archivo HTML

```python
from datetime import date

nombre = f"datos/{date.today().strftime('%Y-%m-%d')}_reporte-[descripcion].html"
with open(nombre, 'w', encoding='utf-8') as f:
    f.write(html_completo)
print(f"Guardado: {nombre}")
```

## Restricciones

- Chart.js debe estar embebido en el HTML (copiar desde `node_modules` local o inline desde CDN solo si se descarga primero). Sin CDN en vivo.
- `muestra_top20` / `muestra_tabla` solo para tabla de detalle. KPIs y graficos siempre desde el total del dataframe.
- Indicar en la seccion caveat del HTML: "Tabla de detalle muestra top-20 de N registros totales. KPIs y graficos incluyen la totalidad."
- Filtros dinamicos: cambiar un `<select>` debe actualizar la tabla Y llamar `chart.update()` en todos los graficos.
- Formato numerico chileno en todo el HTML: `Intl.NumberFormat('es-CL')` en JavaScript; `fmt_cl()` en Python.
- No usar `f-string` con llaves en templates HTML — escapar con `{{ }}` o construir el HTML en partes concatenadas para evitar conflictos con format().
- No inventar cifras: si una columna no existe en el archivo, no calcular el KPI ni mostrar la card.
- Si el build falla en alguna columna del plan, registrar el error y continuar con las columnas restantes. No abortar el build completo por un campo faltante.
- Archivos de salida: solo en `datos/`. Nunca sobreescribir un archivo existente sin agregar la fecha al nombre.
