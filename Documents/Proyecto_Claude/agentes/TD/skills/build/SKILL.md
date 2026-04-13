# Skill: build — Implementación de Soluciones de Transformación Digital

## Propósito

Construir la solución técnica definida en el plan: scripts de integración, pipelines ETL, conectores de telemetría, configuraciones de sistema y arquitecturas de datos. Produce código funcional, documentado y con manejo de errores para operaciones forestales con conectividad variable.

---

## Cuándo usar este skill

- El plan TD está aprobado con acceso a APIs confirmado
- Se necesita desarrollar: ETL, integración REST/SOAP, conector de telemetría, script de automatización
- Se solicita construir un MVP para demostrar valor antes de la solución completa

**Prerequisito:** plan aprobado con arquitectura definida y credenciales disponibles.

---

## Protocolo de ejecución

### Paso 1 — Explorar la API o fuente de datos
```python
import requests
import json

# Autenticación y exploración de endpoint
session = requests.Session()
session.headers.update({"Authorization": f"Bearer {os.getenv('API_TOKEN')}"})

resp = session.get(f"{BASE_URL}/endpoint")
resp.raise_for_status()
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
```

Nunca hardcodear credenciales. Siempre usar variables de entorno:
```python
import os
API_TOKEN = os.getenv("FOREST_API_TOKEN")
SAP_USER  = os.getenv("SAP_USER")
SAP_PASS  = os.getenv("SAP_PASS")
```

### Paso 2 — Pipeline ETL base
```python
import logging
import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def extract(fecha_inicio: str, fecha_fin: str) -> pd.DataFrame:
    """Extrae datos del sistema fuente para el rango de fechas dado."""
    logger.info(f"Extrayendo datos {fecha_inicio} → {fecha_fin}")
    # ... lógica de extracción
    return df

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y normaliza los datos extraídos."""
    df = df.dropna(subset=["campo_clave"])
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["codigo_equipo"] = df["codigo_equipo"].str.upper().str.strip()
    logger.info(f"Transformación: {len(df)} registros procesados")
    return df

def load(df: pd.DataFrame, destino: str) -> None:
    """Carga los datos en el sistema destino."""
    # ... lógica de carga
    logger.info(f"Carga completada: {len(df)} registros en {destino}")

if __name__ == "__main__":
    df_raw = extract("2024-01-01", "2024-01-31")
    df_clean = transform(df_raw)
    load(df_clean, "datos/arauco_mc.db")
```

### Paso 3 — Conectores de telemetría (dealer APIs)
```python
import time

def poll_telemetria(dealer: str, equipos: list, intervalo_seg: int = 300) -> None:
    """
    Polling de telemetría de equipos forestales.
    
    Args:
        dealer: nombre del dealer (tigercat, john_deere, develon, etc.)
        equipos: lista de IDs de equipos a monitorear
        intervalo_seg: frecuencia de consulta en segundos
    """
    logger.info(f"Iniciando polling {dealer} — {len(equipos)} equipos")
    while True:
        try:
            for equipo_id in equipos:
                data = get_telemetria(dealer, equipo_id)
                normalizar_y_guardar(data, equipo_id, dealer)
        except requests.exceptions.ConnectionError:
            logger.warning("Sin conectividad — reintentando en 60s")
            time.sleep(60)
            continue
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
        time.sleep(intervalo_seg)
```

### Paso 4 — Sincronización offline/online
```python
import sqlite3
from pathlib import Path

QUEUE_DB = Path("datos/sync_queue.db")

def encolar_registro(tabla: str, datos: dict) -> None:
    """Encola un registro para sincronización cuando haya conectividad."""
    with sqlite3.connect(QUEUE_DB) as conn:
        conn.execute("""
            INSERT INTO sync_queue (tabla, datos_json, timestamp, estado)
            VALUES (?, ?, ?, 'pendiente')
        """, (tabla, json.dumps(datos), datetime.now().isoformat()))

def sync_pendientes() -> int:
    """Intenta sincronizar registros en cola. Retorna N registros sincronizados."""
    sincronizados = 0
    with sqlite3.connect(QUEUE_DB) as conn:
        pendientes = conn.execute(
            "SELECT id, tabla, datos_json FROM sync_queue WHERE estado='pendiente'"
        ).fetchall()
        for id_, tabla, datos_json in pendientes:
            try:
                enviar_al_servidor(tabla, json.loads(datos_json))
                conn.execute("UPDATE sync_queue SET estado='enviado' WHERE id=?", (id_,))
                sincronizados += 1
            except Exception:
                pass  # queda en cola para el próximo intento
    return sincronizados
```

### Paso 5 — Estructura de archivos del proyecto TD
```
datos/scripts/
├── YYYY-MM-DD_etl-[nombre].py       ← pipeline principal
├── YYYY-MM-DD_config-[nombre].json  ← configuración sin credenciales
├── YYYY-MM-DD_connector-[dealer].py ← conector de telemetría
└── README.md                         ← instrucciones de uso y variables de entorno
```

### Paso 6 — Log de construcción
```
datos/YYYY-MM-DD_build-log-td-[nombre-iniciativa].md
```

---

## Restricciones de este skill

- **Nunca hardcodear credenciales**: siempre `os.getenv()`; documentar las variables requeridas en el README
- **Docstring mínimo en cada función**: propósito, args, retorno
- **Logging en cada paso crítico**: extracción, transformación, carga, errores
- **Manejo de errores explícito**: no usar `except: pass` salvo en sync offline donde está justificado
- **Offline-first si el contexto es terreno**: asumir que la conectividad puede fallar en cualquier momento
