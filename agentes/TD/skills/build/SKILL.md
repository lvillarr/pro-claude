# Skill: build — ETL, conectores de telemetría y sincronización offline

> **Agente:** TD — Transformación Digital

## Propósito

Implementar los componentes de integración definidos en `plan`: scripts de extraccion ETL, conectores API REST para dealers y sistemas forestales, sincronizacion offline/online para predios remotos, manejo de errores y logging operacional.

## Cuándo usar este skill

- Existe un plan (`plan`) aprobado y las dependencias de Fase 1 estan disponibles (credenciales, accesos, ambiente de prueba)
- Se necesita implementar un conector, pipeline ETL o script de sincronizacion
- Se va a construir un modulo Python para integracion con Tigercat, John Deere, Caterpillar, Volvo, Develon, Liebherr, Ecoforst, SAP, SGL, Historian, Planex, Forest Data 2.0 o Datalake

**Prerequisito:** Credenciales de prueba disponibles como variables de entorno. Si no existen, el entregable queda en estado "requiere credenciales" y se documenta como tal.

---

## Protocolo de ejecucion

### Paso 1 — Estructura base del proyecto

Antes de escribir codigo, verificar que el directorio destino existe:

```bash
ls datos/scripts/
```

Convencion de nombres:
```
datos/scripts/YYYY-MM-DD_etl-[descripcion].py
datos/scripts/YYYY-MM-DD_connector-[dealer|sistema].py
datos/scripts/YYYY-MM-DD_sync-[descripcion].py
datos/scripts/YYYY-MM-DD_config-[descripcion].json   # sin credenciales
```

### Paso 2 — Patron base de conector API REST (dealers y sistemas)

Patron estandar para cualquier dealer (Tigercat, John Deere, Caterpillar, Volvo, Develon, Liebherr, Ecoforst) o sistema interno (SGL, Forest Data 2.0, SAP):

```python
"""
Conector [nombre sistema/dealer] — Arauco Mejora Continua
Proposito: [que datos extrae y a donde los carga]
Inputs: variables de entorno TD_[SISTEMA]_URL, TD_[SISTEMA]_KEY
Outputs: registros normalizados en [destino]
"""

import os
import logging
import time
from datetime import datetime, timezone
from typing import Optional

import requests
import pandas as pd

# --- Logging estructurado ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("datos/scripts/logs/etl-[descripcion].log", encoding="utf-8"),
    ],
)
log = logging.getLogger("[descripcion]")


# --- Configuracion desde variables de entorno (nunca hardcodear) ---
def get_config() -> dict:
    required = ["TD_[SISTEMA]_URL", "TD_[SISTEMA]_KEY"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        raise EnvironmentError(f"Variables de entorno faltantes: {missing}")
    return {
        "base_url": os.environ["TD_[SISTEMA]_URL"].rstrip("/"),
        "api_key": os.environ["TD_[SISTEMA]_KEY"],
        "timeout": int(os.environ.get("TD_TIMEOUT_SEC", "30")),
        "max_retries": int(os.environ.get("TD_MAX_RETRIES", "3")),
    }


# --- Cliente HTTP con retry y backoff exponencial ---
def fetch_with_retry(
    url: str,
    headers: dict,
    params: Optional[dict] = None,
    max_retries: int = 3,
    timeout: int = 30,
) -> dict:
    delay = 2
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.Timeout:
            log.warning(f"Timeout en intento {attempt}/{max_retries}: {url}")
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "desconocido"
            log.warning(f"HTTP {status} en intento {attempt}/{max_retries}: {url}")
            if status == 401:
                log.error("Credenciales invalidas o expiradas. Verificar TD_[SISTEMA]_KEY.")
                raise  # No reintentar en 401
        except requests.exceptions.ConnectionError:
            log.warning(f"Error de conexion en intento {attempt}/{max_retries}: {url}")
        if attempt < max_retries:
            time.sleep(delay)
            delay *= 2  # backoff exponencial
    raise RuntimeError(f"Fallo tras {max_retries} intentos: {url}")


# --- Extraccion ---
def extract(config: dict, fecha_desde: str, fecha_hasta: str) -> list[dict]:
    """
    Extrae registros de telemetria del sistema [nombre].
    Inputs: fecha_desde, fecha_hasta en formato ISO8601 (YYYY-MM-DDTHH:MM:SSZ)
    Outputs: lista de registros crudos en formato JSON
    """
    headers = {"Authorization": f"Bearer {config['api_key']}"}
    url = f"{config['base_url']}/api/v1/[endpoint]"
    params = {"from": fecha_desde, "to": fecha_hasta, "format": "json"}
    log.info(f"Extrayendo desde {fecha_desde} hasta {fecha_hasta}")
    data = fetch_with_retry(url, headers=headers, params=params,
                            max_retries=config["max_retries"],
                            timeout=config["timeout"])
    registros = data.get("data", data) if isinstance(data, dict) else data
    log.info(f"Registros extraidos: {len(registros)}")
    return registros


# --- Transformacion ---
def transform(registros: list[dict]) -> pd.DataFrame:
    """
    Normaliza registros crudos al esquema estandar Arauco.
    Outputs: DataFrame con columnas [equipo_id, timestamp_utc, campo1, campo2, ...]
    """
    df = pd.DataFrame(registros)
    if df.empty:
        log.warning("DataFrame vacio tras extraccion")
        return df

    # Renombrar campos al esquema estandar
    df = df.rename(columns={
        "[campo_crudo_1]": "equipo_id",
        "[campo_crudo_2]": "timestamp_utc",
        # agregar segun esquema del sistema
    })

    # Parsear timestamps a UTC
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], utc=True)

    # Eliminar duplicados por clave de negocio
    df = df.drop_duplicates(subset=["equipo_id", "timestamp_utc"])

    # Agregar metadatos de carga
    df["_cargado_en"] = datetime.now(timezone.utc).isoformat()
    df["_fuente"] = "[nombre sistema]"

    log.info(f"Registros tras transformacion: {len(df)}")
    return df


# --- Carga ---
def load(df: pd.DataFrame, destino: str) -> None:
    """
    Carga DataFrame en el destino configurado.
    Inputs: df normalizado, destino ('sqlite' | 'forest_data_2' | 'datalake')
    """
    if df.empty:
        log.warning("Nada que cargar: DataFrame vacio")
        return
    if destino == "sqlite":
        from sqlalchemy import create_engine
        engine = create_engine(f"sqlite:///datos/arauco_mc.db")
        df.to_sql("[tabla_destino]", engine, if_exists="append", index=False)
        log.info(f"{len(df)} registros cargados en sqlite:[tabla_destino]")
    elif destino == "forest_data_2":
        # POST a API Forest Data 2.0
        _load_api(df, url=os.environ["TD_FD2_URL"], key=os.environ["TD_FD2_KEY"])
    else:
        raise ValueError(f"Destino no reconocido: {destino}")


def _load_api(df: pd.DataFrame, url: str, key: str) -> None:
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = df.to_dict(orient="records")
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    log.info(f"{len(payload)} registros cargados via API: {url}")


# --- Punto de entrada ---
if __name__ == "__main__":
    import sys
    config = get_config()
    fecha_desde = sys.argv[1] if len(sys.argv) > 1 else "hoy-1turno"
    fecha_hasta = sys.argv[2] if len(sys.argv) > 2 else "ahora"
    registros = extract(config, fecha_desde, fecha_hasta)
    df = transform(registros)
    load(df, destino=os.environ.get("TD_DESTINO", "sqlite"))
```

### Paso 3 — Sincronizacion offline/online (predios remotos)

Para equipos de cosecha y transporte que operan sin conexion continua:

```python
"""
Modulo de sincronizacion offline/online — buffer local SQLite
Uso: equipos en predios remotos con conectividad satelital o 4G intermitente
"""

import sqlite3
import os
import logging
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger("sync")

BUFFER_DB = os.environ.get("TD_BUFFER_PATH", "datos/scripts/buffer_local.db")


def init_buffer() -> None:
    """Crea tabla de buffer local si no existe."""
    Path(BUFFER_DB).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(BUFFER_DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS telemetria_buffer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipo_id TEXT NOT NULL,
                timestamp_utc TEXT NOT NULL,
                payload TEXT NOT NULL,           -- JSON crudo del dealer
                fuente TEXT NOT NULL,
                sincronizado INTEGER DEFAULT 0,  -- 0=pendiente, 1=enviado
                intentos INTEGER DEFAULT 0,
                creado_en TEXT DEFAULT (datetime('now', 'utc')),
                UNIQUE(equipo_id, timestamp_utc, fuente)
            )
        """)
    log.info(f"Buffer inicializado: {BUFFER_DB}")


def guardar_en_buffer(equipo_id: str, timestamp_utc: str,
                      payload: str, fuente: str) -> None:
    """
    Guarda un registro en el buffer local (idempotente por UNIQUE).
    Inputs: equipo_id, timestamp_utc ISO8601, payload JSON string, fuente
    """
    with sqlite3.connect(BUFFER_DB) as conn:
        conn.execute("""
            INSERT OR IGNORE INTO telemetria_buffer
                (equipo_id, timestamp_utc, payload, fuente)
            VALUES (?, ?, ?, ?)
        """, (equipo_id, timestamp_utc, payload, fuente))


def sincronizar_pendientes(fn_enviar) -> tuple[int, int]:
    """
    Intenta enviar todos los registros no sincronizados.
    fn_enviar: callable(registros: list[dict]) -> bool
    Returns: (enviados, fallidos)
    """
    with sqlite3.connect(BUFFER_DB) as conn:
        pendientes = conn.execute("""
            SELECT id, equipo_id, timestamp_utc, payload, fuente
            FROM telemetria_buffer
            WHERE sincronizado = 0 AND intentos < 5
            ORDER BY creado_en ASC
        """).fetchall()

    enviados, fallidos = 0, 0
    for row in pendientes:
        row_id, equipo_id, ts, payload, fuente = row
        try:
            import json
            fn_enviar([{"equipo_id": equipo_id, "timestamp_utc": ts,
                        **json.loads(payload)}])
            with sqlite3.connect(BUFFER_DB) as conn:
                conn.execute("""
                    UPDATE telemetria_buffer
                    SET sincronizado = 1
                    WHERE id = ?
                """, (row_id,))
            enviados += 1
        except Exception as e:
            log.warning(f"Fallo sincronizacion id={row_id}: {e}")
            with sqlite3.connect(BUFFER_DB) as conn:
                conn.execute("""
                    UPDATE telemetria_buffer
                    SET intentos = intentos + 1
                    WHERE id = ?
                """, (row_id,))
            fallidos += 1

    log.info(f"Sync: {enviados} enviados, {fallidos} fallidos de {len(pendientes)} pendientes")
    return enviados, fallidos
```

### Paso 4 — Script de telemetria forestal (ejemplo Tigercat)

```python
"""
Conector telemetria Tigercat — Arauco Mejora Continua
Extrae: horas motor, horas productivas, operador, predio, estado ON/OFF
Frecuencia: cada turno (8h) o bajo demanda
"""

import os
import logging
import requests
import pandas as pd
from datetime import datetime, timezone

log = logging.getLogger("tigercat")


def get_tigercat_telemetry(equipo_ids: list[str],
                            fecha_desde: str, fecha_hasta: str) -> pd.DataFrame:
    """
    Extrae telemetria de multiples equipos Tigercat.
    Inputs: lista de IDs de equipo, rango de fechas ISO8601
    Outputs: DataFrame con columnas estandar de telemetria forestal
    """
    base_url = os.environ["TD_TIGERCAT_URL"]
    api_key = os.environ["TD_TIGERCAT_KEY"]
    headers = {"x-api-key": api_key, "Accept": "application/json"}
    frames = []
    for eq_id in equipo_ids:
        url = f"{base_url}/equipment/{eq_id}/telemetry"
        params = {"startDate": fecha_desde, "endDate": fecha_hasta}
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            df = pd.DataFrame(data.get("readings", []))
            df["equipo_id"] = eq_id
            df["dealer"] = "Tigercat"
            frames.append(df)
            log.info(f"Tigercat {eq_id}: {len(df)} registros")
        except requests.exceptions.HTTPError as e:
            log.error(f"Error Tigercat {eq_id}: {e}")
    if not frames:
        return pd.DataFrame()
    result = pd.concat(frames, ignore_index=True)
    # Normalizar al esquema estandar
    result = result.rename(columns={
        "engineHours": "horas_motor",
        "productiveHours": "horas_productivas",
        "operatorId": "operador_id",
        "siteId": "predio_id",
        "machineState": "estado",
    })
    return result
```

### Paso 5 — Guardar y reportar

Guardar script en `datos/scripts/`. Verificar:
- [ ] Sin credenciales hardcodeadas
- [ ] Logging en cada paso critico
- [ ] Manejo de excepcion en cada llamada externa
- [ ] Idempotencia documentada (INSERT OR IGNORE, drop_duplicates)

---

## Plantilla de entregable build

```
ENTREGA TD:
Archivo(s): datos/scripts/YYYY-MM-DD_[tipo]-[descripcion].py
Estado: funcional / requiere credenciales / en desarrollo
Dependencias:
  - Python >= 3.10
  - pip install requests pandas sqlalchemy
  - Variables de entorno: TD_[SISTEMA]_URL, TD_[SISTEMA]_KEY
  - [otras dependencias: acceso red, VPN, etc.]
Limitaciones:
  - [ej: probado contra API de desarrollo, no produccion]
  - [ej: buffer offline no probado con > 72h sin conexion]
  - [ej: esquema API dealer puede cambiar sin aviso]
Impacto esperado:
  - [ej: disponibilidad de telemetria Tigercat en Forest Data 2.0 cada turno]
  - [ej: elimina carga manual de planilla Excel de horas motor]
```

---

## Restricciones de este skill

- Credenciales NUNCA hardcodeadas: siempre `os.environ["NOMBRE_VAR"]`; si falta, lanzar `EnvironmentError` con el nombre de la variable
- Cada funcion debe tener docstring con: proposito, inputs, outputs
- Logging obligatorio: nivel INFO en extraccion/carga, WARNING en reintentos, ERROR en fallos criticos
- Idempotencia obligatoria: INSERT OR IGNORE, upsert o drop_duplicates segun el destino — ningun pipeline puede crear duplicados al rerrun
- Buffer local SQLite para cualquier integracion con predios remotos: no asumir conectividad continua
- Dealers distintos tienen APIs distintas: Tigercat, John Deere, Caterpillar, Volvo, Develon, Liebherr y Ecoforst no comparten esquema; nunca unificar sin verificar documentacion real
- Si la API del dealer no esta disponible durante build, generar datos sinteticos realistas para desarrollo y documentar el supuesto
- Archivos de log en `datos/scripts/logs/` con rotacion; no en stdout solamente
