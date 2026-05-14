# Weekly Retro — Retrospectiva Semanal Multi-Agente

Skill de retrospectiva semanal profunda. Usa claude-mem + razonamiento extendido (ultrathink)
para identificar patrones de friccion y proponer cambios arquitecturales concretos.

**Invocar:** `/weekly-retro` o "ejecuta retrospectiva semanal"

---

## Paso 1 — Recopilar observaciones de la semana

Usar claude-mem para obtener el contexto de la semana pasada:

```
get_observations con timeline de los ultimos 7 dias
```

Si no hay observaciones recientes, usar `smart_search` con terminos:
- "fix", "bug", "error", "fallo" → friccion tecnica
- "aprobacion", "autonomia", "auto-commit" → friccion de proceso
- "push", "commit", "git" → friccion de flujo git
- "skill", "agente", "CLAUDE.md" → friccion de arquitectura

---

## Paso 2 — Analisis de patrones (ultrathink)

Con las observaciones recopiladas, razonar en profundidad sobre:

### Patrones de friccion a detectar
1. **Friccion de proceso**: momentos donde la autonomia de Claude choco con la necesidad de aprobacion humana
2. **Friccion de flujo git**: commits sin push, push olvidado, tags faltantes en releases
3. **Friccion arquitectural**: skills en scope equivocado, CLAUDE.md desincronizados, agentes invocando skills ajenos
4. **Friccion de iteracion**: ciclos repetidos de ajuste sobre el mismo problema (ej: filtros de resumen semanal ajustados 3+ veces)
5. **Friccion de contexto**: malentendidos sobre alcance de tareas que requirieron aclaracion

### Preguntas a responder
- Que tipo de friccion ocurrio mas veces?
- Cual tuvo mayor impacto (tiempo perdido, trabajo rehecho)?
- Que patron se podria eliminar con un cambio de una sola vez?

---

## Paso 3 — Proponer 3 cambios arquitecturales concretos

Para cada cambio propuesto:

```
### Cambio N: [Nombre corto]
**Problema detectado:** [descripcion del patron de friccion]
**Frecuencia:** [veces observada en la semana]
**Cambio propuesto:** [descripcion precisa — archivo, seccion, regla]
**Archivo a modificar:** [ruta exacta]
**PR sugerido:** [titulo del PR y descripcion de los cambios]
**Impacto esperado:** [que friccion elimina]
```

Criterios de seleccion:
- Preferir cambios en CLAUDE.md sobre cambios en codigo (mas durables)
- Preferir cambios que eliminen friccion recurrente sobre friccion puntual
- Los 3 cambios deben ser independientes entre si (no hay que hacer A para hacer B)

---

## Paso 4 — Reporte final

Formato de salida:

```
## Retrospectiva Semanal — [fecha]

### Resumen ejecutivo
[2-3 oraciones: que semana fue, patron dominante]

### Observaciones analizadas: N
### Patrones de friccion identificados: N

---

### Cambio 1: ...
### Cambio 2: ...
### Cambio 3: ...

---

### Proxima semana
[1 accion concreta de seguimiento]
```

---

## Notas

- NO aplicar cambios automaticamente. Reportar y esperar aprobacion.
- Si hay menos de 3 observaciones de la semana, ampliar ventana a 14 dias.
- Fecha de hoy disponible en el contexto del sistema (`currentDate`).
- Patrones conocidos ya documentados en CLAUDE.md no necesitan ser re-propuestos.
