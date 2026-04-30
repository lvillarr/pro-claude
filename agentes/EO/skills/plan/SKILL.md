# Skill: plan — EDT, cronograma, riesgos y hitos PMBoK

> **Agente:** EO — Excelencia Operacional

## Proposito

Traducir el spec aprobado en un plan ejecutable: EDT (WBS), cronograma con hitos verificables, recursos, dependencias y matriz de riesgos. Salida: documento que el orquestador puede monitorear y TD puede tomar para automatizar seguimiento.

## Cuando usar este skill

- Spec en estado APROBADO y tipo de solucion identificado
- Iniciativa con duracion mayor a 1 semana o con mas de un area involucrada
- Cuando el orquestador necesita cronograma para coordinar agentes en paralelo (EO + TD + IA)
- Rediseno de proceso que requiere piloto antes de estandarizar

**Prerequisito:** `agentes/EO/skills/spec/SKILL.md` ejecutado y archivo `datos/YYYY-MM-DD_spec-*.md` en estado APROBADO.

## Protocolo de ejecucion

### Paso 1 — Determinar tipo de proyecto

| Escala | Criterio | Marco |
|---|---|---|
| Micro (< 2 semanas) | 1 area, 1 equipo, causa raiz clara | A3 / PDCA directo |
| Pequeño (2-8 semanas) | 1-2 areas, piloto requerido | Kaizen estructurado |
| Mediano (2-6 meses) | Multiples areas, presupuesto, charter | PMBoK simplificado |
| Grande (> 6 meses) | Multisitio o transformacional | PMBoK completo |

### Paso 2 — Construir la EDT (WBS)

Descomponer en entregables, no en actividades. Niveles:

```
1. Proyecto [nombre]
   1.1 Inicio
       1.1.1 Spec aprobado
       1.1.2 Charter firmado (si aplica)
   1.2 Diagnostico
       1.2.1 GEMBA / recoleccion de datos
       1.2.2 Analisis causa raiz
       1.2.3 BPMN AS-IS validado
   1.3 Diseno
       1.3.1 BPMN TO-BE
       1.3.2 KPIs y metricas
       1.3.3 Plan de accion
   1.4 Piloto
       1.4.1 Implementacion piloto
       1.4.2 Validacion KPIs vs. linea base
       1.4.3 Checklist operadores
   1.5 Estandarizacion
       1.5.1 Procedimientos actualizados
       1.5.2 Registro SGL
       1.5.3 Cierre formal
```

### Paso 3 — Cronograma con hitos

Para cada entregable de la EDT, definir:
- Fecha inicio / fecha termino
- Responsable (cargo, no nombre propio)
- Hito verificable (criterio binario: logrado / no logrado)
- Dependencia (ID del entregable previo)

### Paso 4 — Recursos necesarios

| Recurso | Tipo | Dedicacion | Observacion |
|---|---|---|---|
| Jefe EO | Coordinacion | 20% | Revision de hitos |
| Operador turno | Terreno | 4h/semana | GEMBA y piloto |
| Analista IA | Datos | Segun carga | Si requiere historico SGL |
| TD | Automatizacion | Segun alcance | Si hay rediseno de flujo |

### Paso 5 — Matriz de riesgos PMBoK

Cada riesgo: descripcion, probabilidad (1-3), impacto (1-3), score (P x I), tratamiento.

Score >= 6: plan de contingencia obligatorio.

### Paso 6 — Guardar y reportar

```
datos/YYYY-MM-DD_plan-[area]-[tipo].md
```

Notificar al orquestador con hitos y fechas clave para coordinacion de agentes.

## Plantilla de Plan

```markdown
# Plan EO — [Nombre del Proyecto / Iniciativa]

**Fecha:** YYYY-MM-DD
**Spec de referencia:** datos/YYYY-MM-DD_spec-[area]-[tipo].md
**Responsable EO:** [cargo]
**Duracion estimada:** [N semanas]
**Estado:** BORRADOR | APROBADO | EN EJECUCION

---

## EDT (WBS)

| ID | Entregable | Responsable | Inicio | Termino | Dependencia | Hito verificable |
|---|---|---|---|---|---|---|
| 1.1.1 | Spec aprobado | Jefe EO | YYYY-MM-DD | YYYY-MM-DD | — | Documento en estado APROBADO |
| 1.2.1 | GEMBA / datos | Jefe EO + Operador | | | 1.1.1 | Ficha GEMBA completada |
| 1.2.3 | BPMN AS-IS | Jefe EO | | | 1.2.1 | Diagrama validado por area |
| 1.3.1 | BPMN TO-BE | Jefe EO | | | 1.2.3 | Aprobado por Subgerente MC |
| 1.3.2 | KPIs definidos | Jefe EO | | | 1.3.1 | Diccionario con formula, fuente, meta |
| 1.4.1 | Piloto activo | Jefe EO + Operador | | | 1.3.2 | Operando en turno real |
| 1.4.2 | Validacion KPIs | Analista | | | 1.4.1 | Delta vs. linea base confirmado |
| 1.5.2 | Registro SGL | Jefe EO | | | 1.4.2 | Entrada creada en SGL |
| 1.5.3 | Cierre formal | Jefe EO | | | 1.5.1 | Acta firmada |

---

## Cronograma de hitos

| Hito | Fecha | Criterio de cierre |
|---|---|---|
| Spec aprobado | YYYY-MM-DD | Estado = APROBADO |
| Diagnostico completo | YYYY-MM-DD | BPMN AS-IS + causa raiz documentada |
| Solucion disenada | YYYY-MM-DD | BPMN TO-BE + KPIs aprobados |
| Piloto iniciado | YYYY-MM-DD | Primer turno con nueva forma de operar |
| Validacion completada | YYYY-MM-DD | KPIs mejoran >= meta definida en spec |
| Cierre | YYYY-MM-DD | Acta + SGL actualizado |

---

## Recursos

| Recurso | Tipo | Dedicacion | Periodo |
|---|---|---|---|
| | | | |

---

## Matriz de riesgos

| ID | Riesgo | Probabilidad (1-3) | Impacto (1-3) | Score | Tratamiento |
|---|---|---|---|---|---|
| R1 | Datos SGL incompletos para el periodo | 2 | 3 | 6 | Solicitar exportacion SAP PM como respaldo |
| R2 | Operadores no disponibles para GEMBA | 2 | 2 | 4 | Coordinar con jefe de turno con 48h de anticipacion |
| R3 | Piloto interrumpido por parada de equipo | 1 | 3 | 3 | Definir equipo alternativo en spec |
| R4 | Causa raiz no confirmada post-GEMBA | 2 | 3 | 6 | Activar analisis Ishikawa con equipo ampliado |

---

## Coordinacion con otros agentes

| Agente | Rol en este proyecto | Dependencia |
|---|---|---|
| IA | Analisis historico de perdidas en arauco_mc.db | Provee datos para spec y BPMN AS-IS |
| TD | Automatizacion de alertas o flujos rediseñados | Recibe BPMN TO-BE aprobado |
| DA | Lectura de archivos fuente (.xlsx, .pdf) | Bajo demanda segun necesidad |
```

## Restricciones de este skill

- No elaborar plan sin spec en estado APROBADO: cualquier entregable derivado de un spec BLOQUEADO es invalido
- Hitos deben ser binarios (logrado / no logrado) — no usar porcentajes de avance como criterio
- Fechas realistas: considerar turnos, ventanas de parada programada y disponibilidad de equipos industriales
- Riesgos con score >= 6 deben tener contingencia — no dejar el campo vacio
- No incluir nombres propios de personas en el plan; usar cargos
- Si el proyecto requiere presupuesto, agregar fila en recursos con monto estimado y fuente (OPEX / proyecto aprobado); no inventar montos
