# Análisis de Proceso: Gestión de Producción de Contratistas
**Fecha:** 2026-04-09
**Área responsable:** Excelencia Operacional
**Versiones:** AS-IS y TO-BE

---

## Resumen ejecutivo

El proceso de Gestión de Producción de Contratistas gestiona el ciclo completo desde la creación del contrato hasta la emisión del memo de avance para pago. Involucra 8 roles: Área Contratos, Líder de Operaciones, Encargado Cosecha, dos analistas (Logístico y Valorizado), Analista Terreno, Jefe Producción Contratista y el Contratista. El AS-IS presenta 3 fases con ~40% de actividades clasificadas como NVA, principalmente por falta de integración entre sistemas, captura de datos no estandarizada y retrabajo recurrente. El TO-BE elimina 7 actividades NVA puras y automatiza 3 tareas manuales.

---

## Participantes

| Pool/Lane | Rol | Responsabilidades principales |
|---|---|---|
| Área Contratos | Gestor de contratos | Crear y formalizar el contrato con el contratista |
| Líder de Operaciones | Supervisor operacional | Notificar producción diaria; monitorear cumplimiento |
| Encargado Cosecha | Operador de terreno | Registrar producción en actas |
| Analista C. Producción Logístico | Analista de datos | Validar NOC, procesar inventario, generar pedidos |
| Analista C. Producción Valorizado | Analista de valorización | Crear contratos en sistemas, valorizar producción, emitir reporte |
| Analista C. Producción Terreno | Analista de terreno | Cerrar actas de producción |
| Jefe Producción Contratista | Aprobador | Validar y aprobar el valorizado mensual |
| Contratista / Contratante | Receptor | Recibir memo de avance para pago |

---

## Análisis de valor — AS-IS

| ID Actividad | Nombre | Tipo | Observación |
|---|---|---|---|
| Task_GenerarContrato | Generar contrato | VAN | Necesario internamente; no agrega valor al cliente |
| Task_CreacionActas | Creación de actas | VA | Core del registro de producción |
| Task_CreacionContratoSAP | Creación contrato SAP | VAN | Entrada manual en sistema; automatizable |
| Task_CreacionContratoMA | Creación contrato MA | VAN | Duplica entrada anterior en otro sistema |
| Task_CreacionContratoCDH | Creación contrato CDH | VAN | Tercera entrada manual del mismo contrato |
| Task_NotificarProduccion | Notificar producción diaria | VAN | Automatizable con trigger de sistema |
| Task_ValidacionNOC | Validación Acta/NOC | VA | Control clave de calidad del dato |
| Task_Revision | Revisión | NVA | Retrabajo causado por datos de origen no estandarizados |
| Task_EliminaDuplicado | Eliminación de duplicado | NVA | Desperdicio puro — error de origen en captura |
| Task_CorreccionDesvio | Corrección de desvío | NVA | Retrabajo por error de captura en terreno |
| Task_SaleInventario | Sale de inventario (Tendencia) | NVA | Ajuste por desvío sistemático |
| Task_ProcesoInventario | A proceso de inventario | VAN | Automatizable |
| Task_PreliminarNOC | Preliminar Acta/NOC | VA | Consolidación necesaria para pedidos |
| Task_CreacionPedidos | Creación pedidos | VAN | Automatizado pero dependiente de calidad upstream |
| Task_CuadraturaInterna | Cuadratura interna sistemas | NVA | Señal clara de falta de integración entre SAP, MA y CDH |
| Task_ReasignaNotificacion | Reasigna notificación | NVA | Retrabajo por cuadratura fallida |
| Task_GestionModificacionesVMA | Gestión modificaciones VMA | VAN | Excepcional; necesario cuando cambian tarifas |
| Task_ActualizaVariables | Actualiza variables | VA | Parte del ciclo de valorización |
| Task_CalculaTarifas | Calcula tarifas | VA | Cálculo esencial para pago correcto |
| Task_ConciliaProduccion | Concilia producción | VA | Control de coherencia entre sistemas |
| Task_ValoraProduccion | Valora producción | VA | Actividad central del proceso |
| Task_RevisaEEGMM | Revisa EEGMM (Excel) | NVA | Excel manual: riesgo de error, sin trazabilidad, sin control de versión |
| Task_TramitaErrores | Tramitar errores | NVA | Consecuencia directa de mala calidad del dato upstream |
| Task_DaVoBo | Dar VoBo valorizado | VAN | Control necesario antes de emisión |
| Task_EnviaReportes | Envía reportes | VAN | Distribución del resultado |
| Task_CierreActas | Cierre de actas | VA | Formalización del período productivo |
| Task_AprobacionValorizado | Aprobación valorizado | VAN | Validación final antes de pago |
| Task_GeneraMemoAvance | Generar memo de avance | VA | Hito de pago al contratista |

**Resumen AS-IS:** 8 VA | 10 VAN | 7 NVA (32% de actividades son desperdicio puro)

---

## Pérdidas identificadas (AS-IS)

| # | Actividad NVA | Causa raíz | Impacto estimado |
|---|---|---|---|
| 1 | Revisión + 3 ramas (Duplicado / Desvío / Tendencia) | Captura de datos no estandarizada en terreno | 3-4 h analista/día en correcciones |
| 2 | Cuadratura interna sistemas (mensual) | Sin integración en tiempo real SAP↔MA↔CDH | 1-2 días/mes de conciliación manual |
| 3 | Reasigna notificación | Consecuencia directa de cuadratura fallida | 0,5-1 día/mes adicional |
| 4 | Revisa EEGMM (Excel) | Sin reporte automático integrado a SAP | Riesgo de error en valorización; sin trazabilidad |
| 5 | Tramitar errores | Calidad del dato insuficiente en fases previas | Variable; hasta 3 días/mes en meses complejos |

---

## Mejoras aplicadas en TO-BE

| # | Mejora | Actividades eliminadas | Actividades nuevas | Impacto esperado |
|---|---|---|---|---|
| **M1** | Captura digital estandarizada en actas | Task_Revision, Task_EliminaDuplicado, Task_CorreccionDesvio, Task_SaleInventario | Task_CreacionActasDigital (formulario digital con validación en origen) | -4 actividades NVA; errores en NOC ≈0 |
| **M2** | Integración en tiempo real SAP↔MA↔CDH | Task_CuadraturaInterna, Task_ReasignaNotificacion | Task_IntegracionSistemas (serviceTask automático post-creación contrato) | -2 actividades NVA; 2 días/mes recuperados |
| **M3** | Reporte automático SAP / Power BI | Task_RevisaEEGMM | Task_GeneraReporteSAP (serviceTask con extracción directa de SAP) | Elimina riesgo de error Excel; trazabilidad 100% |
| **M4** | Consolidar eventos de fin | 5 endEvents dispersos | 2 endEvents: End_ProcesoOK y End_Excepcion | Proceso más claro y controlable |
| **M5** | Corrección única estandarizada | 3 ramas de desvío → 1 rama simple | Task_CorreccionEstandar (asistida por sistema) | Flujo lineal; menor tiempo de resolución |

---

## Análisis de valor — TO-BE

| ID Actividad | Nombre | Tipo | Cambio vs AS-IS |
|---|---|---|---|
| Task_GenerarContrato | Generar contrato | VAN | Sin cambio |
| Task_CreacionActasDigital | Creación de actas (digital) | VA | **MEJORADO** — formulario digital elimina errores de origen |
| Task_CreacionContratoSAP | Crear contrato SAP | VAN | **AUTOMATIZADO** — serviceTask vía API |
| Task_CreacionContratoMA | Crear contrato MA | VAN | **AUTOMATIZADO** |
| Task_CreacionContratoCDH | Crear contrato CDH | VAN | **AUTOMATIZADO** |
| Task_IntegracionSistemas | Sincronización SAP↔MA↔CDH | VAN | **NUEVO** — elimina cuadratura mensual |
| Task_NotificarProduccion | Notificar producción diaria | VAN | **AUTOMATIZADO** |
| Task_ValidacionNOC | Validación Acta/NOC | VA | Sin cambio — mantiene control clave |
| Task_CorreccionEstandar | Corrección estandarizada | NVA residual | **REDUCIDO** — 1 rama vs 3; asistida por sistema |
| Task_ProcesoInventario | Proceso de inventario | VAN | **AUTOMATIZADO** |
| Task_PreliminarNOC | Preliminar Acta/NOC | VA | Sin cambio |
| Task_CreacionPedidos | Creación pedidos | VAN | Sin cambio |
| Task_GestionModificacionesVMA | Gestión modificaciones VMA | VAN | Sin cambio (excepcional) |
| Task_ActualizaVariables | Actualiza variables | VA | Sin cambio |
| Task_CalculaTarifas | Calcula tarifas | VA | Sin cambio |
| Task_CierreActas | Cierre de actas | VA | Sin cambio |
| Task_ConciliaProduccion | Concilia producción | VA | Sin cambio |
| Task_ValoraProduccion | Valora producción | VA | Sin cambio |
| Task_GeneraReporteSAP | Generar reporte SAP / Power BI | VAN | **NUEVO** — reemplaza Excel EEGMM |
| Task_TramitaErrores | Tramitar errores | NVA residual | **REDUCIDO** — menor frecuencia esperada |
| Task_DaVoBo | Dar VoBo valorizado | VAN | Sin cambio |
| Task_EnviaReportes | Envía reportes | VAN | Sin cambio |
| Task_AprobacionValorizado | Aprobación valorizado | VAN | Sin cambio |
| Task_GeneraMemoAvance | Generar memo de avance | VA | Sin cambio |

**Resumen TO-BE:** 8 VA | 12 VAN | 2 NVA residual (8% de actividades, vs 32% AS-IS)

---

## KPIs del proceso

| KPI | Fórmula | Meta TO-BE | Frecuencia | Fuente |
|---|---|---|---|---|
| Tasa de rechazo NOC | (Actas rechazadas / Total actas) × 100 | < 2% | Diaria | Sistema NOC / SGL |
| Tiempo de cuadratura mensual | Horas dedicadas a conciliación SAP↔MA↔CDH | 0 h (automatizado) | Mensual | SAP / Log integración |
| Tiempo ciclo valorización | Días desde cierre de actas hasta memo de avance | ≤ 5 días hábiles | Mensual | SAP / Power BI |
| Errores en valorizado | N° de diferencias detectadas en GW_ExistenDiferencias | < 3 por ciclo | Mensual | SAP |
| Actividades NVA ejecutadas | N° de actividades NVA activas en el proceso | ≤ 2 | Trimestral | Auditoría EO |

---

## Plan de acción — Implementación TO-BE

| Acción | Responsable | Plazo | Criterio de cierre |
|---|---|---|---|
| M1: Diseñar formulario digital de actas con validaciones obligatorias | Analista TD + Encargado Cosecha | 2026-05-15 | Formulario live con 0 campos libres en campos críticos |
| M2: Desarrollar integración SAP↔MA↔CDH (API o ETL) | Área TD | 2026-06-30 | Cuadratura manual eliminada; log de sincronización activo |
| M3: Configurar reporte automático SAP/Power BI | Analista Valorizado + TD | 2026-05-30 | Reporte generado automáticamente al cierre del ciclo |
| M4/M5: Actualizar proceso en Bizagi y capacitar roles | EO | 2026-07-15 | 100% de participantes capacitados; proceso TO-BE documentado y aprobado |

---

## Archivos asociados

| Archivo | Descripción |
|---|---|
| `2026-04-09_proceso-bpmn-gestion-produccion-contratistas-as-is.bpmn` | Diagrama BPMN 2.0 AS-IS — importable en Bizagi |
| `2026-04-09_proceso-bpmn-gestion-produccion-contratistas-to-be.bpmn` | Diagrama BPMN 2.0 TO-BE — importable en Bizagi |
| `2026-04-09_analisis-proceso-gestion-produccion-contratistas.md` | Este documento |
