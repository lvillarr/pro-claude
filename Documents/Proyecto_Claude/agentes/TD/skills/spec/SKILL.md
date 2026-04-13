# Skill: spec — Especificación de Iniciativa de Transformación Digital

## Propósito

Definir con precisión una iniciativa de transformación digital antes de planificar o implementar. Produce un documento de especificación que alinea al equipo sobre qué proceso se digitaliza, qué sistemas se integran, cuál es el MVP y cómo se mide el éxito. Evita construir integraciones o arquitecturas para requerimientos mal entendidos.

---

## Cuándo usar este skill

- El orquestador asigna una nueva iniciativa de digitalización o integración de sistemas
- Se detecta una brecha en visibilidad operacional, trazabilidad o conectividad de datos
- Se solicita conectar sistemas existentes (SAP, SGL, Planex, Forest Data, telemetría)
- Se necesita alinear a stakeholders técnicos y de negocio antes de iniciar desarrollo

**Prerequisito:** ninguno. Es el punto de partida de toda iniciativa TD.

---

## Protocolo de ejecución

### Paso 1 — Entender el proceso que se digitaliza
Antes de pensar en herramientas o APIs, responder:
- ¿Qué proceso forestal habilita o mejora esta iniciativa? (cosecha, transporte, planta, caminos)
- ¿Qué información no existe hoy o llega tarde/incompleta?
- ¿Qué sistemas están involucrados (fuente → destino)?
- ¿Hay conectividad confiable en el área de operación? (predio remoto vs. planta)

### Paso 2 — Clasificar el tipo de iniciativa
| Tipo | Cuándo aplica |
|---|---|
| **Integración de sistemas** | Conectar dos sistemas existentes (SAP ↔ SGL, Planex → Forest Data) |
| **Telemetría / IoT** | Capturar datos de máquinas o sensores en tiempo real |
| **ETL / pipeline de datos** | Transformar y cargar datos entre sistemas para análisis |
| **Automatización de proceso** | Reemplazar tarea manual con script o workflow automatizado |
| **Arquitectura de datos** | Diseñar Datalake, esquemas, gobierno de datos |
| **Conectividad en terreno** | Sincronización offline/online para predios remotos |

### Paso 3 — Mapear sistemas involucrados
| Sistema | Rol | Tipo de integración | Disponibilidad de API | Responsable técnico |
|---|---|---|---|---|

Confirmar:
- ¿Existe documentación de la API o del esquema de datos?
- ¿Hay credenciales disponibles o se necesita gestión con TI?
- ¿El sistema tiene restricciones de seguridad o acceso?

### Paso 4 — Definir MVP vs. solución completa
- **MVP (semanas)**: qué es lo mínimo que entrega valor demostrable
- **Solución completa (meses)**: qué incluye la versión definitiva
- ¿Qué queda explícitamente fuera del alcance?

### Paso 5 — Definir KPIs de éxito
| KPI | Línea base | Meta | Fuente | Responsable |
|---|---|---|---|---|

### Paso 6 — Entregar
```
datos/YYYY-MM-DD_spec-td-[nombre-iniciativa].md
```

---

## Plantilla de especificación TD

```markdown
# Especificación de Iniciativa TD
**Fecha:** YYYY-MM-DD | **Área:** Transformación Digital
**Iniciativa:** [Nombre] | **Tipo:** [Integración / Telemetría / ETL / Automatización / Arquitectura / Conectividad]

---

## 1. Proceso que habilita
[Qué proceso forestal mejora. ¿Por qué importa operacionalmente?]

## 2. Brecha actual
[Qué información o automatización no existe hoy. Impacto cuantificado si aplica.]

## 3. Sistemas involucrados
| Sistema | Rol (fuente/destino/ambos) | API disponible | Acceso confirmado |
|---|---|---|---|

## 4. MVP vs. solución completa
**MVP:** [qué entrega en semanas y qué valor demuestra]
**Completo:** [qué incluye la versión definitiva]
**Excluye:** [qué queda fuera del scope]

## 5. KPIs de éxito
| KPI | Línea base | Meta | Fuente |
|---|---|---|---|

## 6. Restricciones técnicas
- [Conectividad: ¿el área tiene red? ¿Cuál es el ancho de banda disponible?]
- [Seguridad: ¿hay VPN, firewall, política de datos corporativa?]
- [Dependencias de TI: ¿qué gestiones externas se requieren?]

## 7. Criterio de inicio del plan
- [ ] Sistemas confirmados con API o esquema de datos conocido
- [ ] MVP definido y validado con stakeholder de negocio
- [ ] Credenciales o acceso gestionado con TI
- [ ] KPIs de éxito acordados
```

---

## Restricciones de este skill

- No proponer arquitectura técnica sin entender el proceso: primero proceso, luego herramienta
- Confirmar disponibilidad de API y credenciales antes de comprometer el plan
- El MVP debe ser tan pequeño como sea posible manteniendo valor demostrable
- Si no hay conectividad confiable, la arquitectura debe soportar modo offline desde el diseño
