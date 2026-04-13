# Skill: plan — Planificación de Iniciativa de Transformación Digital

## Propósito

Transformar la especificación TD validada en un plan de implementación técnica: arquitectura de la solución, secuencia de desarrollo, dependencias de sistemas y criterios de aceptación. Define el orden correcto para no construir integraciones sobre bases inestables.

---

## Cuándo usar este skill

- El skill `spec` fue completado con sistemas confirmados y MVP definido
- El orquestador solicita planificar una iniciativa de digitalización o integración
- Se necesita estimar esfuerzo técnico y dependencias de TI antes de iniciar

**Prerequisito:** `spec` aprobado con sistemas, MVP y KPIs definidos.

---

## Protocolo de ejecución

### Paso 1 — Revisar la especificación
Leer `datos/YYYY-MM-DD_spec-td-[iniciativa].md` y extraer:
- Tipo de iniciativa, sistemas involucrados, MVP, KPIs, restricciones técnicas

### Paso 2 — Diseñar la arquitectura de la solución
Documentar el flujo de datos o el flujo de integración:
```
[Sistema Fuente] → [Capa de transformación] → [Sistema Destino]
     SGL API          ETL Python script         SQLite local
     SAP BAPI         Pandas + validación        Forest Data API
     Dealer API       Normalización JSON          Datalake
```

Definir:
- Método de extracción (pull/push, polling/webhook, batch/streaming)
- Formato de intercambio (JSON, CSV, XML, SOAP)
- Frecuencia de actualización
- Estrategia ante falla de conectividad (retry, queue local, offline-first)

### Paso 3 — Definir fases del proyecto TD

| Fase | Descripción | Hito verificable |
|---|---|---|
| **1. Acceso y exploración** | Conectar a APIs, explorar esquemas, muestra de datos | Datos reales extraídos exitosamente |
| **2. Transformación** | Normalización, validación, mapeo de campos | Pipeline transforma 100% de la muestra sin errores |
| **3. Integración** | Cargar en sistema destino, validar integridad | Datos en destino verificados vs. fuente |
| **4. Automatización** | Scheduler, manejo de errores, logging | Pipeline corre automático sin intervención manual |
| **5. Monitoreo y entrega** | Alertas, dashboard de estado, hand-off | Operacional con responsable designado |

### Paso 4 — Identificar dependencias de TI
| Dependencia | Responsable | Estado actual | Fecha compromiso |
|---|---|---|---|
| Credenciales API [sistema] | TI Arauco / Proveedor | Pendiente / Gestionado | YYYY-MM-DD |
| Acceso VPN a entorno [X] | TI Arauco | | |
| Servidor o entorno de ejecución | TI / Área | | |

### Paso 5 — Evaluar riesgos técnicos
| Riesgo | P | I | Mitigación |
|---|---|---|---|
| API de sistema sin documentación actualizada | A | M | Prototipo exploratorio primero |
| Cambios en estructura de datos sin aviso | M | A | Validación de esquema en cada ejecución |
| Conectividad intermitente en terreno | A | M | Arquitectura offline-first con sync posterior |
| Dependencia de TI para credenciales | A | A | Gestionar en paralelo con el desarrollo |

### Paso 6 — Entregar
```
datos/YYYY-MM-DD_plan-td-[nombre-iniciativa].md
```

---

## Plantilla de plan TD

```markdown
# Plan de Implementación TD — [Nombre]
**Fecha:** YYYY-MM-DD | **Responsable:** [Nombre]

---

## Arquitectura de la solución
```
[Fuente] → [Transformación] → [Destino]
```
**Frecuencia:** [batch diario / tiempo real / on-demand]
**Manejo offline:** [retry automático / queue local / N/A]

---

## Fases e hitos
| Fase | Tareas | Responsable | Inicio | Fin | Hito |
|---|---|---|---|---|---|

---

## Dependencias de TI
| Dependencia | Responsable | Estado | Fecha |
|---|---|---|---|

---

## Riesgos técnicos
| Riesgo | P | I | Mitigación |
|---|---|---|---|

---

## Criterio de inicio de implementación (build)
- [ ] Acceso a API(s) confirmado con credenciales reales
- [ ] Esquema de datos de fuente y destino documentado
- [ ] Arquitectura técnica revisada por al menos un par
- [ ] Dependencias de TI en curso con fecha comprometida
```

---

## Restricciones de este skill

- No iniciar implementación sin credenciales reales o al menos un endpoint de prueba funcional
- La estrategia offline debe definirse en el plan, no agregarse después: es mucho más costoso retrofit
- Toda dependencia de TI debe tener responsable y fecha comprometida antes de planificar cronograma
