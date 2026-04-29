# Skill: review — Verificacion de calidad analitica y alineacion con el negocio

> **Agente:** DA — Analisis de Datos

## Proposito

Confirmar que el analisis responde la pregunta del spec, que las cifras se interpretan correctamente en contexto forestal (ha, m³, OEE, turnos, SGL), y que no hay cifras inventadas ni conclusiones que excedan lo que los datos permiten afirmar. Produce una habilitacion: HABILITADO, HABILITADO CON CONDICIONES o NO HABILITADO.

## Cuando usar

- Test emitio veredicto VALIDADO o VALIDADO CON OBSERVACIONES (condiciones resueltas)
- El analisis sera presentado a la Subgerencia MC, jefes de area o agentes IA/EO
- El reporte contiene KPIs operacionales que impactaran decisiones de mejora continua

**Prerequisito:** Checklist de test completado con veredicto VALIDADO (o VALIDADO CON OBSERVACIONES con fallas menores documentadas). El spec aprobado debe estar disponible para verificar alineacion.

## Protocolo

### Paso 1 — Verificar alineacion con la pregunta del spec

Leer el spec y verificar que cada KPI card y grafico del dashboard responde directamente a la pregunta formulada.

Tabla de alineacion:

| Pregunta del spec | Elemento del dashboard | Responde la pregunta | Observacion |
|---|---|---|---|
| Ej: "calcular minutos perdidos por equipo" | Grafico bar horizontal equipos + card top equipo | SI / NO / PARCIAL | |
| Ej: "identificar turno con mayor concentracion" | Grafico pie turnos + filtro turno | SI / NO / PARCIAL | |

Si algun elemento del dashboard no corresponde a ninguna pregunta del spec, marcarlo como "elemento no solicitado" — puede quedar si agrega valor, pero debe documentarse.

Si una pregunta del spec no tiene elemento en el dashboard, es una brecha critica: NO HABILITADO hasta que se corrija en build.

### Paso 2 — Interpretar cifras en contexto forestal

Cada metrica debe interpretarse con sus unidades y magnitudes tipicas del sector. No aceptar cifras que sean fisicamente imposibles o que contradigan el conocimiento operacional.

| Metrica | Rango tipico Arauco | Alerta si |
|---|---|---|
| OEE por linea de celulosa | 75%-92% | < 50% o > 98% sin justificacion |
| Minutos perdidos por turno (8 h) | 0-480 min | > 480 min (mas que el turno completo) |
| Hectareas cosechadas por faena (mensual) | 20-500 ha | > 2.000 ha sin aclaracion de periodo |
| Produccion celulosa (ton/dia) | 1.000-4.000 ton | > 5.000 ton sin validacion de planta |
| Horas de mantenimiento correctivo (semana) | 0-200 h | > 480 h (mas de 3 turnos) |
| Rendimiento cosecha (m³/ha) | 80-350 m³/ha | < 20 o > 500 sin nota explicativa |
| Paradas no planificadas por semana | 1-30 eventos | > 100 eventos sin aclaracion de granularidad |

Si una cifra esta fuera del rango tipico, no rechazarla automaticamente. Verificar si:
- El periodo es diferente al esperado (acumulado anual vs. mensual)
- La unidad es diferente (ton vs. m³; minutos vs. horas)
- El archivo contiene datos de multiples plantas o lineas acumuladas

Documentar la verificacion. Si no se puede confirmar, marcar como caveat adicional.

### Paso 3 — Verificar que no hay cifras inventadas

```python
import pandas as pd

# Recalcular los KPIs principales desde el archivo fuente
df = pd.read_excel('datos/archivo.xlsx', sheet_name='NombreHoja')

kpis_recalculados = {
    'total_minutos': round(df['MINUTOS'].sum(), 1),
    'promedio_oee': round(df['OEE'].mean() * 100, 1) if 'OEE' in df.columns else 'N/A',
    'top_equipo_minutos': round(df.groupby('EQUIPO')['MINUTOS'].sum().max(), 1),
    'periodos_cubiertos': f"{df['FECHA'].min()} a {df['FECHA'].max()}"
}

print("KPIs recalculados desde fuente:")
for k, v in kpis_recalculados.items():
    print(f"  {k}: {v}")

# Comparar con los valores del HTML (extraidos manualmente o via BeautifulSoup)
# Si hay discrepancia > 0.5%, es una cifra que no viene del archivo
```

Regla: cualquier numero que aparece en el HTML y no puede ser recalculado desde el archivo fuente es una cifra inventada. Si se detecta, el review es NO HABILITADO hasta correccion.

### Paso 4 — Verificar que las conclusiones no exceden los datos

Las conclusiones del texto resumen (si existe) deben cumplir:
- No afirmar causalidad desde correlacion: "el equipo X tiene mas fallas porque..." requiere datos adicionales
- No proyectar tendencias sin datos suficientes: al menos 4 periodos para afirmar tendencia
- No comparar con benchmarks externos sin citar la fuente del benchmark
- No generalizar de datos parciales: si los datos son de una sola linea, las conclusiones no aplican a toda la planta

Ejemplo de conclusion invalida:
> "El OEE mejorara el proximo trimestre si se mantiene la tendencia actual."
(Proyeccion sin datos futuros — no esta en los datos.)

Ejemplo de conclusion valida:
> "En las ultimas 4 semanas, el OEE de Linea 3 aumento 2,3 pp (de 78,4% a 80,7%), lo que sugiere una mejora en disponibilidad. Se requiere seguimiento de al menos 4 semanas adicionales para confirmar la tendencia."

### Paso 5 — Verificar caveats completos

| Caveat | Estado en el reporte |
|---|---|
| N total de registros analizados | presente / ausente |
| Tabla detalle muestra top-N de M totales | presente / ausente |
| Columnas con nulos significativos y su impacto | presente / ausente |
| Periodo exacto cubierto por los datos | presente / ausente |
| Supuestos de limpieza aplicados | presente / ausente |
| Fuente: archivo, hoja, sistema origen | presente / ausente |

Si algun caveat esta ausente, el review es HABILITADO CON CONDICIONES — corregir antes de ship.

### Paso 6 — Verificar terminologia operacional Arauco

El reporte usa la terminologia correcta del negocio. Verificar:

| Termino incorrecto | Termino correcto en Arauco |
|---|---|
| "falla de maquina" | "parada no planificada" o "evento correctivo" |
| "trabajadores" | "operadores" (planta) o "operarios forestales" (terreno) |
| "fabrica" | "planta" o "linea de produccion" |
| "eficiencia de la maquina" | "OEE" o "disponibilidad mecanica" segun la formula usada |
| "hectareas trabajadas" | "hectareas cosechadas" o "hectareas intervenidas" segun la operacion |
| "perdida de tiempo" | "perdida operacional" o "tiempo de parada" |
| "turno 1/2/3" | "turno manana / tarde / noche" |

Adicionalmente, verificar las restricciones de lenguaje del contexto chileno (ver CLAUDE.md global): evitar terminos con connotaciones regionales inadecuadas.

### Paso 7 — Emitir habilitacion

| Habilitacion | Criterio |
|---|---|
| HABILITADO | Todas las verificaciones pasan. Reporte listo para ship. |
| HABILITADO CON CONDICIONES | Fallas menores: caveat ausente, terminologia, elementos extra no solicitados. Corregir antes de ship. |
| NO HABILITADO | Cifra inventada, KPI no alineado con spec, conclusion que excede los datos, cifra fuera de rango sin justificacion. Volver a build. |

## Plantilla de Informe Review DA

```markdown
# Review DA — [Nombre del reporte]

**Fecha:** YYYY-MM-DD
**Archivo revisado:** datos/YYYY-MM-DD_reporte-descripcion.html
**Referencia spec:** datos/YYYY-MM-DD_spec-[area]-[tipo].md
**Test previo:** VALIDADO / VALIDADO CON OBSERVACIONES
**Habilitacion:** HABILITADO | HABILITADO CON CONDICIONES | NO HABILITADO

---

## Alineacion con el spec

| Pregunta del spec | Elemento en dashboard | Responde | Observacion |
|---|---|---|---|

Brechas criticas (preguntas sin elemento en el dashboard):
- [lista o "ninguna"]

Elementos extra no solicitados:
- [lista o "ninguno"]

---

## Coherencia de cifras en contexto forestal

| Metrica | Valor en reporte | Rango tipico | Estado | Verificacion realizada |
|---|---|---|---|---|

---

## Caveats

| Caveat | Presente | Observacion |
|---|---|---|
| N total registros | SI / NO | |
| Top-N de M totales (tabla) | SI / NO | |
| Nulos significativos | SI / NO / N/A | |
| Periodo cubierto | SI / NO | |
| Supuestos de limpieza | SI / NO / N/A | |
| Fuente citada | SI / NO | |

---

## Conclusiones del texto resumen

- [ ] No afirman causalidad sin evidencia
- [ ] No proyectan tendencias con menos de 4 periodos
- [ ] No usan benchmarks sin fuente
- [ ] No generalizan datos parciales al total de la planta

---

## Terminologia

- [ ] Terminologia Arauco correcta (OEE, parada, operador, linea)
- [ ] Sin terminos con connotaciones inadecuadas en contexto chileno

---

## Condiciones para habilitar (si aplica)

| # | Condicion | Urgencia | Accion requerida |
|---|---|---|---|
| 1 | [descripcion] | CRITICA / MENOR | build / edicion directa |

---

## Habilitacion

**Veredicto:** HABILITADO | HABILITADO CON CONDICIONES | NO HABILITADO

**Fundamento:**
- [punto 1]
- [punto 2]
```

## Restricciones

- No emitir HABILITADO si hay cualquier cifra que no puede ser recalculada desde el archivo fuente
- No emitir HABILITADO si una pregunta del spec no tiene elemento en el dashboard
- HABILITADO CON CONDICIONES solo para fallas de presentacion o terminologia — no para errores de datos o alineacion con el spec
- Si la cifra esta fuera del rango tipico pero es verificable desde el archivo, documentar la verificacion y habilitar con nota — no rechazar sin verificar
- No agregar interpretaciones de negocio que no esten soportadas por los datos del archivo
- El review no modifica el HTML directamente — documenta las condiciones y el build hace las correcciones
