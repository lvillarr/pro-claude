# Skill: spec — Especificación de iniciativa digital TD

> **Agente:** TD — Transformación Digital

## Propósito

Levantar y documentar el alcance técnico de una iniciativa de integración o habilitación digital: proceso operacional que habilita, sistemas a conectar, MVP acotado, KPIs de integración y restricciones de conectividad en terreno forestal.

## Cuándo usar este skill

- Se pide integrar un sistema forestal (Planex, Forest Data 2.0, dealer API, SGL, SAP) con otro sistema o pipeline
- Se quiere digitalizar un proceso operacional (trazabilidad de madera, telemetría de cosecha, sincronización de datos de predio)
- Se va a construir un conector, ETL o pipeline y no existe especificación previa
- El orquestador activa a TD con una solicitud nueva sin documento base

**Prerequisito:** Debe existir una descripción del proceso operacional afectado (verbal, doc de Word, correo o brief del orquestador). Sin proceso entendido, no se especifica tecnología.

---

## Protocolo de ejecución

### Paso 1 — Entender el proceso antes de la herramienta

Leer cualquier documento de contexto disponible con `read_file` o `markitdown`. Si no hay documento, hacer UNA pregunta concreta al orquestador:

> "¿Cuál es el proceso operacional que esta integración debe habilitar y qué decisión mejora?"

Identificar:
- Proceso operacional: ¿cosecha, transporte, mantenimiento, planificación, trazabilidad?
- Rol del dato: ¿alimenta planificación (Opticort/Opti-Maq), visibilidad operacional (Forest Gantt/SGL), analytics (Datalake/Forest Data 2.0)?
- Usuario final: ¿jefe de cosecha, planificador, analista MC, TI?

### Paso 2 — Identificar sistemas fuente y destino

Para cada sistema involucrado, relevar:

| Campo | Preguntar/verificar |
|---|---|
| Nombre del sistema | Planex, Opticort, dealer Tigercat, SAP PM, SGL, Historian, Forest Data 2.0, Datalake |
| Tipo de interfaz | API REST, archivo Excel/CSV, base de datos SQL, SFTP, WebSocket |
| Protocolo de autenticación | API key, OAuth2, usuario/contrasena LDAP, certificado |
| Frecuencia de actualización | Tiempo real, cada turno (8h), diario, semanal |
| Formato de datos | JSON, XML, CSV, parquet, tabla SQL |
| Propietario/contacto | TI Arauco, proveedor externo (Planex S.A., dealer), área operacional |

### Paso 3 — Separar MVP de alcance futuro

Definir el MVP como la integración mínima que entrega valor demostrable en menos de 4 semanas:

```
MVP (semana 1-4):
  - Un sistema fuente, un sistema destino
  - Un tipo de dato crítico (ej: horas motor Tigercat → Forest Data 2.0)
  - Frecuencia mínima aceptable (ej: cada turno, no tiempo real)
  - Sin transformaciones complejas si no son necesarias

Alcance futuro:
  - Segundo dealer o segundo tipo de dato
  - Enriquecimiento con datos geo-espaciales Planex NOM
  - Normalización multi-dealer
  - Dashboard en Forest Data 2.0
```

### Paso 4 — Definir KPIs de integración

No KPIs de negocio (esos son del agente EO). KPIs técnicos de la integración:

| KPI | Descripcion | Meta ejemplo |
|---|---|---|
| **Latencia de entrega** | Tiempo desde que el dato se genera hasta que está disponible en destino | < 30 min por turno |
| **Completitud** | % de registros esperados que llegan sin nulls en campos criticos | >= 95% |
| **Frecuencia** | Cadencia de sincronizacion o polling real vs. acordada | Desviacion < 10% |
| **Tasa de error** | % de llamadas API o cargas que fallan | < 2% |
| **Tiempo de recuperacion** | Cuanto tarda en resincronizar tras caida de conectividad | < 1 turno |

### Paso 5 — Documentar restricciones de conectividad

Predios remotos tienen conectividad satelital o 4G limitada. Especificar:

- ¿El equipo fuente (dealer, sensor) opera offline? ¿Cuanto tiempo puede acumular datos?
- ¿Hay edge device (tablet, gateway local) o solo la maquina?
- ¿La sincronizacion es push (dispositivo envia) o pull (servidor consulta)?
- ¿Ventana de conectividad: siempre online, solo en base, al llegar a zona con senal?

### Paso 6 — Producir el documento de especificacion

Usar la plantilla de abajo. Guardar en:
```
datos/YYYY-MM-DD_spec-[descripcion].md
```

---

## Plantilla de especificacion

```markdown
# Especificacion TD: [Nombre de la iniciativa]

**Fecha:** YYYY-MM-DD
**Solicitante:** [Orquestador / Area / Persona]
**Responsable TD:** [Nombre]
**Estado:** Borrador / Revisado / Aprobado

---

## 1. Proceso operacional habilitado

[1 parrafo: que proceso mejora, que decision facilita, quien la toma]

**Sistemas afectados en la cadena:** Planex → Opticort → Opti-Maq → Forest Gantt → [destino]

---

## 2. Sistemas a integrar

| Rol | Sistema | Interfaz | Autenticacion | Frecuencia | Propietario |
|---|---|---|---|---|---|
| Fuente | [sistema] | [API/CSV/SQL] | [tipo] | [cadencia] | [dueno] |
| Destino | [sistema] | [API/tabla] | [tipo] | [cadencia] | [dueno] |

**Datos criticos:**
- Campo: `[nombre_campo]` — Descripcion: [uso operacional] — Tipo: [string/float/datetime]

---

## 3. MVP vs. alcance futuro

**MVP (semanas 1-4):**
- [ ] [entregable 1]
- [ ] [entregable 2]

**Alcance futuro (post-MVP):**
- [ ] [capacidad futura 1]

---

## 4. KPIs de integracion

| KPI | Meta | Metodo de medicion |
|---|---|---|
| Latencia de entrega | [valor] | [como se mide] |
| Completitud de registros | [valor %] | [query o script] |
| Tasa de error | [valor %] | [log o monitoreo] |
| Tiempo de recuperacion | [valor] | [test de reconexion] |

---

## 5. Restricciones de conectividad

- **Tipo de conexion en predio:** [satelital / 4G / LAN / sin conexion]
- **Modo de operacion:** [offline con sync al llegar a base / online continuo]
- **Capacidad de almacenamiento local:** [horas o dias de datos en buffer]
- **Ventana de sincronizacion:** [descripcion]

---

## 6. Dependencias y riesgos iniciales

| Dependencia | Responsable | Riesgo si no disponible |
|---|---|---|
| Credenciales API [sistema] | TI Arauco / Proveedor | Bloquea desarrollo |
| Acceso a ambiente de prueba [sistema] | [responsable] | Retrasa validacion |
| Documentacion API dealer [dealer] | [dealer] | Requiere ingenieria inversa |

---

## 7. Proximos pasos

1. Validar especificacion con TI y area operacional
2. Activar skill `plan` para arquitectura de fases
3. Solicitar credenciales y ambientes de prueba
```

---

## Restricciones de este skill

- No proponer stack tecnologico en este paso: la tecnologia se define en `plan`, no en `spec`
- Si no hay proceso entendido, no hay spec: hacer una pregunta antes de escribir
- MVP debe ser alcanzable en 4 semanas con el equipo disponible; no sobreprometer
- Restricciones de conectividad de predios remotos son obligatorias: siempre documentar modo offline/online
- Nunca asumir que una API de dealer esta disponible sin confirmacion del proveedor (Tigercat, John Deere, Caterpillar, Volvo, Develon, Liebherr, Ecoforst tienen distintos niveles de apertura de API)
- KPIs de integracion distintos de KPIs de negocio: latencia/completitud/frecuencia, no toneladas ni costo
