# Skill: ship — Cierre, Estandarización y Entrega Formal

## Propósito

Cerrar formalmente la iniciativa de mejora: estandarizar el nuevo proceso como la forma oficial de trabajo, transferir el conocimiento al área operacional, documentar lecciones aprendidas y registrar los resultados en el SGL. Asegura que la mejora no se revierta con el tiempo y que el conocimiento generado quede disponible para futuras iniciativas.

---

## Cuándo usar este skill

- El skill `review` fue completado con decisión "Aprobar cierre y estandarizar"
- Todos los ajustes críticos identificados en el review fueron resueltos
- Se necesita hacer el hand-off formal al área operacional
- Se requiere el cierre del proyecto ante el sponsor y la gerencia

**Prerequisito:** review aprobado sin hallazgos críticos pendientes.

---

## Protocolo de ejecución

### Paso 1 — Verificar condiciones de cierre
Confirmar que están resueltos:
- [ ] Todos los hallazgos críticos del review cerrados
- [ ] KPIs de éxito validados con datos reales (no solo del piloto)
- [ ] Proceso TO-BE documentado y probado en todos los turnos/áreas involucrados

### Paso 2 — Estandarizar el nuevo proceso
Producir o actualizar:
- **BPMN TO-BE final**: versión definitiva del proceso aprobado, con todas las correcciones post-review
- **Procedimiento operacional estándar (POE)**: documento de trabajo para operadores y supervisores
- **Diccionario de datos**: definición formal de todos los KPIs del proceso (D.A.M.A.)
- **Plantillas actualizadas**: formularios, checklists, dashboards en versión final

Nombrar los estándares como versión oficial:
```
datos/plantillas/STD-[codigo]-[nombre-proceso]-v1.0.md
datos/plantillas/STD-[codigo]-kpi-[nombre]-v1.0.xlsx
```

### Paso 3 — Registrar en SGL (si aplica)
- Cerrar las oportunidades de mejora asociadas en el SGL
- Registrar el resultado como mejora estandarizada
- Actualizar o crear el seguimiento de KPIs en la plataforma

### Paso 4 — Transferir al área operacional
Actividades de hand-off:
- Sesión de traspaso con supervisores y referentes operacionales
- Entrega física/digital de los estándares (POE, BPMN, dashboards)
- Capacitación o entrenamiento si el proceso cambió significativamente
- Designar responsable de seguimiento de KPIs post-cierre

### Paso 5 — Documentar lecciones aprendidas
Registrar para el sistema de mejora continua:
- ¿Qué funcionó muy bien y debe replicarse?
- ¿Qué fue difícil y cómo se resolvió?
- ¿Qué haría diferente si comenzara de nuevo?
- ¿Qué oportunidades adicionales se identificaron en el proceso?

### Paso 6 — Cerrar el proyecto formalmente
- Informe ejecutivo de cierre para el sponsor
- Acta de cierre con firmas (si corresponde)
- Archivo de todo el proyecto en `datos/` con convención de nombrado

### Paso 7 — Entregar
```
datos/YYYY-MM-DD_ship-cierre-[nombre-iniciativa].md
datos/plantillas/STD-[codigo]-[nombre]-v1.0.[ext]
datos/YYYY-MM-DD_lecciones-aprendidas-[nombre-iniciativa].md
```

Reportar al orquestador con formato estándar:
```
ENTREGA EO:
Archivo(s): datos/YYYY-MM-DD_ship-cierre-[nombre].md
Hallazgos clave: [3 resultados operacionales cuantificados]
Causa raíz identificada: [confirmación de hipótesis original]
Plan de acción: [seguimiento post-cierre: responsable, KPI a monitorear, frecuencia]
```

---

## Plantilla de cierre y estandarización

```markdown
# Cierre de Iniciativa de Mejora — [Nombre]
**Fecha de cierre:** YYYY-MM-DD
**Área:** Excelencia Operacional
**PM responsable:** [Nombre]
**Sponsor:** [Cargo + Nombre]

---

## 1. Resumen ejecutivo
[3-5 líneas: qué se mejoró, cuánto mejoró, quién lo usa ahora]

---

## 2. Resultados finales vs. objetivos

| KPI | Línea base | Meta comprometida | Resultado final | % logro |
|---|---|---|---|---|

**Impacto económico estimado:** [CLP/año o equivalente operacional]

---

## 3. Estándares generados

| Documento | Archivo | Versión | Responsable de mantenimiento |
|---|---|---|---|
| BPMN TO-BE | datos/... | v1.0 | |
| Procedimiento operacional | datos/plantillas/STD-... | v1.0 | |
| Diccionario de KPIs | datos/plantillas/STD-... | v1.0 | |

---

## 4. Registro en SGL
- [ ] Oportunidad de mejora cerrada en SGL (ID: ___)
- [ ] KPIs ingresados para seguimiento continuo
- [ ] Pérdida original marcada como resuelta

---

## 5. Hand-off al área operacional

| Actividad | Fecha | Participantes | Confirmación |
|---|---|---|---|
| Sesión de traspaso | | | [ ] Realizada |
| Entrega de estándares | | | [ ] Entregados |
| Capacitación | | | [ ] Completada |
| Responsable KPI designado | | [Nombre + cargo] | [ ] Confirmado |

---

## 6. Lecciones aprendidas

### ¿Qué funcionó muy bien?
1.
2.

### ¿Qué fue difícil y cómo se resolvió?
1.
2.

### ¿Qué haríamos diferente?
1.
2.

### Oportunidades adicionales identificadas (para próximas iniciativas)
1.
2.

---

## 7. Plan de seguimiento post-cierre

| KPI a monitorear | Frecuencia | Responsable | Alerta si baja de |
|---|---|---|---|

**Revisión de sostenibilidad:** [Fecha de revisión a 90 días: YYYY-MM-DD]

---

## 8. Acta de cierre
| Rol | Nombre | Firma / Confirmación |
|---|---|---|
| PM Proyecto | | |
| Jefe EO | | |
| Sponsor | | |
| Referente Operacional | | |

**Estado del proyecto:** CERRADO ✓
```

---

## Restricciones de este skill

- No se puede cerrar el proyecto sin hand-off formal al área operacional: la mejora es de ellos, no de EO
- El responsable de seguimiento de KPIs post-cierre debe ser designado explícitamente (cargo + nombre)
- Las lecciones aprendidas deben registrarse aunque el proyecto haya sido exitoso
- La revisión de sostenibilidad a 90 días es obligatoria: EO valida que la mejora no se revirtió
- Un proyecto cerrado sin estándares escritos no está realmente cerrado
