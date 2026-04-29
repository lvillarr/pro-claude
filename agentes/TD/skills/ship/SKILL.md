# Skill: ship — Documentación operacional, hand-off a TI y monitoreo post-entrega

> **Agente:** TD — Transformación Digital

## Propósito

Cerrar el ciclo de desarrollo: documentar operacionalmente el pipeline para que TI de Arauco pueda operarlo sin soporte continuo del agente TD, formalizar el hand-off con credenciales y accesos, versionar el codigo en git, y establecer el plan de monitoreo y alertas post-entrega.

## Cuándo usar este skill

- El pipeline paso la revision (`review`) con estado APROBADO o APROBADO CON OBSERVACIONES sin bloqueos
- El orquestador solicita preparar la entrega formal a TI
- Un pipeline existente necesita ser transferido a un nuevo equipo operacional
- Se cierra un sprint de implementacion y se necesita dejar evidencia de lo construido

**Prerequisito:** Revision (`review`) aprobada. Sin aval de revision, no hay hand-off: el pipeline podria tener problemas de seguridad o calidad que TI heredaria sin saberlo.

---

## Protocolo de ejecucion

### Paso 1 — README operacional

Crear el README en la carpeta del script. Estructura minima:

```
datos/scripts/README-[descripcion].md
```

El README debe ser legible por alguien de TI Arauco sin contexto previo del proyecto.

**Secciones obligatorias:**
1. Que hace el pipeline (1 parrafo, sin jerga de desarrollo)
2. Pre-requisitos (Python, librerias, variables de entorno)
3. Instalacion paso a paso
4. Como ejecutar manualmente
5. Como programar ejecucion automatica (cron)
6. Variables de entorno: nombre, descripcion, donde obtenerla
7. Troubleshooting: los 5 errores mas comunes con causa y solucion
8. Contacto para soporte: area responsable, no nombre individual

```markdown
# Pipeline: [Nombre descriptivo en espanol]

## Que hace

[1 parrafo: conecta [fuente] con [destino], extrae [que datos],
con frecuencia [cadencia], habilitando [proceso operacional].]

---

## Pre-requisitos

- Python 3.10 o superior
- Acceso a red interna Arauco (VPN si es remoto)
- Variables de entorno configuradas (ver seccion Variables)
- Librerias: `pip install requests pandas sqlalchemy` (ver requirements.txt)

---

## Instalacion

```bash
# 1. Clonar repositorio (o copiar carpeta)
git clone [URL_REPO] && cd proyecto_claude

# 2. Instalar dependencias
pip install -r datos/scripts/requirements.txt

# 3. Configurar variables de entorno
cp datos/scripts/.env.ejemplo datos/scripts/.env
# Editar .env con los valores reales (ver seccion Variables)
source datos/scripts/.env  # Linux/Mac
# En Windows: usar el panel de variables de entorno del sistema

# 4. Verificar conexion (modo diagnostico)
python datos/scripts/YYYY-MM-DD_[nombre].py --check-conexion
```

---

## Ejecucion manual

```bash
# Extraer turno actual (ultimas 8 horas)
python datos/scripts/YYYY-MM-DD_[nombre].py

# Extraer rango especifico
python datos/scripts/YYYY-MM-DD_[nombre].py \
  --desde 2025-01-01T00:00:00Z \
  --hasta 2025-01-01T08:00:00Z

# Modo verbose (logs detallados)
TD_LOG_LEVEL=DEBUG python datos/scripts/YYYY-MM-DD_[nombre].py
```

---

## Programacion automatica (cron)

```bash
# Ejecutar al final de cada turno: 06:00, 14:00, 22:00
crontab -e
# Agregar:
0 6,14,22 * * * /usr/bin/python3 /ruta/completa/datos/scripts/YYYY-MM-DD_[nombre].py >> /ruta/logs/etl.log 2>&1
```

En Windows Task Scheduler: [instrucciones paso a paso si aplica]

---

## Variables de entorno

| Variable | Descripcion | Ejemplo | Donde obtenerla |
|---|---|---|---|
| `TD_[SISTEMA]_URL` | URL base de la API [sistema] | `https://api.dealer.com/v2` | Proveedor / TI Arauco |
| `TD_[SISTEMA]_KEY` | Token de autenticacion API | `abc123...` | Proveedor / TI Arauco |
| `TD_DESTINO` | Sistema de destino | `forest_data_2` | Configuracion del proyecto |
| `TD_BUFFER_PATH` | Ruta del buffer offline local | `datos/scripts/buffer.db` | Default si no se define |
| `TD_LOG_LEVEL` | Nivel de logging | `INFO` o `DEBUG` | Default: INFO |
| `TD_TIMEOUT_SEC` | Timeout llamadas API (segundos) | `30` | Default: 30 |

---

## Troubleshooting

### Error: `EnvironmentError: Variables de entorno faltantes: ['TD_[SISTEMA]_KEY']`
**Causa:** La variable de entorno no esta configurada en el servidor.
**Solucion:** Verificar que el archivo `.env` existe y fue cargado (`source .env`). Confirmar con TI que el token fue asignado.

### Error: `HTTP 401 Unauthorized`
**Causa:** Token de API expirado o incorrecto.
**Solucion:** Solicitar token nuevo al proveedor [dealer/sistema]. Actualizar `TD_[SISTEMA]_KEY` en `.env`.

### Error: `ConnectionError: Max retries exceeded`
**Causa:** El servidor de [sistema] no es alcanzable. Puede ser corte de conectividad en predio remoto, VPN caida o mantencion del proveedor.
**Solucion:** Verificar conectividad de red. Si es predio remoto, los datos quedan en buffer local y se sincronizaran automaticamente al recuperar conexion.

### Advertencia: `Registros extraidos: 0`
**Causa:** No hubo actividad en el turno (equipo apagado, predio sin operacion) o el rango de fechas no tiene datos.
**Solucion:** Es comportamiento normal en fines de semana o durante mantenciones programadas. Verificar con el jefe de cosecha si persiste en dias habiles.

### Error: `UNIQUE constraint failed`
**Causa:** Se intento insertar un registro ya existente con INSERT OR IGNORE. No es un error real.
**Solucion:** Ignorar. El pipeline es idempotente: reejecutar con los mismos datos no genera duplicados.

---

## Contacto y soporte

**Area responsable:** Subgerencia de Mejora Continua — Transformacion Digital
**Canal de reporte de incidentes:** [Teams/correo del equipo]
**SLA de respuesta:** [N horas habiles]
```

### Paso 2 — Hand-off formal a TI

Producir el documento de transferencia:

```markdown
# Documento de Hand-off TD → TI: [nombre pipeline]

**Fecha de transferencia:** YYYY-MM-DD
**Entregado por:** TD (Arauco Mejora Continua)
**Receptor:** [Nombre, area TI Arauco]
**Estado al momento de transferencia:** Produccion / Staging

---

## Inventario de lo entregado

| Artefacto | Ruta | Descripcion |
|---|---|---|
| Script principal | datos/scripts/YYYY-MM-DD_[nombre].py | Pipeline ETL completo |
| Configuracion ejemplo | datos/scripts/.env.ejemplo | Plantilla de variables (sin valores reales) |
| Requirements | datos/scripts/requirements.txt | Dependencias Python exactas |
| README operacional | datos/scripts/README-[nombre].md | Guia de operacion y troubleshooting |
| Reporte de pruebas | datos/YYYY-MM-DD_test-[nombre].md | Evidencia de validacion tecnica |
| Revision aprobada | datos/YYYY-MM-DD_review-[nombre].md | Aval tecnico para produccion |

---

## Credenciales y accesos a transferir

| Sistema | Tipo de credencial | Estado | Responsable de entrega |
|---|---|---|---|
| [dealer/sistema] API | Token API | [Pendiente / Entregado] | [TI Arauco / Proveedor] |
| Forest Data 2.0 | Cuenta servicio | [Pendiente / Entregado] | Equipo FD2.0 |
| VPN / whitelist | IP del servidor | [Pendiente / Entregado] | TI infraestructura |

**Nota:** Todos los tokens y contrasenas deben almacenarse en el sistema de gestion de secretos de TI, no en archivos de texto plano.

---

## Accesos de servidor requeridos

- [ ] Python 3.10+ instalado en servidor de produccion
- [ ] Librerias instaladas en entorno virtual
- [ ] Variables de entorno configuradas en el servidor (no en .env en produccion)
- [ ] Cron o Task Scheduler configurado
- [ ] Directorio de logs con permisos de escritura

---

## Plan de on-call

| Escenario | Quien responde | Como detectarlo | Accion |
|---|---|---|---|
| Pipeline no ejecuto en > 10h | TI | Alerta en [sistema de monitoreo] | Revisar cron, logs |
| HTTP 401 | TI + proveedor | Log de error | Renovar token |
| Completitud < 90% | TI + MC | Alerta automatica | Investigar fuente |
| Buffer offline > 48h pendiente | TI | Alerta automatica | Verificar conectividad predio |
```

### Paso 3 — Versionado git

```bash
# Verificar que el script esta bajo control de version
git -C /ruta/proyecto status

# Agregar archivos del pipeline al staging
git add datos/scripts/YYYY-MM-DD_[nombre].py
git add datos/scripts/requirements.txt
git add datos/scripts/.env.ejemplo   # Ejemplo SIN valores reales
git add datos/scripts/README-[nombre].md
# NO agregar: .env, *.log, buffer_*.db

# Commit con mensaje descriptivo
git commit -m "feat(td): pipeline ETL [descripcion] — [sistemas integrados]

- Extrae [tipo de dato] desde [sistema fuente] via API REST
- Carga en [sistema destino] cada turno (8h)
- Buffer offline para predios remotos con sincronizacion automatica
- KPIs: completitud >= 95%, latencia < 30min, tasa error < 2%"

# Etiquetar version de produccion
git tag -a v1.0-[nombre-pipeline] -m "Version inicial produccion [fecha]"
```

Verificar que `.gitignore` incluye:
```
.env
*.log
datos/scripts/logs/
datos/scripts/buffer_*.db
datos/arauco_mc.db
```

### Paso 4 — Plan de monitoreo y alertas

```python
"""
Script de monitoreo post-entrega — Arauco TD
Proposito: Verificar estado del pipeline en produccion
Ejecutar: python YYYY-MM-DD_monitor-[nombre].py
Frecuencia recomendada: cada turno, despues de la ejecucion ETL
"""

import sqlite3
import logging
from datetime import datetime, timezone, timedelta

log = logging.getLogger("monitor")


def verificar_latencia(db_path: str, tabla: str,
                        col_ts: str, max_minutos: int = 30) -> bool:
    """
    Verifica que el registro mas reciente no tenga mas de max_minutos de antiguedad.
    Alerta si el pipeline no ha ejecutado en el ultimo turno.
    """
    with sqlite3.connect(db_path) as conn:
        ultimo = conn.execute(
            f"SELECT MAX({col_ts}) FROM {tabla}"
        ).fetchone()[0]
    if not ultimo:
        log.error("[ALERTA] No hay datos en tabla — pipeline nunca ha ejecutado")
        return False
    ts_ultimo = datetime.fromisoformat(ultimo.replace("Z", "+00:00"))
    edad_min = (datetime.now(timezone.utc) - ts_ultimo).total_seconds() / 60
    ok = edad_min <= max_minutos
    if not ok:
        log.error(f"[ALERTA] Dato mas reciente tiene {edad_min:.0f} min de antiguedad "
                  f"(maximo: {max_minutos} min). Pipeline puede estar caido.")
    else:
        log.info(f"[OK] Latencia: ultimo dato hace {edad_min:.1f} min")
    return ok


def verificar_completitud_reciente(db_path: str, tabla: str,
                                    campos_criticos: list[str],
                                    horas: int = 8) -> float:
    """
    Verifica completitud en las ultimas N horas (un turno).
    Returns: porcentaje de completitud del campo mas bajo
    """
    desde = (datetime.now(timezone.utc) - timedelta(hours=horas)).isoformat()
    min_completitud = 100.0
    with sqlite3.connect(db_path) as conn:
        total = conn.execute(
            f"SELECT COUNT(*) FROM {tabla} WHERE timestamp_utc >= ?", (desde,)
        ).fetchone()[0]
        if total == 0:
            log.warning("[ALERTA] Sin registros en el ultimo turno")
            return 0.0
        for campo in campos_criticos:
            nulos = conn.execute(
                f"SELECT COUNT(*) FROM {tabla} WHERE {campo} IS NULL AND timestamp_utc >= ?",
                (desde,)
            ).fetchone()[0]
            pct = (1 - nulos / total) * 100
            if pct < 95:
                log.error(f"[ALERTA] Completitud '{campo}' en ultimo turno: {pct:.1f}% "
                          f"(minimo: 95%)")
            else:
                log.info(f"[OK] Completitud '{campo}': {pct:.1f}%")
            min_completitud = min(min_completitud, pct)
    return min_completitud


def verificar_buffer_pendiente(buffer_db: str, max_horas: int = 48) -> bool:
    """
    Alerta si hay registros en buffer offline con mas de max_horas sin sincronizar.
    Puede indicar problema de conectividad persistente en predio remoto.
    """
    desde = (datetime.now(timezone.utc) - timedelta(hours=max_horas)).isoformat()
    with sqlite3.connect(buffer_db) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM telemetria_buffer "
            "WHERE sincronizado=0 AND creado_en < ?", (desde,)
        ).fetchone()[0]
    if count > 0:
        log.error(f"[ALERTA] {count} registros en buffer sin sincronizar por > {max_horas}h. "
                  "Verificar conectividad del predio remoto.")
        return False
    log.info("[OK] Buffer offline sin registros pendientes")
    return True
```

### Paso 5 — Producir el ENTREGA TD final

```
ENTREGA TD:
Archivo(s):
  - datos/scripts/YYYY-MM-DD_[nombre].py
  - datos/scripts/README-[nombre].md
  - datos/scripts/.env.ejemplo
  - datos/scripts/requirements.txt
  - datos/YYYY-MM-DD_handoff-[nombre].md
  - datos/YYYY-MM-DD_monitor-[nombre].py
Estado: funcional / en produccion
Dependencias:
  - Python 3.10+
  - pip install requests pandas sqlalchemy
  - Variables de entorno: [lista]
  - Cron configurado en servidor [nombre]
Limitaciones:
  - [ej: monitoreo de alertas requiere integracion con Teams/email por TI]
  - [ej: token dealer se rota cada 30 dias; TI debe actualizar manualmente]
Impacto esperado:
  - [ej: telemetria Tigercat disponible en Forest Data 2.0 cada turno sin intervencion manual]
  - [ej: elimina planilla Excel semanal de horas motor — ahorra 3h analista/semana]
```

---

## Restricciones de este skill

- El README debe ser escrito para un tecnico TI sin contexto del proyecto: si requiere saber que es Forest Data 2.0 para seguir las instrucciones, reescribir
- `.env.ejemplo` es obligatorio y debe tener TODOS los nombres de variables con descripcion pero SIN valores reales; el archivo `.env` con valores reales NUNCA se incluye en git
- El hand-off no esta completo hasta que TI confirme haber recibido y probado las credenciales reales; si no hay confirmacion, documentar el pendiente
- Seccion de troubleshooting: minimo los 5 errores mas frecuentes observados en pruebas; no inventar errores teoricos
- Plan de monitoreo debe incluir explicitamente el caso de buffer offline > 48h en predio remoto: es el fallo mas comun y el mas dificil de detectar sin alerta
- Versionado git es obligatorio antes de hand-off: TI debe poder reproducir exactamente lo que recibio y hacer rollback si hay regresion
- Los tiempos de turno (8h) y los umbrales de alerta deben estar configurables via variable de entorno, no hardcodeados: el ciclo de turnos puede cambiar entre faenas o temporadas
