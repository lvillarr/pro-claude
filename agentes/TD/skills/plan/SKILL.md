# Skill: plan — Arquitectura de integración por fases

> **Agente:** TD — Transformación Digital

## Propósito

Traducir la especificación (`spec`) en una arquitectura técnica concreta: fases de implementación, stack de integración, plan de conectividad edge/cloud, dependencias con TI y proveedores, y mapa de riesgos por punto de integración.

## Cuándo usar este skill

- Existe un documento `spec` aprobado o revisado para la iniciativa
- El orquestador pide un plan de implementacion técnica después de aprobar el alcance
- Se necesita dimensionar esfuerzo, dependencias y riesgos antes de empezar a construir (`build`)

**Prerequisito:** Documento de especificacion (`spec`) con sistemas identificados, MVP definido y restricciones de conectividad documentadas. Sin spec, no hay plan.

---

## Protocolo de ejecucion

### Paso 1 — Leer la especificacion

```python
# Leer el spec con read_file o markitdown segun formato
import subprocess
result = subprocess.run(
    ["markitdown", "datos/YYYY-MM-DD_spec-descripcion.md"],
    capture_output=True, text=True
)
```

Extraer: sistemas fuente/destino, interfaz de cada uno, restricciones de conectividad, KPIs de integracion comprometidos.

### Paso 2 — Definir patron de arquitectura

Seleccionar el patron adecuado segun el contexto:

| Patron | Cuando usar | Ejemplo forestal |
|---|---|---|
| **Pull batch** | Datos no criticos, conectividad intermitente, volumen moderado | Polling cada turno a API Tigercat → Forest Data 2.0 |
| **Push event** | Datos en tiempo real, equipo siempre online | Historian/OSIsoft PI → SGL en tiempo real |
| **Edge buffer + sync** | Predio remoto sin conectividad continua | Gateway local acumula telemetria → sync al llegar a base |
| **File drop (SFTP/S3)** | Sistema legacy sin API | Planex exporta CSV → pipeline ingesta → Datalake |
| **CDC (Change Data Capture)** | Base de datos SQL accesible | SAP PM tablas → replica incremental → analytics |

### Paso 3 — Fases de implementacion

Estructurar en fases de 2-4 semanas cada una. MVP siempre en Fase 1.

**Plantilla de fases:**

```
Fase 1 — Conexion basica y validacion (semanas 1-4)
  Objetivo: Demostrar que los datos fluyen de A a B
  Entregables:
    - Script de extraccion autenticado contra [sistema fuente]
    - Carga en [sistema destino] (tabla staging o archivo)
    - Validacion de completitud: row counts y campos criticos
  Criterio de exito: >= 95% completitud en 3 turnos consecutivos

Fase 2 — Robustez y manejo de errores (semanas 5-8)
  Objetivo: Pipeline tolerante a fallos y reconexion automatica
  Entregables:
    - Retry logic con backoff exponencial
    - Log estructurado de errores
    - Sincronizacion offline si aplica (predio remoto)
  Criterio de exito: recuperacion en < 1 turno tras caida de API

Fase 3 — Produccion y monitoreo (semanas 9-12)
  Objetivo: Pipeline en produccion con alertas y documentacion
  Entregables:
    - Cron/scheduler en servidor de produccion
    - Alertas en [canal: Teams/email/SGL]
    - Documentacion operacional y hand-off a TI
  Criterio de exito: KPIs de integracion dentro de meta 30 dias seguidos
```

### Paso 4 — Arquitectura de conectividad edge/cloud

Para cada punto de integracion que incluya predios remotos:

```
[Maquina/sensor en predio]
       |
       | (conexion satelital / 4G / sin conexion)
       v
[Edge device / gateway local]  <-- buffer local (SQLite o archivo)
       |
       | (sync al llegar a base o ventana de conectividad)
       v
[Servidor de integracion Arauco]  <-- Python worker / scheduler
       |
       v
[Sistema destino: Forest Data 2.0 / Datalake / SGL / SAP]
```

Definir para cada nodo:
- Tecnologia propuesta (solo si hay razon tecnica, no por preferencia)
- Capacidad de almacenamiento local necesaria
- Frecuencia y disparador de sincronizacion

### Paso 5 — Mapa de dependencias con TI y proveedores

```markdown
| Dependencia | Tipo | Responsable | Plazo estimado | Bloquea |
|---|---|---|---|---|
| Credenciales API Tigercat | Acceso externo | Proveedor Tigercat | 1-2 semanas | Fase 1 |
| VPN / whitelist IP servidor Arauco | Infraestructura | TI Arauco | 3-5 dias | Fase 1 |
| Acceso lectura tabla SAP PM | Permiso BD | TI SAP Arauco | 1 semana | Fase 2 |
| Cuenta servicio Forest Data 2.0 | Acceso plataforma | Equipo FD2.0 | 1 semana | Fase 1 |
| Ambiente de prueba [sistema] | Entorno test | TI / proveedor | antes Fase 1 | Desarrollo |
```

### Paso 6 — Riesgos tecnicos por punto de integracion

Para cada sistema en la cadena, documentar el riesgo real:

```markdown
| Punto | Riesgo | Probabilidad | Impacto | Mitigacion |
|---|---|---|---|---|
| API Tigercat | API down o cambio de version sin aviso | Media | Alto | Retry + alerta + contrato SLA |
| Credenciales dealer | Rotacion de tokens sin notificacion | Media | Alto | Almacenar en env vars + monitoreo 401 |
| Conectividad predio remoto | Perdida de senal > 8h (un turno) | Alta | Medio | Buffer local + sync diferido |
| SAP PM | Timeout en consultas tablas grandes | Media | Medio | Paginacion + ventana horaria off-peak |
| Forest Data 2.0 | Rate limiting en ingesta masiva | Baja | Medio | Batch con delays + encolar |
| Planex exportacion CSV | Cambio de esquema sin versionado | Media | Alto | Validacion de esquema en ingesta |
```

### Paso 7 — Guardar el plan

```
datos/YYYY-MM-DD_plan-[descripcion].md
```

---

## Plantilla de plan de arquitectura

```markdown
# Plan de Arquitectura TD: [Nombre iniciativa]

**Fecha:** YYYY-MM-DD
**Basado en spec:** datos/YYYY-MM-DD_spec-[descripcion].md
**Responsable TD:** [Nombre]

---

## 1. Patron de arquitectura seleccionado

**Patron:** [Pull batch / Push event / Edge buffer + sync / File drop / CDC]
**Justificacion:** [1-2 lineas: por que este patron para este contexto]

## 2. Diagrama de flujo

```
[fuente] -> [protocolo/frecuencia] -> [transformacion] -> [destino]
        \-> [log/error store]
```

## 3. Fases de implementacion

### Fase 1 — [nombre] (semanas X-Y)
- Objetivo: ...
- Entregables: ...
- Criterio de exito: ...

### Fase 2 — [nombre] (semanas X-Y)
...

## 4. Conectividad edge/cloud

[diagrama y especificacion por nodo]

## 5. Dependencias con TI y proveedores

[tabla de dependencias]

## 6. Mapa de riesgos

[tabla de riesgos por punto de integracion]

## 7. Stack tecnico propuesto

| Componente | Tecnologia | Justificacion |
|---|---|---|
| Extraccion | Python + requests | Liviano, compatible con APIs REST dealers |
| Transformacion | pandas | Suficiente para volumen de telemetria forestal |
| Carga | sqlalchemy / requests POST | Segun interfaz del destino |
| Scheduling | cron / APScheduler | Sin overhead de orquestador complejo para MVP |
| Buffer offline | SQLite local | Liviano, sin dependencias, funciona en edge |
| Logging | logging stdlib + archivo rotativo | Sin dependencias externas |

## 8. Proximos pasos

1. Aprobar plan con TI y area operacional
2. Gestionar dependencias criticas (credenciales, accesos, ambientes)
3. Activar skill `build` para implementacion de Fase 1
```

---

## Restricciones de este skill

- No empezar Fase 2 o 3 en el plan si la Fase 1 no tiene criterio de exito verificable
- Stack tecnico debe justificarse contra el contexto forestal (conectividad, volumen, equipo mantenedor), no por preferencia tecnologica
- Credenciales, tokens y contrasenas nunca en el plan: solo referencia a variables de entorno o vault
- Dependencias con TI y proveedores deben tener responsable y plazo nombrados; no dejar como "a coordinar"
- Riesgos de conectividad en predios remotos son mandatorios: todos los planes que incluyan equipos de cosecha o transporte deben incluir estrategia offline
- Diagrama de flujo obligatorio aunque sea ASCII: hace visible la arquitectura sin herramientas externas
