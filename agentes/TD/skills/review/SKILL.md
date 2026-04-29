# Skill: review — Seguridad, idempotencia en producción y calidad end-to-end

> **Agente:** TD — Transformación Digital

## Propósito

Auditar el pipeline o conector antes de entregarlo a produccion: verificar que las credenciales y datos sensibles estan protegidos, que el pipeline es seguro ante rerun, que la calidad de datos cumple el SLA acordado en `spec`, y que el codigo es mantenible por el equipo de TI de Arauco sin soporte continuo del agente TD.

## Cuándo usar este skill

- El pipeline paso las pruebas de `test` y esta listo para revision final antes de produccion
- El orquestador solicita aval tecnico antes del hand-off a TI
- Se detecta un incidente en produccion y se necesita auditoria retrospectiva
- Un script existente va a ser modificado y se requiere revision de impacto

**Prerequisito:** Reporte de pruebas (`test`) aprobado con los 4 tipos de prueba cubiertos. Sin evidencia de pruebas, la revision no puede concluir estado "apto para produccion".

---

## Protocolo de ejecucion

### Paso 1 — Auditoria de seguridad

Leer el codigo fuente del script con `read_file` y revisar los siguientes puntos en orden:

**1a. Credenciales y tokens**

```python
# Buscar patrones de credenciales hardcodeadas
import ast
import sys

def audit_credenciales(filepath: str) -> list[str]:
    """
    Detecta posibles credenciales hardcodeadas en codigo Python.
    Retorna lista de advertencias.
    """
    advertencias = []
    patrones_sospechosos = [
        "password", "passwd", "secret", "token", "api_key",
        "apikey", "bearer", "authorization", "credential",
    ]
    with open(filepath, encoding="utf-8") as f:
        contenido = f.read()

    lineas = contenido.splitlines()
    for i, linea in enumerate(lineas, 1):
        linea_lower = linea.lower()
        for patron in patrones_sospechosos:
            if patron in linea_lower and "=" in linea and "os.environ" not in linea:
                if not linea.strip().startswith("#"):
                    advertencias.append(
                        f"Linea {i}: posible credencial hardcodeada — '{linea.strip()[:80]}'"
                    )
    return advertencias
```

Verificar manualmente:
- [ ] No hay strings literales que parezcan tokens, contrasenas o API keys
- [ ] Toda credencial se lee de `os.environ` o de un vault/secrets manager
- [ ] No hay archivos `.env` ni JSON con credenciales en el repositorio git
- [ ] `.gitignore` excluye `.env`, `*.key`, `secrets/`, `credenciales/`

**1b. Permisos de acceso a datos**

- [ ] El script solo accede a los sistemas declarados en el `spec`
- [ ] Credenciales usadas tienen permisos minimos: solo lectura en fuente, solo escritura en tabla/endpoint destino
- [ ] No se accede a tablas SAP de RRHH, Finanzas o datos personales sin autorizacion explicita

**1c. Datos sensibles en logs**

```python
# Verificar que logs no exponen tokens ni datos sensibles
# Patron correcto:
log.info(f"Autenticando en {config['base_url']} con clave terminada en ...{config['api_key'][-4:]}")

# Patron incorrecto (nunca):
log.debug(f"Headers: {headers}")  # expone token completo
log.info(f"Config completa: {config}")  # expone api_key
```

- [ ] Logs no incluyen tokens ni contrasenas completas
- [ ] Logs no incluyen payloads completos que puedan contener datos operacionales sensibles

### Paso 2 — Auditoria de idempotencia en produccion

Revisar cada punto de escritura en el pipeline:

**Base de datos SQLite / SQL:**
```python
# Correcto: INSERT OR IGNORE o UPSERT
conn.execute("INSERT OR IGNORE INTO tabla (...) VALUES (...)")
df.to_sql("tabla", engine, if_exists="append",
          method=lambda table, conn, keys, data_iter: ...,  # custom upsert
          index=False)

# Incorrecto para produccion:
df.to_sql("tabla", engine, if_exists="replace")  # borra toda la tabla
df.to_sql("tabla", engine, if_exists="append")   # sin control de duplicados
```

**API de destino (Forest Data 2.0, SGL):**
- [ ] El endpoint de carga acepta re-envio? (POST idempotente o PUT con ID?)
- [ ] Si POST no es idempotente: deduplicar en el script antes de enviar

Checklist de idempotencia:
- [ ] Rerrun con mismos datos no aumenta row count en destino
- [ ] Rerrun con datos parcialmente nuevos solo inserta los nuevos
- [ ] Fallo en mitad del pipeline no deja datos parciales sin marcar

### Paso 3 — Calidad de datos end-to-end (SLA)

Verificar que los KPIs de integracion definidos en `spec` se cumplen con datos reales:

```python
"""
Verificacion de SLA de integracion — post build
Compara KPIs comprometidos en spec vs. resultados reales de las pruebas
"""

def verificar_sla(resultados_test: dict, sla: dict) -> dict:
    """
    resultados_test: dict con metricas reales
      {
        'latencia_min': 12,          # minutos promedio
        'completitud_pct': 97.3,
        'tasa_error_pct': 0.8,
        'tiempo_recuperacion_turnos': 0.5,
      }
    sla: dict con metas del spec
      {
        'latencia_min': 30,
        'completitud_pct': 95.0,
        'tasa_error_pct': 2.0,
        'tiempo_recuperacion_turnos': 1.0,
      }
    Returns: dict con estado por KPI
    """
    resultado = {}
    for kpi, meta in sla.items():
        real = resultados_test.get(kpi)
        if real is None:
            resultado[kpi] = {"estado": "NO_MEDIDO", "real": None, "meta": meta}
            continue
        # Latencia, tasa de error, tiempo de recuperacion: real <= meta es OK
        # Completitud: real >= meta es OK
        if "completitud" in kpi:
            ok = real >= meta
        else:
            ok = real <= meta
        resultado[kpi] = {
            "estado": "OK" if ok else "INCUMPLE",
            "real": real,
            "meta": meta,
        }
    return resultado
```

Revisar para cada KPI del `spec`:
- Latencia de entrega: tiempo real desde generacion hasta disponibilidad en destino
- Completitud: % de campos criticos sin nulos en los ultimos 3 turnos
- Frecuencia: desviacion real vs. cadencia acordada (ej: cada turno = 8h)
- Tasa de error: % de llamadas que fallaron vs. total

### Paso 4 — Revision de mantenibilidad

El codigo va a ser mantenido por TI de Arauco, no por el agente TD. Criterios:

**Estructura:**
- [ ] Funciones nombradas descriptivamente (`extract_tigercat`, no `func1`)
- [ ] Docstring en cada funcion con proposito, inputs y outputs
- [ ] Constantes nombradas (no magic numbers ni magic strings)
- [ ] Modulo con punto de entrada claro (`if __name__ == "__main__":`)

**Dependencias:**
- [ ] `requirements.txt` o comentario con versiones exactas en el script
- [ ] Sin dependencias innecesarias (no instalar `numpy` si solo se usa `pandas`)
- [ ] Compatible con Python 3.10+

**Operabilidad:**
- [ ] Variables de entorno documentadas en comentario al inicio del script
- [ ] Logging con nivel INFO por defecto; DEBUG solo activable via variable de entorno
- [ ] Mensajes de log en espanol (mismo idioma que el equipo operacional)
- [ ] Archivo de log con rotacion: no crece indefinidamente

**Conectividad forestal:**
- [ ] Timeout configurado (no usar valor por defecto de `requests` que es None)
- [ ] Comportamiento documentado cuando no hay conexion en predio remoto
- [ ] Buffer local o mecanismo de reintento documentado

### Paso 5 — Producir el informe de revision

```
datos/YYYY-MM-DD_review-[descripcion].md
```

---

## Plantilla de informe de revision

```markdown
# Revision TD: [nombre pipeline]

**Fecha:** YYYY-MM-DD
**Script revisado:** datos/scripts/YYYY-MM-DD_[tipo]-[descripcion].py
**Revisor:** TD
**Estado final:** APROBADO / APROBADO CON OBSERVACIONES / RECHAZADO

---

## 1. Seguridad

| Aspecto | Estado | Observacion |
|---|---|---|
| Sin credenciales hardcodeadas | OK / FALLO | [detalle si fallo] |
| Permisos minimos en sistemas | OK / FALLO | [accesos auditados] |
| Logs sin datos sensibles | OK / FALLO | [lineas problematicas si hay] |
| .gitignore cubre archivos sensibles | OK / FALLO | [detalle] |

## 2. Idempotencia

| Punto de escritura | Mecanismo | Estado |
|---|---|---|
| [tabla/endpoint] | INSERT OR IGNORE / UPSERT / PUT | OK / FALLO |

## 3. SLA de integracion (vs. spec)

| KPI | Meta (spec) | Real (test) | Estado |
|---|---|---|---|
| Latencia de entrega | [meta] | [real] | OK / INCUMPLE |
| Completitud campos criticos | [meta %] | [real %] | OK / INCUMPLE |
| Tasa de error | [meta %] | [real %] | OK / INCUMPLE |
| Tiempo de recuperacion | [meta] | [real] | OK / INCUMPLE |

## 4. Mantenibilidad

| Criterio | Estado | Observacion |
|---|---|---|
| Docstrings en funciones | OK / PARCIAL / FALLO | [funciones sin docstring] |
| Variables de entorno documentadas | OK / FALLO | [variables no documentadas] |
| Timeout configurado | OK / FALLO | [llamadas sin timeout] |
| Logging operacional en espanol | OK / PARCIAL | [lineas en ingles si hay] |
| requirements o dependencias declaradas | OK / FALLO | |

## 5. Observaciones abiertas

| ID | Tipo | Descripcion | Severidad | Bloquea entrega |
|---|---|---|---|---|
| [R-001] | Seguridad/Idempotencia/SLA/Manten. | [descripcion] | Alta/Media/Baja | Si/No |

## 6. Veredicto

**APROBADO** — El pipeline cumple todos los criterios minimos para produccion.

**APROBADO CON OBSERVACIONES** — Puede ir a produccion pero se requiere resolver [R-00X] en plazo [N dias].

**RECHAZADO** — Requiere correccion en build antes de revision nueva. Motivos: [lista].
```

---

## Restricciones de este skill

- Un "RECHAZADO" en seguridad (credencial hardcodeada, log con token completo) bloquea el pipeline: no puede ir a produccion
- Un "FALLO" en idempotencia bloquea el pipeline si el destino es una base de datos compartida o Forest Data 2.0
- SLA incumplido en completitud (< 95%) con datos reales: debe reportarse al orquestador y al area operacional antes de aprobar
- La revision no reemplaza las pruebas de `test`: si no hay reporte de pruebas, la revision no puede emitir estado "APROBADO"
- Mantenibilidad es obligatoria: codigo sin docstrings o sin variables de entorno documentadas es "APROBADO CON OBSERVACIONES" como minimo
- Revisar el `.gitignore` activo del repositorio, no asumir que existe o que cubre los archivos correctos
- Credenciales de dealers (Tigercat, John Deere, Caterpillar, Volvo, Develon, Liebherr, Ecoforst) tienen distinto ciclo de rotacion: algunos proveedores rotan tokens cada 30 dias sin aviso; el pipeline debe documentar como detecta y reacciona a un 401 inesperado
