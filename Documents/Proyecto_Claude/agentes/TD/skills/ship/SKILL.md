# Skill: ship — Cierre y Entrega de Soluciones TD

## Propósito

Cerrar formalmente la iniciativa de transformación digital: versionar el código, documentar la operación, transferir al equipo de TI o al área responsable, y registrar lecciones aprendidas. Asegura que la solución sea operable por alguien distinto al autor y que el conocimiento técnico no se pierda.

---

## Cuándo usar este skill

- El skill `review` fue completado con decisión de aprobación
- Todos los ajustes críticos identificados en review fueron resueltos
- Se necesita hacer el hand-off formal a TI o al área operacional

**Prerequisito:** review aprobado sin hallazgos críticos pendientes.

---

## Protocolo de ejecución

### Paso 1 — Verificar condiciones de cierre
- [ ] Sin credenciales hardcodeadas, sin bugs críticos de datos
- [ ] Código versionado en git con README completo
- [ ] Variables de entorno documentadas
- [ ] Logs funcionando y rotando correctamente

### Paso 2 — Documentar la solución

**README obligatorio** (`datos/scripts/README-[nombre].md`):
```markdown
# [Nombre del Script / Pipeline / Integración]
**Versión:** v1.0 | **Fecha:** YYYY-MM-DD | **Área:** Transformación Digital

## Qué hace
[1-3 líneas. Sin jerga técnica.]

## Cómo ejecutar
```bash
# Configurar variables de entorno
export API_TOKEN="..."
export SAP_USER="..."

# Ejecutar
python3 datos/scripts/YYYY-MM-DD_etl-[nombre].py
```

## Cómo programar ejecución automática (cron)
```bash
# Ejecutar diariamente a las 06:00
0 6 * * * /usr/bin/python3 /ruta/script.py >> /var/log/arauco-etl.log 2>&1
```

## Qué hacer si falla
1. Revisar log en `/var/log/arauco-etl.log`
2. Verificar conectividad al sistema fuente
3. Contactar: [Nombre responsable TD] — [email/teléfono]

## Variables de entorno requeridas
| Variable | Descripción | Quién la provee |
|---|---|---|
| API_TOKEN | Token de autenticación sistema X | TI Arauco |
| SAP_USER | Usuario SAP para lectura | TI Arauco |

## Dependencias
pip install requests pandas sqlalchemy  (ver requirements.txt)
```

### Paso 3 — Versionar en git
```bash
git add datos/scripts/YYYY-MM-DD_etl-[nombre].py
git add datos/scripts/README-[nombre].md
git commit -m "ship: [nombre-iniciativa] v1.0 — [descripción breve]"
git tag v1.0-[nombre-iniciativa]
```

### Paso 4 — Transferir al área de operación
- Reunión de traspaso con TI (o área responsable de operar el script)
- Entrega de README, variables de entorno y procedimiento de falla
- Confirmar que el responsable operacional puede ejecutar, monitorear y reiniciar el proceso
- Definir canal de soporte para incidentes (quién llama a quién si el pipeline falla)

### Paso 5 — Documentar lecciones aprendidas
- ¿Qué fue más complejo de lo esperado en la integración?
- ¿Qué problemas de datos o de API no estaban en la especificación?
- ¿Qué haría diferente en la arquitectura?
- ¿Qué sistemas tienen APIs mejor o peor documentadas?

### Paso 6 — Entregar
```
datos/YYYY-MM-DD_ship-td-[nombre-iniciativa].md
datos/scripts/README-[nombre].md
```

Reportar al orquestador:
```
ENTREGA TD:
Archivo(s): datos/scripts/YYYY-MM-DD_etl-[nombre].py
Estado: funcional — en operación desde YYYY-MM-DD
Dependencias: [variables de entorno, librerías, accesos requeridos]
Impacto esperado: [qué habilita en el negocio forestal]
```

---

## Plantilla de cierre TD

```markdown
# Cierre de Iniciativa TD — [Nombre]
**Fecha:** YYYY-MM-DD | **Responsable:** [Nombre]

## Resultados finales
| KPI | Meta | Resultado |
|---|---|---|

## Entregables versionados
| Entregable | Archivo | Versión | Tag git |
|---|---|---|---|

## Hand-off técnico
| Actividad | Fecha | Receptor | Confirmado |
|---|---|---|---|
| Reunión de traspaso | | | [ ] |
| Entrega de README | | | [ ] |
| Variables de entorno configuradas | | | [ ] |
| Responsable operacional designado | | [Nombre + cargo] | [ ] |

## Canal de soporte post-cierre
**Incidente nivel 1 (pipeline falla):** [Nombre TD] — [contacto]
**Incidente nivel 2 (datos corruptos):** [Nombre TI] — [contacto]

## Lecciones aprendidas
**Qué fue más complejo:** [lista]
**Problemas no anticipados en spec:** [lista]
**Haría diferente:** [lista]
**APIs mejor documentadas:** [lista] | **Peor documentadas:** [lista]

## Estado: CERRADO ✓
```

---

## Restricciones de este skill

- No cerrar sin README que permita a TI operar el script sin el autor presente
- El responsable operacional debe ser una persona real con nombre y cargo, no "el área de TI"
- Las variables de entorno deben estar documentadas con quién las provee: nadie puede operar algo que no sabe cómo configurar
- La revisión de integridad a 30 días es obligatoria: los pipelines se rompen cuando los sistemas fuente cambian sin aviso
