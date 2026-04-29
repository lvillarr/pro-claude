# Skill: ship — Entrega ejecutiva final al usuario

> **Agente:** Orquestador — Subgerente de Mejora Continua

## Proposito

Convertir la sintesis validada en un entregable ejecutivo listo para el usuario: contexto, hallazgos clave, recomendaciones y proximos pasos. Cada entregable incluye fecha, area responsable, impacto cuantificado y proximo paso con dueño y plazo.

## Cuando usar

- Revision (`review`) con estado APROBADA o APROBADA CON OBSERVACIONES sin bloqueos
- El usuario solicita el resultado de la iniciativa
- Se cierra un ciclo completo de orquestacion (spec → plan → agentes → review → ship)
- Se necesita presentar resultados de una iniciativa en curso a gerencia o jefatura

**Prerequisito:** `orquestador/skills/review/SKILL.md` ejecutado con estado APROBADA. Sin revision aprobada, no hay ship: el usuario podria recibir informacion con inconsistencias o campos obligatorios faltantes.

## Protocolo

### Paso 1 — Seleccionar el formato segun audiencia

| Audiencia | Formato | Extension | Largo maximo |
|---|---|---|---|
| Gerencia / Directorio | Informe ejecutivo | `.docx` o `.md` | 2 paginas |
| Subgerencia / Jefatura | Informe gerencial | `.docx` o `.md` | 5 paginas |
| Equipo tecnico / Operaciones | Informe tecnico | `.md` o `.html` | Sin limite |
| Presentacion a comite | Presentacion | `.pptx` | 8-12 diapositivas |

El formato lo define el brief. Si no fue especificado: usar `.md` gerencial por defecto.

### Paso 2 — Estructurar el entregable con el marco ejecutivo

Estructura obligatoria de todo entregable ejecutivo:

```
1. CONTEXTO          — situacion y periodo analizado
2. HALLAZGOS CLAVE   — maximos 3-5, cuantificados, con fuente
3. RECOMENDACIONES   — jerarquizadas por impacto, con responsable implicito
4. PROXIMOS PASOS    — accionables, con dueño (cargo) y plazo
5. ANEXOS (si aplica) — datos de soporte, tablas, graficos
```

Esta secuencia sigue la piramide Minto. No invertirla.

### Paso 3 — Cuantificar el impacto en lenguaje de negocio forestal

Cada hallazgo y cada recomendacion debe tener una cifra de impacto expresada en unidades relevantes para Arauco:

| Dimension | Unidades preferidas |
|---|---|
| Produccion | m³/mes, ton/mes, ton celulosa/dia |
| Eficiencia | OEE %, h disponibles/mes, h perdidas/mes |
| Costo logistico | $/m³, $/ton, CLP/viaje, CLP/km |
| Financiero agregado | EBITDA CLP/mes, costo operacional CLP/mes |
| Tiempo | h/turno, dias/mes, semanas de retraso |
| Superficie | ha, ha/temporada |

Si no hay cifra real con fuente: indicar "impacto pendiente de cuantificar — requiere [dato especifico]". No inventar magnitudes.

### Paso 4 — Jerarquizar recomendaciones por impacto y urgencia

Cada recomendacion sigue la estructura:

```
[N]. [Verbo de accion] [objeto] [cuantificacion del impacto]
   Responsable: [cargo — no nombre propio]
   Plazo: [fecha especifica o "dentro de N semanas"]
   Insumo necesario: [que se necesita para ejecutar esta recomendacion]
```

Ordenar de mayor a menor impacto esperado. Si hay mas de 5 recomendaciones, agrupar las menores en "Acciones complementarias".

### Paso 5 — Declarar limitaciones del analisis

Todo entregable ejecutivo debe incluir una seccion de limitaciones. No omitirla aunque parezca debilitar las conclusiones: ocultar limitaciones genera decisiones mal informadas.

Formato minimo:

```
LIMITACIONES:
- [Cobertura de datos: periodo, sistemas o lineas sin informacion]
- [Supuestos: hipotesis no verificadas que podrian cambiar las conclusiones]
- [Precision: rangos de incertidumbre en cifras clave]
```

### Paso 6 — Generar el archivo entregable

```
datos/YYYY-MM-DD_[tipo]-[descripcion].md   (o .docx / .pptx segun brief)
```

Para `.docx` o `.pptx`: usar `python-docx` / `python-pptx` via `bash` con branding Arauco.

### Paso 7 — Presentar al usuario con mensaje de cierre

El mensaje de cierre al usuario (no el archivo) tiene maximo 5 lineas:
1. Que se hizo y que se encontro (1 linea)
2. Recomendacion principal (1 linea)
3. Proximo paso mas urgente con dueño y plazo (1 linea)
4. Ruta del entregable (1 linea)
5. Limitacion principal si es material (1 linea — opcional)

### Paso 8 — Actualizar `tasks/lessons.md` si aplica

Si en este ciclo hubo alguna correccion del usuario (hipotesis erronea, delegacion incorrecta, output rechazado, inconsistencia no anticipada): registrar la leccion antes de cerrar.

```
### [YYYY-MM-DD] Leccion: <titulo breve>
**Que salio mal:** <descripcion concisa>
**Causa raiz:** <por que ocurrio>
**Regla nueva:** <que hacer diferente la proxima vez>
**Aplica a:** [delegacion / spec / sintesis / validacion]
```

## Plantilla de Entregable Ejecutivo

```markdown
# [Titulo del informe]

**Fecha:** YYYY-MM-DD
**Area responsable:** Subgerencia de Mejora Continua — [area especifica]
**Elaborado por:** Orquestador (Arauco Mejora Continua)
**Audiencia:** [Gerencia / Subgerencia / Jefatura]
**Fuentes:** [arauco_mc.db / datos/YYYY-MM-DD_archivo.ext / SGL / SAP PM]

---

## Contexto

[2-3 lineas: que se analizo, en que periodo, en que area. Lo que el receptor ya sabe o necesita saber para leer el informe.]

---

## Hallazgos clave

1. **[Hallazgo 1 — cuantificado]**
   [1-2 lineas de respaldo. Fuente: [sistema / archivo]. Periodo: [YYYY-MM a YYYY-MM].]

2. **[Hallazgo 2 — cuantificado]**
   [1-2 lineas de respaldo. Fuente: [sistema / archivo].]

3. **[Hallazgo 3 — cuantificado]** (si aplica)
   [1-2 lineas de respaldo.]

> Los valores siguen formato numerico chileno: `1.234,5 h`, `87,3%`, `$12.500 CLP/ton`.

---

## Recomendaciones

| Prioridad | Recomendacion | Impacto estimado | Responsable | Plazo |
|---|---|---|---|---|
| 1 | [accion especifica] | [magnitud en unidad de negocio] | [cargo] | [fecha] |
| 2 | [accion especifica] | [magnitud] | [cargo] | [fecha] |
| 3 | [accion especifica] | [magnitud o "pendiente de cuantificar"] | [cargo] | [fecha] |

---

## Proximos pasos

| Paso | Responsable | Plazo | Criterio de cierre |
|---|---|---|---|
| [accion concreta e inmediata] | [cargo] | [fecha] | [como sabemos que esta hecho] |
| [accion siguiente] | [cargo] | [fecha] | [criterio binario] |
| [seguimiento] | [cargo — Subgerente MC] | [fecha — 30/60/90 dias] | [KPI o hito de sostenibilidad] |

---

## Limitaciones

- **Cobertura de datos:** [periodos o sistemas sin cobertura completa]
- **Supuestos:** [hipotesis que no fue posible verificar con datos disponibles]
- **Precision:** [rangos o estimaciones aproximadas en cifras clave]

---

## Anexos (si aplica)

- Anexo 1: [descripcion] — datos/YYYY-MM-DD_[archivo].ext
- Anexo 2: [descripcion] — datos/YYYY-MM-DD_[archivo].ext
```

## Restricciones

- No emitir entregable sin revision en estado APROBADA: el usuario no debe recibir outputs con inconsistencias ni campos del Paso 3.5 faltantes
- Hallazgos sin cifra con fuente: no presentarlos como hallazgo; presentarlos como "hipotesis pendiente de validar con [dato especifico]"
- Recomendaciones sin responsable de cargo: no son recomendaciones validas; "el area" no es un responsable
- Proximos pasos sin plazo: no son accionables; si el plazo es incierto, indicar "sujeto a disponibilidad de [insumo]"
- Limitaciones no son opcionales: todo entregable tiene alguna limitacion real; si el campo esta vacio, es una señal de que no se analizaron las restricciones del analisis
- Impacto en EBITDA u otras cifras financieras agregadas: solo incluir si hay tasa de conversion real (costo por hora de parada, precio ton, costo logistico unitario) con fuente; no usar benchmarks de industria sin citar origen verificable
- El mensaje de cierre al usuario (no el archivo) debe ser breve: maximo 5 lineas; el detalle esta en el archivo, no en el chat
- Nunca declarar "listo" o "perfecto": si no se puede verificar algo, indicarlo como limitacion o incertidumbre pendiente
