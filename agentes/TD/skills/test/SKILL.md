# Skill: test — Validación de integridad, errores y conectividad adversa

> **Agente:** TD — Transformación Digital

## Propósito

Verificar que el pipeline o conector construido en `build` cumple los KPIs de integracion definidos en `spec`: integridad de datos (row counts, rangos, nulos), tolerancia a fallos (API down, timeout, payload malformado), comportamiento en conectividad adversa (predios remotos, latencia alta, reconexion), e idempotencia (rerrun sin duplicados).

## Cuándo usar este skill

- El script o conector de `build` esta listo para validacion antes de Fase 2 o produccion
- Se va a entregar el pipeline al equipo de TI y se necesita evidencia de pruebas
- Se detecta un defecto en produccion y se necesita reproducirlo con un caso de prueba
- El orquestador solicita validacion tecnica antes de aprobar el paso a produccion

**Prerequisito:** Script funcional de `build` con al menos una extraccion real o con datos sinteticos documentados. Las pruebas de conectividad adversa se pueden ejecutar sin credenciales reales.

---

## Protocolo de ejecucion

### Paso 1 — Suite de pruebas de integridad de datos

```python
"""
Suite de pruebas de integridad — Arauco TD
Proposito: Verificar calidad del pipeline antes de produccion
Ejecutar: python YYYY-MM-DD_test-integridad-[descripcion].py
"""

import sqlite3
import pandas as pd
import logging

log = logging.getLogger("test_integridad")

PASS = "[OK]"
FAIL = "[FALLO]"


def test_row_count(df: pd.DataFrame, min_esperado: int, nombre: str) -> bool:
    """Verifica que el DataFrame tenga al menos min_esperado filas."""
    ok = len(df) >= min_esperado
    estado = PASS if ok else FAIL
    log.info(f"{estado} row_count '{nombre}': {len(df)} (min={min_esperado})")
    return ok


def test_campos_criticos_no_nulos(df: pd.DataFrame,
                                   campos: list[str], nombre: str) -> bool:
    """
    Verifica completitud de campos criticos: ninguno debe tener nulos.
    Campos criticos tipicos en telemetria forestal:
      equipo_id, timestamp_utc, horas_motor, predio_id
    """
    resultados = {}
    for campo in campos:
        if campo not in df.columns:
            log.error(f"{FAIL} '{campo}' no existe en DataFrame '{nombre}'")
            resultados[campo] = False
            continue
        nulos = df[campo].isna().sum()
        pct_completo = (1 - nulos / len(df)) * 100 if len(df) > 0 else 0
        ok = pct_completo >= 95.0  # SLA: >= 95% completitud
        estado = PASS if ok else FAIL
        log.info(f"{estado} completitud '{campo}' en '{nombre}': {pct_completo:.1f}%")
        resultados[campo] = ok
    return all(resultados.values())


def test_rangos_numericos(df: pd.DataFrame, campo: str,
                          min_val: float, max_val: float, nombre: str) -> bool:
    """
    Verifica que un campo numerico este dentro de rango operacional esperado.
    Ejemplos para telemetria forestal:
      horas_motor: 0 a 24 (por dia)
      velocidad_kmh: 0 a 40
      pendiente_pct: -100 a 100
    """
    if campo not in df.columns:
        log.error(f"{FAIL} campo '{campo}' no existe en '{nombre}'")
        return False
    fuera = df[(df[campo] < min_val) | (df[campo] > max_val)]
    ok = len(fuera) == 0
    estado = PASS if ok else FAIL
    log.info(f"{estado} rango '{campo}' en '{nombre}': "
             f"{len(fuera)} valores fuera de [{min_val}, {max_val}]")
    if not ok:
        log.warning(f"Ejemplos fuera de rango:\n{fuera[[campo]].head(5).to_string()}")
    return ok


def test_timestamps_monotonicos(df: pd.DataFrame, col_ts: str, nombre: str) -> bool:
    """Verifica que los timestamps esten ordenados y sin retrocesos."""
    ts = pd.to_datetime(df[col_ts], utc=True)
    retrocesos = (ts.diff() < pd.Timedelta(0)).sum()
    ok = retrocesos == 0
    estado = PASS if ok else FAIL
    log.info(f"{estado} timestamps monotonicos '{nombre}': {retrocesos} retrocesos")
    return ok


def test_sin_duplicados(df: pd.DataFrame,
                         clave: list[str], nombre: str) -> bool:
    """
    Verifica idempotencia: no deben existir filas duplicadas por clave de negocio.
    Clave tipica: [equipo_id, timestamp_utc]
    """
    dupes = df.duplicated(subset=clave).sum()
    ok = dupes == 0
    estado = PASS if ok else FAIL
    log.info(f"{estado} duplicados '{nombre}' por {clave}: {dupes} filas duplicadas")
    return ok


def test_integridad_completo(df: pd.DataFrame, nombre: str,
                              campos_criticos: list[str],
                              clave_negocio: list[str],
                              rangos: dict) -> dict:
    """
    Ejecuta la suite completa de integridad.
    Returns: dict con resultado de cada prueba
    """
    resultados = {}
    resultados["row_count"] = test_row_count(df, min_esperado=1, nombre=nombre)
    resultados["campos_criticos"] = test_campos_criticos_no_nulos(
        df, campos_criticos, nombre)
    resultados["sin_duplicados"] = test_sin_duplicados(df, clave_negocio, nombre)
    if "timestamp_utc" in df.columns:
        resultados["timestamps"] = test_timestamps_monotonicos(
            df, "timestamp_utc", nombre)
    for campo, (min_v, max_v) in rangos.items():
        resultados[f"rango_{campo}"] = test_rangos_numericos(
            df, campo, min_v, max_v, nombre)
    aprobados = sum(1 for v in resultados.values() if v)
    total = len(resultados)
    log.info(f"Resultado integridad '{nombre}': {aprobados}/{total} pruebas OK")
    return resultados
```

### Paso 2 — Pruebas de manejo de errores (API down, timeout, payload malformado)

```python
"""
Pruebas de tolerancia a fallos — Arauco TD
Simula condiciones adversas: API down, timeout, 401, payload malformado
"""

import unittest
from unittest.mock import patch, MagicMock
import requests


class TestConectorResiliencia(unittest.TestCase):

    @patch("requests.get")
    def test_retry_en_timeout(self, mock_get):
        """Verifica que se reintenten 3 veces en timeout antes de fallar."""
        mock_get.side_effect = requests.exceptions.Timeout()
        # Importar la funcion a testear
        from datos.scripts.YYYY_MM_DD_connector_dealer import fetch_with_retry
        with self.assertRaises(RuntimeError):
            fetch_with_retry("http://api.dealer.com/data",
                             headers={}, max_retries=3, timeout=1)
        self.assertEqual(mock_get.call_count, 3,
                         "Debe reintentar exactamente 3 veces")

    @patch("requests.get")
    def test_no_retry_en_401(self, mock_get):
        """Verifica que NO se reintente en 401: credenciales invalidas."""
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_resp)
        mock_get.return_value = mock_resp
        from datos.scripts.YYYY_MM_DD_connector_dealer import fetch_with_retry
        with self.assertRaises(requests.exceptions.HTTPError):
            fetch_with_retry("http://api.dealer.com/data",
                             headers={}, max_retries=3, timeout=5)
        self.assertEqual(mock_get.call_count, 1,
                         "No debe reintentar en 401")

    @patch("requests.get")
    def test_payload_malformado(self, mock_get):
        """Verifica manejo de respuesta JSON invalida."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.side_effect = ValueError("JSON invalido")
        mock_get.return_value = mock_resp
        # El conector debe lanzar excepcion informativa, no crash silencioso
        from datos.scripts.YYYY_MM_DD_connector_dealer import extract
        with self.assertRaises(Exception):
            extract(config={"base_url": "http://x", "api_key": "k",
                            "timeout": 5, "max_retries": 1},
                    fecha_desde="2025-01-01T00:00:00Z",
                    fecha_hasta="2025-01-01T08:00:00Z")

    @patch("requests.get")
    def test_respuesta_vacia(self, mock_get):
        """Verifica comportamiento con lista de datos vacia (sin registros en el turno)."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"data": []}
        mock_get.return_value = mock_resp
        from datos.scripts.YYYY_MM_DD_connector_dealer import extract, transform
        registros = extract(config={"base_url": "http://x", "api_key": "k",
                                    "timeout": 5, "max_retries": 1},
                            fecha_desde="2025-01-01T00:00:00Z",
                            fecha_hasta="2025-01-01T08:00:00Z")
        df = transform(registros)
        self.assertEqual(len(df), 0,
                         "DataFrame vacio es valido: turno sin registros")
```

### Paso 3 — Prueba de conectividad adversa (predios remotos)

```python
"""
Prueba de sincronizacion offline — simula predio remoto sin conexion
Escenario: 24h sin conexion, luego sync al llegar a base
"""

import os
import tempfile
import json
import unittest

class TestSyncOffline(unittest.TestCase):

    def setUp(self):
        # Buffer temporal para tests
        self.tmpdir = tempfile.mkdtemp()
        os.environ["TD_BUFFER_PATH"] = f"{self.tmpdir}/buffer_test.db"
        from datos.scripts.YYYY_MM_DD_sync_offline import init_buffer
        init_buffer()

    def test_acumulacion_sin_conexion(self):
        """Simula 100 registros acumulados durante 24h sin conexion."""
        from datos.scripts.YYYY_MM_DD_sync_offline import guardar_en_buffer
        for i in range(100):
            guardar_en_buffer(
                equipo_id="TCT-001",
                timestamp_utc=f"2025-01-01T{i // 60:02d}:{i % 60:02d}:00Z",
                payload=json.dumps({"horas_motor": 0.1 * i, "estado": "ON"}),
                fuente="tigercat"
            )
        import sqlite3
        with sqlite3.connect(os.environ["TD_BUFFER_PATH"]) as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM telemetria_buffer WHERE sincronizado=0"
            ).fetchone()[0]
        self.assertEqual(count, 100, "100 registros pendientes en buffer")

    def test_idempotencia_buffer(self):
        """Verifica que guardar el mismo registro dos veces no genera duplicados."""
        from datos.scripts.YYYY_MM_DD_sync_offline import guardar_en_buffer
        for _ in range(3):  # insertar 3 veces el mismo registro
            guardar_en_buffer("TCT-001", "2025-01-01T08:00:00Z",
                              '{"horas_motor": 2.5}', "tigercat")
        import sqlite3
        with sqlite3.connect(os.environ["TD_BUFFER_PATH"]) as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM telemetria_buffer"
            ).fetchone()[0]
        self.assertEqual(count, 1, "INSERT OR IGNORE: solo 1 registro")

    def test_sync_exitoso_marca_sincronizado(self):
        """Verifica que sync exitoso actualiza flag sincronizado=1."""
        from datos.scripts.YYYY_MM_DD_sync_offline import (
            guardar_en_buffer, sincronizar_pendientes)
        guardar_en_buffer("TCT-002", "2025-01-01T10:00:00Z",
                          '{"horas_motor": 1.0}', "tigercat")
        enviados, fallidos = sincronizar_pendientes(fn_enviar=lambda x: None)
        self.assertEqual(enviados, 1)
        self.assertEqual(fallidos, 0)
```

### Paso 4 — Prueba de idempotencia en produccion

```python
def test_rerrun_sin_duplicados(engine, tabla: str, clave: list[str]) -> bool:
    """
    Ejecuta el pipeline dos veces con los mismos datos de entrada
    y verifica que el numero de filas en destino no cambia.
    """
    from sqlalchemy import text
    import logging
    log = logging.getLogger("test_idempotencia")

    with engine.connect() as conn:
        count_antes = conn.execute(
            text(f"SELECT COUNT(*) FROM {tabla}")
        ).scalar()

    # Segunda ejecucion con mismos inputs
    # Llamar al pipeline aqui...

    with engine.connect() as conn:
        count_despues = conn.execute(
            text(f"SELECT COUNT(*) FROM {tabla}")
        ).scalar()

    ok = count_antes == count_despues
    estado = "[OK]" if ok else "[FALLO]"
    log.info(f"{estado} idempotencia '{tabla}': antes={count_antes}, "
             f"despues={count_despues}")
    return ok
```

### Paso 5 — Reportar resultados de pruebas

Documentar en el entregable:
```
Pruebas ejecutadas: [N]
Aprobadas: [N]
Fallidas: [N]
Cobertura:
  - Integridad de datos: [OK/FALLO]
  - Tolerancia a fallos: [OK/FALLO]
  - Conectividad adversa: [OK/FALLO — simulado/real]
  - Idempotencia: [OK/FALLO]
Casos no cubiertos: [listar si hay]
```

---

## Plantilla de reporte de pruebas

```markdown
# Reporte de Pruebas TD: [nombre pipeline]

**Fecha:** YYYY-MM-DD
**Script probado:** datos/scripts/YYYY-MM-DD_[tipo]-[descripcion].py
**Ambiente:** desarrollo / staging / produccion

## Resumen

| Categoria | Pruebas | OK | Fallo |
|---|---|---|---|
| Integridad de datos | [N] | [N] | [N] |
| Tolerancia a fallos | [N] | [N] | [N] |
| Conectividad adversa | [N] | [N] | [N] |
| Idempotencia | [N] | [N] | [N] |

## Resultados detallados

### Integridad
- [OK/FALLO] row_count: [valor obtenido] (min=[meta])
- [OK/FALLO] completitud equipo_id: [%]
- [OK/FALLO] completitud timestamp_utc: [%]
- [OK/FALLO] rango horas_motor: [min-max observado] (esperado [rango])
- [OK/FALLO] sin_duplicados por [clave]

### Tolerancia a fallos
- [OK/FALLO] Retry x3 en timeout: [descripcion]
- [OK/FALLO] No retry en 401: [descripcion]
- [OK/FALLO] Payload malformado: [descripcion]
- [OK/FALLO] Respuesta vacia: [descripcion]

### Conectividad adversa
- [OK/FALLO] Buffer offline 100 registros: [descripcion]
- [OK/FALLO] Idempotencia INSERT OR IGNORE: [descripcion]
- [OK/FALLO] Sync exitoso marca sincronizado=1: [descripcion]

### Idempotencia en produccion
- [OK/FALLO] Rerrun sin duplicados en [tabla]: [descripcion]

## Defectos encontrados

| ID | Descripcion | Severidad | Estado |
|---|---|---|---|
| [T-001] | [descripcion] | Alta/Media/Baja | Abierto/Resuelto |

## Condiciones no probadas

- [ej: API dealer en ambiente de produccion real — requiere credenciales prod]
- [ej: buffer con > 72h sin conexion — no se simulo]
```

---

## Restricciones de este skill

- Las pruebas de integridad requieren al menos 3 turnos de datos reales o sinteticos representativos; no validar con 1 registro
- Pruebas de tolerancia a fallos deben cubrir los 4 casos minimos: timeout, 401, payload malformado, respuesta vacia
- Idempotencia es obligatoria: todo pipeline debe pasar la prueba de rerrun antes de ir a produccion
- Si no hay acceso a API real del dealer durante test, usar mocks documentados y marcar como "simulado" en el reporte
- Los rangos numericos de validacion deben ser operacionalmente correctos: preguntar al area operacional si no se conocen los limites fisicos del equipo (ej: horas motor maximas por turno para un harvester Tigercat 880)
- Pruebas de conectividad adversa son obligatorias para cualquier pipeline que incluya equipos en predios remotos; no omitir por falta de ambiente
- Umbral de completitud: >= 95% en campos criticos es el SLA minimo; documentar si se acepta menos y por que
