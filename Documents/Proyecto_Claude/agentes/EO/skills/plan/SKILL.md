# Skill: plan — Planificación de Iniciativa de Mejora

## Propósito

Transformar la especificación validada en un plan de proyecto ejecutable. Produce el charter del proyecto, la EDT (WBS), el cronograma con hitos, la matriz de riesgos y el plan de recursos. Sigue el framework PMBoK adaptado a iniciativas de excelencia operacional en contexto forestal.

---

## Cuándo usar este skill

- Se completa exitosamente el skill `spec` y la especificación está validada
- El orquestador solicita planificar una iniciativa de mejora con charter formal
- Se necesita gestionar recursos, plazos y riesgos de un proyecto de EO
- Se requiere aprobación de gerencia antes de iniciar ejecución

**Prerequisito:** documento `spec` aprobado con KPIs de éxito definidos.

---

## Protocolo de ejecución

### Paso 1 — Leer la especificación
Revisar el documento `datos/YYYY-MM-DD_spec-[iniciativa].md` y extraer:
- Problema, brecha y KPIs de éxito
- Stakeholders y sus roles
- Alcance incluido y excluido
- Restricciones y supuestos

### Paso 2 — Definir el charter del proyecto
Estructura mínima del charter:
- Nombre del proyecto, área responsable, fecha
- Objetivo SMART alineado al problema spec
- Entregables principales
- Presupuesto estimado (si aplica)
- Sponsor y PM responsable

### Paso 3 — Construir la EDT (WBS)
Descomponer en fases y paquetes de trabajo:
```
1. Diagnóstico / GEMBA
2. Análisis de causa raíz
3. Diseño de solución (BPMN TO-BE, KPIs, herramientas)
4. Piloto / prueba en terreno
5. Validación de resultados
6. Estandarización y cierre
```

### Paso 4 — Definir cronograma e hitos
Para cada paquete de trabajo:
- Fechas de inicio y fin
- Responsable
- Hito de control (entregable verificable)
- Dependencias entre tareas

### Paso 5 — Evaluar riesgos
Matriz probabilidad × impacto para riesgos principales:

| Riesgo | Probabilidad (A/M/B) | Impacto (A/M/B) | Nivel | Plan de respuesta |
|---|---|---|---|---|

### Paso 6 — Entregar plan
Guardar como:
```
datos/YYYY-MM-DD_plan-[nombre-iniciativa].md
datos/YYYY-MM-DD_charter-[nombre-iniciativa].md
```

---

## Plantilla de plan de proyecto

```markdown
# Plan de Proyecto — Iniciativa de Mejora
**Fecha:** YYYY-MM-DD
**Proyecto:** [Nombre]
**Área:** Excelencia Operacional
**PM responsable:** [Nombre]
**Sponsor:** [Cargo + Nombre]

---

## Charter del proyecto
| Campo | Detalle |
|---|---|
| **Objetivo** | [SMART: específico, medible, alcanzable, relevante, con plazo] |
| **Justificación** | [Brecha operacional de la spec + impacto económico] |
| **Entregables** | [Lista de productos del proyecto] |
| **Presupuesto** | [CLP estimado o "sin costo directo"] |
| **Fecha límite** | [YYYY-MM-DD] |
| **Sponsor aprobación** | [ ] Pendiente / [x] Aprobado |

---

## EDT — Estructura de Desglose del Trabajo

### Fase 1: Diagnóstico
| Tarea | Responsable | Inicio | Fin | Hito |
|---|---|---|---|---|

### Fase 2: Análisis
| Tarea | Responsable | Inicio | Fin | Hito |
|---|---|---|---|---|

### Fase 3: Diseño de solución
| Tarea | Responsable | Inicio | Fin | Hito |
|---|---|---|---|---|

### Fase 4: Piloto
| Tarea | Responsable | Inicio | Fin | Hito |
|---|---|---|---|---|

### Fase 5: Validación
| Tarea | Responsable | Inicio | Fin | Hito |
|---|---|---|---|---|

### Fase 6: Estandarización y cierre
| Tarea | Responsable | Inicio | Fin | Hito |
|---|---|---|---|---|

---

## Cronograma de hitos

| Hito | Fecha | Criterio de cumplimiento |
|---|---|---|
| Especificación aprobada | | |
| GEMBA realizado | | |
| Causa raíz validada | | |
| Solución diseñada (BPMN TO-BE) | | |
| Piloto completado | | |
| KPI meta alcanzada | | |
| Proyecto cerrado y estandarizado | | |

---

## Matriz de riesgos

| Riesgo | P | I | Nivel | Respuesta | Responsable |
|---|---|---|---|---|---|
| Indisponibilidad de datos en SGL | M | A | Alto | Validar con TI acceso previo al inicio | PM |
| Resistencia de operadores al cambio | A | M | Alto | Plan comunicacional + taller Kaizen | EO |
| Parada no planificada de equipos | M | M | Medio | Buffer de tiempo en cronograma | PM |

---

## Plan de comunicaciones

| Audiencia | Frecuencia | Formato | Responsable |
|---|---|---|---|
| Sponsor | Mensual | Informe ejecutivo 1 página | PM |
| Equipo EO | Semanal | Reunión de avance 30 min | PM |
| Operadores | Por hito | Taller o charla en terreno | Facilitador |

---

## Criterio de inicio de ejecución (build)
- [ ] Charter aprobado por sponsor
- [ ] Recursos humanos confirmados
- [ ] Acceso a sistemas (SGL, SAP, Historian) verificado
- [ ] Riesgos críticos con plan de respuesta definido
```

---

## Restricciones de este skill

- No se puede iniciar ejecución (`build`) sin charter aprobado
- Los hitos deben tener criterio de cumplimiento verificable, no solo fecha
- La matriz de riesgos debe incluir al menos los riesgos de datos y resistencia al cambio
- El cronograma debe respetar disponibilidad de equipos en terreno (temporadas de cosecha, mantenciones programadas)
