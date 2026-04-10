# Skill: BPMN 2.0 — Modelamiento de Procesos Forestales

## Propósito

Generar, revisar y editar diagramas de proceso en formato **BPMN 2.0 XML** válido, importable directamente en Bizagi Modeler, Camunda, draw.io o cualquier herramienta compatible con el estándar BPMN 2.0.

Especializado en procesos forestales: cosecha, abastecimiento, transporte, planificación, gestión de contratistas y procesos de mejora continua.

---

## Cuándo usar este skill

- El usuario pide modelar, documentar o rediseñar un proceso
- Se necesita un diagrama AS-IS (proceso actual) o TO-BE (proceso futuro)
- Se entrega un XML `.bpmn` para revisar, corregir o mejorar
- Se requiere análisis de valor (actividades que agregan valor vs. pérdidas)
- Se necesita integrar un proceso con sistemas digitales (SGL, SAP, Planex, etc.)

---

## Protocolo de ejecución

### Paso 1 — Entender el proceso
Antes de modelar, responder:
- ¿Cuál es el evento de inicio y el evento de fin del proceso?
- ¿Quiénes son los participantes (pools) y sus roles (lanes)?
- ¿Cuáles son las actividades principales en secuencia?
- ¿Dónde hay decisiones (gateways: exclusivo, paralelo, inclusivo)?
- ¿Hay subprocesos, procesos de excepción o bucles?
- ¿Qué sistemas digitales intervienen?

### Paso 2 — Clasificar actividades por valor
Para cada actividad identificar:
- **VA** (Valor Agregado al cliente): el cliente pagaría por esto
- **VAN** (Valor Agregado al Negocio): necesario internamente pero no agrega valor directo
- **NVA** (No Agrega Valor / Desperdicio): candidato a eliminar o reducir

### Paso 3 — Generar el XML BPMN 2.0
Usar la estructura estándar definida abajo. Siempre:
- Generar IDs únicos para cada elemento (`sid-` + UUID corto)
- Incluir `<bpmndi:BPMNDiagram>` con coordenadas para renderizado visual
- Validar que cada `sequenceFlow` referencie `sourceRef` y `targetRef` existentes
- Todo gateway exclusivo (XOR) debe tener condición en los flows de salida

### Paso 4 — Entregar
Guardar el archivo como:
```
datos/YYYY-MM-DD_proceso-bpmn-[nombre-proceso].bpmn
```
Acompañar con un documento de análisis:
```
datos/YYYY-MM-DD_analisis-proceso-[nombre-proceso].md
```

---

## Estructura XML BPMN 2.0 — Plantilla base

```xml
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
             xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
             xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
             targetNamespace="http://arauco.com/mejora-continua/bpmn"
             id="Definitions_1">

  <!-- PROCESO PRINCIPAL -->
  <process id="Process_1" name="[Nombre del Proceso]" isExecutable="false">

    <!-- POOL / PARTICIPANTES -->
    <!-- Usar <laneSet> para separar roles dentro de un pool -->
    <laneSet id="LaneSet_1">
      <lane id="Lane_Rol1" name="[Rol 1]">
        <flowNodeRef>StartEvent_1</flowNodeRef>
        <flowNodeRef>Task_1</flowNodeRef>
      </lane>
      <lane id="Lane_Rol2" name="[Rol 2]">
        <flowNodeRef>Task_2</flowNodeRef>
        <flowNodeRef>EndEvent_1</flowNodeRef>
      </lane>
    </laneSet>

    <!-- EVENTO DE INICIO -->
    <startEvent id="StartEvent_1" name="[Disparador del proceso]">
      <outgoing>Flow_1</outgoing>
    </startEvent>

    <!-- TAREAS (tipos: task, userTask, serviceTask, manualTask, scriptTask) -->
    <userTask id="Task_1" name="[Actividad 1]">
      <incoming>Flow_1</incoming>
      <outgoing>Flow_2</outgoing>
    </userTask>

    <!-- GATEWAY EXCLUSIVO (XOR) — solo un camino -->
    <exclusiveGateway id="Gateway_1" name="[¿Condición?]">
      <incoming>Flow_2</incoming>
      <outgoing>Flow_3</outgoing>
      <outgoing>Flow_4</outgoing>
    </exclusiveGateway>

    <!-- GATEWAY PARALELO (AND) — todos los caminos simultáneos -->
    <!-- <parallelGateway id="Gateway_2" name="[Inicio paralelo]"> -->

    <!-- GATEWAY INCLUSIVO (OR) — uno o más caminos -->
    <!-- <inclusiveGateway id="Gateway_3" name="[Al menos uno]"> -->

    <task id="Task_2" name="[Actividad 2 — rama Sí]">
      <incoming>Flow_3</incoming>
      <outgoing>Flow_5</outgoing>
    </task>

    <task id="Task_3" name="[Actividad 3 — rama No]">
      <incoming>Flow_4</incoming>
      <outgoing>Flow_6</outgoing>
    </task>

    <!-- EVENTO DE FIN -->
    <endEvent id="EndEvent_1" name="[Resultado del proceso]">
      <incoming>Flow_5</incoming>
      <incoming>Flow_6</incoming>
    </endEvent>

    <!-- FLUJOS DE SECUENCIA -->
    <sequenceFlow id="Flow_1" sourceRef="StartEvent_1" targetRef="Task_1"/>
    <sequenceFlow id="Flow_2" sourceRef="Task_1" targetRef="Gateway_1"/>
    <sequenceFlow id="Flow_3" name="Sí" sourceRef="Gateway_1" targetRef="Task_2">
      <conditionExpression>${condicion == true}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow id="Flow_4" name="No" sourceRef="Gateway_1" targetRef="Task_3">
      <conditionExpression>${condicion == false}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow id="Flow_5" sourceRef="Task_2" targetRef="EndEvent_1"/>
    <sequenceFlow id="Flow_6" sourceRef="Task_3" targetRef="EndEvent_1"/>

  </process>

  <!-- DIAGRAMA VISUAL (coordenadas para renderizado) -->
  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_1">

      <bpmndi:BPMNShape id="StartEvent_1_di" bpmnElement="StartEvent_1">
        <dc:Bounds x="152" y="82" width="36" height="36"/>
        <bpmndi:BPMNLabel><dc:Bounds x="135" y="125" width="70" height="14"/></bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>

      <bpmndi:BPMNShape id="Task_1_di" bpmnElement="Task_1">
        <dc:Bounds x="250" y="60" width="100" height="80"/>
      </bpmndi:BPMNShape>

      <bpmndi:BPMNShape id="Gateway_1_di" bpmnElement="Gateway_1" isMarkerVisible="true">
        <dc:Bounds x="415" y="75" width="50" height="50"/>
        <bpmndi:BPMNLabel><dc:Bounds x="395" y="132" width="90" height="14"/></bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>

      <bpmndi:BPMNShape id="Task_2_di" bpmnElement="Task_2">
        <dc:Bounds x="530" y="60" width="100" height="80"/>
      </bpmndi:BPMNShape>

      <bpmndi:BPMNShape id="Task_3_di" bpmnElement="Task_3">
        <dc:Bounds x="530" y="200" width="100" height="80"/>
      </bpmndi:BPMNShape>

      <bpmndi:BPMNShape id="EndEvent_1_di" bpmnElement="EndEvent_1">
        <dc:Bounds x="702" y="82" width="36" height="36"/>
        <bpmndi:BPMNLabel><dc:Bounds x="685" y="125" width="70" height="14"/></bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>

      <bpmndi:BPMNEdge id="Flow_1_di" bpmnElement="Flow_1">
        <di:waypoint x="188" y="100"/><di:waypoint x="250" y="100"/>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_2_di" bpmnElement="Flow_2">
        <di:waypoint x="350" y="100"/><di:waypoint x="415" y="100"/>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_3_di" bpmnElement="Flow_3">
        <di:waypoint x="465" y="100"/><di:waypoint x="530" y="100"/>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_4_di" bpmnElement="Flow_4">
        <di:waypoint x="440" y="125"/><di:waypoint x="440" y="240"/><di:waypoint x="530" y="240"/>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_5_di" bpmnElement="Flow_5">
        <di:waypoint x="630" y="100"/><di:waypoint x="702" y="100"/>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_6_di" bpmnElement="Flow_6">
        <di:waypoint x="630" y="240"/><di:waypoint x="720" y="240"/><di:waypoint x="720" y="118"/>
      </bpmndi:BPMNEdge>

    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>

</definitions>
```

---

## Tipos de elementos BPMN más usados en procesos forestales

| Elemento | Tipo BPMN | Cuándo usarlo |
|---|---|---|
| Inicio de temporada cosecha | `startEvent` (timer) | Proceso que inicia en fecha/hora definida |
| Revisión de supervisor | `userTask` | Actividad manual con responsable humano |
| Generación de reporte SGL | `serviceTask` | Actividad ejecutada por sistema (SGL, SAP) |
| Transporte de madera | `manualTask` | Actividad física sin soporte de sistema |
| ¿Cumple volumen planificado? | `exclusiveGateway` | Decisión con una sola salida posible |
| Inicio de procesos paralelos | `parallelGateway` | Volteo y madereo simultáneos |
| Notificación de falla | `intermediateThrowEvent` (message) | Envío de alerta a otro proceso |
| Subproceso de habilitación | `subProcess` | Proceso interno colapsado |
| Proceso de contratista externo | Pool separado | Participante externo a la organización |

---

## Integración con sistemas digitales forestales

Cuando el proceso interactúa con sistemas, usar `serviceTask` y anotar el sistema en el nombre:

```xml
<serviceTask id="Task_SGL" name="Registrar pérdida en SGL">
  <!-- Integración: SGL API REST -->
</serviceTask>
<serviceTask id="Task_SAP" name="Generar OT en SAP PM">
  <!-- Integración: SAP PM BAPI -->
</serviceTask>
```

Sistemas a referenciar según contexto: SGL, SAP PM/MM, Planex, Planex NOM, Opticort, Opti-Maq, Forest Gantt, Forest Data 2.0, Datalake, Telemetría de Máquinas.

---

## Documento de análisis que acompaña cada diagrama

El archivo `.md` de análisis debe incluir:

```markdown
# Análisis de Proceso: [Nombre]
**Fecha:** YYYY-MM-DD
**Área responsable:** Excelencia Operacional
**Versión:** AS-IS / TO-BE

## Resumen ejecutivo
[Descripción del proceso y su propósito en 3-5 líneas]

## Participantes
| Pool/Lane | Rol | Responsabilidades principales |
|---|---|---|

## Análisis de valor
| ID Actividad | Nombre | Tipo (VA/VAN/NVA) | Tiempo estimado | Observación |
|---|---|---|---|---|

## Pérdidas identificadas
[Lista de actividades NVA con impacto estimado]

## Mejoras propuestas (si es AS-IS)
[Lista de cambios para el TO-BE con impacto esperado]

## KPIs del proceso
| KPI | Fórmula | Meta | Frecuencia |
|---|---|---|---|
```

---

## Instrucciones para importar en Bizagi

1. Guardar el archivo con extensión `.bpmn`
2. En Bizagi Modeler: **File → Import → BPMN File**
3. Seleccionar el archivo generado
4. Ajustar posiciones visuales si es necesario (las coordenadas son aproximadas)
5. Exportar desde Bizagi a PDF o PNG para presentaciones

**Nota:** Bizagi puede agregar propiedades adicionales (formas, colores, documentación) que no afectan la validez del XML BPMN 2.0 subyacente.
