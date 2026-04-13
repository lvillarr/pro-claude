# Skill: review — Revisión de Soluciones de Transformación Digital

## Propósito

Evaluar de forma estructurada la calidad técnica, seguridad y mantenibilidad de la solución implementada antes del cierre. Combina revisión de código, validación de datos en producción y retroalimentación del equipo técnico y operacional. Identifica deudas técnicas y riesgos antes de estandarizar.

---

## Cuándo usar este skill

- El test fue completado con resultado APROBADO o APROBADO CON OBSERVACIONES
- Se necesita revisión formal de la arquitectura antes del cierre
- El orquestador solicita auditar una integración o pipeline existente

**Prerequisito:** reporte de test completado.

---

## Protocolo de ejecución

### Paso 1 — Revisar el ciclo completo
Leer en orden: `spec` → `plan` → `build-log` → `test-reporte`.
¿La solución entrega el MVP comprometido en la especificación?

### Paso 2 — Revisión de código y arquitectura

**Seguridad:**
- [ ] Sin credenciales hardcodeadas en el código
- [ ] Variables de entorno documentadas en README
- [ ] Logging no expone datos sensibles (tokens, contraseñas, PII)

**Calidad de código:**
- [ ] Docstrings en todas las funciones
- [ ] Manejo de errores explícito en puntos críticos
- [ ] Sin código muerto o experimentos sin limpiar

**Arquitectura:**
- [ ] El pipeline puede reprocesar un rango de fechas sin duplicar datos (idempotencia)
- [ ] La estrategia de retry es correcta (no genera loops infinitos)
- [ ] La estructura de archivos sigue la convención `datos/scripts/`

**Conectividad:**
- [ ] El modo offline está probado y documentado (si aplica)
- [ ] La queue de sincronización tiene límite de tamaño para evitar llenado de disco

### Paso 3 — Validar integridad de datos en producción
Después del período de test, verificar en datos reales:
```python
# ¿Los datos en destino coinciden con la fuente?
completitud = len(df_destino) / len(df_fuente)
print(f"Completitud: {completitud*100:.1f}%")

# ¿Hay duplicados en el destino?
duplicados = df_destino.duplicated(subset=["id_registro"]).sum()
print(f"Duplicados: {duplicados}")

# ¿Los campos numéricos están en rango esperado?
print(df_destino["horas_operacion"].describe())
```

### Paso 4 — Recoger retroalimentación
- **Equipo técnico TD/TI**: ¿el código es mantenible? ¿pueden operar esto sin el autor?
- **Equipo IA**: ¿los datos que llegan son los que necesitan para los modelos?
- **Equipo EO**: ¿los KPIs que se alimentan de esta integración son confiables?
- **Operadores o supervisores**: ¿ven la información que esperaban en el sistema destino?

### Paso 5 — Identificar ajustes
- **Críticos**: bug de datos, credencial expuesta, pipeline falla en producción
- **Importantes**: mejora de rendimiento, logging más detallado, documentación incompleta
- **Menores**: refactoring, convenciones de nombres, backlog

### Paso 6 — Entregar
```
datos/YYYY-MM-DD_review-td-[nombre-iniciativa].md
```

---

## Plantilla de review TD

```markdown
# Review — Iniciativa TD [Nombre]
**Fecha:** YYYY-MM-DD | **Revisado por:** [Nombre]

## Seguridad y calidad de código
| Criterio | Estado | Hallazgo |
|---|---|---|
| Sin credenciales hardcodeadas | OK / NOK | |
| Docstrings completos | OK / NOK | |
| Manejo de errores | OK / NOK | |
| Idempotencia del pipeline | OK / NOK | |

## Integridad de datos en producción
| Métrica | Resultado | Estado |
|---|---|---|
| Completitud (%) | | OK ≥ 98% |
| Duplicados | | OK = 0 |

## Retroalimentación del equipo
| Equipo | ¿Código mantenible? | ¿Datos confiables? | Comentario |
|---|---|---|---|

## Ajustes identificados
### Críticos
| Hallazgo | Acción | Responsable | Plazo |
|---|---|---|---|

## Decisión: Aprobar cierre / Requiere ajustes
```

---

## Restricciones de este skill

- No recomendar cierre si hay credenciales expuestas o bug de duplicación de datos
- La idempotencia es obligatoria: un pipeline que duplica datos en el segundo run es un problema crítico
- La retroalimentación del equipo IA es clave: si los datos no sirven para análisis, la integración no cumple su propósito
