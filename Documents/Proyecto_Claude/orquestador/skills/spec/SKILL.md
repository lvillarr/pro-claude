# Skill: spec — Especificación del Problema de Negocio (Orquestador)

## Propósito

Definir con precisión el problema de negocio antes de delegar a los agentes. Produce un documento de encuadre estratégico que alinea al equipo sobre qué se busca resolver, cuál es el impacto en el negocio forestal, qué agentes participan y en qué orden. Evita delegar trabajo mal especificado que genera iteraciones costosas.

---

## Cuándo usar este skill

- El usuario plantea una necesidad compleja que involucra a más de un agente
- Antes de toda delegación de una iniciativa nueva (mejora operacional, proyecto IA, integración digital)
- Cuando la solicitud es ambigua y hay múltiples interpretaciones válidas
- Para documentar el mandato antes de coordinar EO, IA y TD

**El orquestador no ejecuta: define el problema y delega.**

---

## Protocolo de ejecución

### Paso 1 — Encuadrar el problema de negocio (estilo McKinsey)
Antes de responder, articular explícitamente:
- ¿Cuál es el problema de negocio real (no la tarea pedida)?
- ¿Cuál es el impacto cuantificado si no se resuelve? (CLP, horas, %OEE, m³)
- ¿Qué hipótesis iniciales tengo sobre causa o solución?
- ¿Es urgente (operacional) o estratégico (transformacional)?

### Paso 2 — Definir el mandato con estructura MECE
```
Problema: [una frase, cuantificada]
Hipótesis: [qué creemos que es la causa o solución]
Impacto esperado: [si lo resolvemos, qué mejora y cuánto]
```

### Paso 3 — Identificar qué agentes participan y en qué orden

| Agente | Rol en esta iniciativa | Orden | Insumos que necesita | Entregable esperado |
|---|---|---|---|---|
| EO | | 1° / 2° / paralelo | | |
| IA | | | | |
| TD | | | | |

Decidir: ¿secuencial (output de uno alimenta al siguiente) o paralelo (trabajan con los mismos datos)?

### Paso 4 — Identificar datos disponibles
Listar con `list_dir datos/` qué archivos existen relevantes al problema:
- ¿Hay históricos en `arauco_mc.db`?
- ¿Hay reportes previos en `datos/`?
- ¿Qué datos faltan y quién los provee?

### Paso 5 — Definir entregable final para el usuario
- ¿Qué formato? (informe ejecutivo, dashboard, plan de acción, arquitectura)
- ¿Qué audiencia? (gerencia, equipo técnico, operadores)
- ¿Qué estructura? (situación → hallazgos → recomendaciones → próximos pasos)

### Paso 6 — Entregar
```
datos/YYYY-MM-DD_spec-orq-[nombre-iniciativa].md
```

---

## Plantilla de especificación del orquestador

```markdown
# Mandato de Iniciativa — [Nombre]
**Fecha:** YYYY-MM-DD | **Orquestador:** Subgerente Mejora Continua

---

## Problema de negocio
| | |
|---|---|
| **Situación** | [contexto actual cuantificado] |
| **Complicación** | [por qué es urgente o estratégico resolver esto ahora] |
| **Pregunta clave** | [qué debemos responder o lograr] |
| **Impacto estimado** | [CLP / horas / %OEE / m³ en juego] |

## Hipótesis de trabajo
[Qué creemos que es la causa o la solución. Los agentes validarán o refutarán esto.]

## Agentes y secuencia
| Agente | Tarea | Orden | Entregable |
|---|---|---|---|

## Datos disponibles
- [Archivo existente relevante]
- [Gap de datos: qué falta y quién lo provee]

## Entregable final para el usuario
**Formato:** [informe ejecutivo / dashboard / plan]
**Audiencia:** [gerencia / equipo técnico / operadores]
**Estructura:** situación → hallazgos → recomendaciones → próximos pasos

## Criterio de éxito del mandato
[¿Cómo sabe el orquestador que la iniciativa cumplió su objetivo?]
```

---

## Restricciones de este skill

- El orquestador no resuelve el problema: lo encuadra y lo delega con precisión
- No delegar sin definir primero el impacto de negocio: los agentes necesitan el "para qué"
- Si la solicitud es ambigua, hacer las preguntas de clarificación antes de spec — no asumir
- El mandato debe ser validado internamente antes de delegar: si el problema está mal definido, los agentes producen outputs correctos para la pregunta equivocada
