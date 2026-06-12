# web_chat.html — Quick Start Guide

## Abrir el archivo

```bash
# Opción 1: Direct (local)
open /Users/lucianovillarroelparra/telegram-bot/proyecto_claude/web_chat.html

# Opción 2: Servidor local
cd /Users/lucianovillarroelparra/telegram-bot/proyecto_claude
python3 -m http.server 8000
# Luego: http://localhost:8000/web_chat.html

# Opción 3: Copiar URL y abrir en navegador (Chrome, Safari, Firefox)
file:///Users/lucianovillarroelparra/telegram-bot/proyecto_claude/web_chat.html
```

---

## Layout & Secciones

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER (Arauco logo, título, agent badges)                     │
├──────────────────────────────┬──────────────────────────────────┤
│                              │                                  │
│  CHAT PANEL (60%)            │  LIVE DATA PANEL (40%)          │
│  • Timeline (msgs)           │  • Tabs: Equipos/KPIs/          │
│  • Input area                │    Pérdidas/Acciones/Query      │
│  • Send button               │  • Búsqueda + Export CSV        │
│  • Hint buttons              │  • Mini Gantt (acciones)        │
│                              │  • SQL Query Builder            │
└──────────────────────────────┴──────────────────────────────────┘
```

---

## Interacciones principales

### 1. Escribir un mensaje
```
1. Click en textarea ("Escribe tu consulta...")
2. Escribe: "Analiza OEE Línea 3"
3. Press ENTER o click botón Enviar
4. El sistema simula respuesta después de 1.5s
```

### 2. Expandir un chat card
```
1. Busca un mensaje del Agente (fondo blanco, no gris)
2. Si tiene flecha "▼", es expandible
3. Click en el mensaje
4. Se abre detalle con tabla + chips KPI + evidencia badge
5. Click de nuevo para contraer
```

### 3. Cambiar tabs en Live Data Panel
```
1. Haz click en los botones: "Equipos", "KPIs", "Pérdidas", "Acciones", "Query"
2. Cada tab muestra una tabla diferente con datos mock
3. Busca, exporta, o escribe SQL
```

### 4. Buscar en una tabla
```
1. Abre cualquier tab (ej: "KPIs")
2. En el input "Buscar KPI..." escribe: "OEE"
3. La tabla se filtra en tiempo real
```

### 5. Exportar datos a CSV
```
1. Abre un tab (ej: "Pérdidas")
2. Click botón "📥 CSV"
3. Se descarga: perdidas-arauco-mc-2026-06-12.csv
```

### 6. Usar hint buttons
```
1. Bajo el input hay 4 botones: "📊 OEE L3", "🔍 Pérdidas", "📋 BPMN", "⚡ Acciones"
2. Click en uno → auto-rellena el input con esa consulta
```

### 7. Query Builder SQL
```
1. Abre tab "Query"
2. Escribe en textarea:
   SELECT * FROM perdidas WHERE fecha >= DATE('now', '-7 days')
3. Click "Ejecutar"
4. Mock: muestra mensaje "En producción se ejecutaría..."
```

---

## Características implementadas

| Feature | Estado | Descripción |
|---|---|---|
| **Chat cards expandibles** | ✅ Funcional | Click → expand/collapse detail |
| **Timeline virtualized** | ⏳ Mock | Setup para Intersection Observer |
| **Live Data Panel** | ✅ Funcional | 5 tabs + búsqueda + export |
| **Mini Gantt** | ✅ Visual | CSS bars, no SVG |
| **Colores Arauco** | ✅ Aplicados | WCAG AA/AAA compliant |
| **Responsive mobile** | ✅ Funcional | Stack vertical < 768px |
| **Evidence badges** | ✅ Clickable | alert() con fuente |
| **Artifacts inline** | ✅ Embebidos | Tablas, KPI chips |
| **Export CSV** | ✅ Funcional | Descarga inmediata |
| **Query Builder** | ⏳ Mock | Input SQL, sin backend |
| **WebSocket real-time** | ❌ No | Próxima fase |
| **Autenticación** | ❌ No | Próxima fase |

---

## Mock Data

### Tablas disponibles
- **Equipos:** Cizalla 3A, Prensa 3B, Clasificador 3C, Horno 1A
- **KPIs:** OEE 71,2%, Disponibilidad 85,3%, Rendimiento 78,9%, Calidad 96,4%
- **Pérdidas:** Parada 40,7%, Ajuste 29,4%, Rechazo 18,3%, Otros 11,6%
- **Acciones:** GEMBA (en curso), Kaizen (pendiente), A3 (pendiente)

### Mensajes de chat (ejemplos)
- Usuario pregunta sobre OEE L3
- Orquestador delega
- EO responde con tabla de pérdidas
- Orquestador sintetiza recomendaciones

---

## Próximos pasos (Backend)

Para conectar a Railway + Claude API + arauco_mc.db:

1. **Crear endpoint `/api/chat/message`**
   - POST { content, files, context }
   - Return: ChatMessage[] con agent responses

2. **Crear endpoint `/api/live-data/{table}`**
   - GET con query params: limit, dateRange, equipoId
   - Return: SELECT * FROM {table} en JSON

3. **Crear endpoint `/api/live-data/query`**
   - POST { sql, validate: true }
   - Ejecutar contra arauco_mc.db

4. **Configurar WebSocket**
   - Stream responses en tiempo real
   - Subscribe a live updates de arauco_mc.db

5. **Implementar autenticación**
   - Session token en header
   - Validación de permisos por agent

---

## Navegadores soportados

| Navegador | Versión | Estado |
|---|---|---|
| Chrome | 90+ | ✅ Soportado |
| Safari | 14+ | ✅ Soportado |
| Firefox | 88+ | ✅ Soportado |
| Edge | 90+ | ✅ Soportado |
| Mobile Safari | iOS 14+ | ✅ Responsive |
| Chrome Mobile | Android 10+ | ✅ Responsive |

---

## Tips & Tricks

- **Auto-expand input:** El textarea crece automáticamente (max 120px)
- **Scroll automático:** Timeline se scrollea al final cuando llega nuevo msg
- **Search con Cmd/Ctrl+/:** Todavía no implementado, próximamente
- **Dark mode:** No implementado, opcional en Phase 5
- **Share links:** No implementado, próxima fase

---

## Ficheros relacionados

- **web_chat.html** — HTML5 completo (este archivo)
- **WEB_CHAT_ARCHITECTURE.md** — Documentación técnica profunda
- **arauco_mc.db** — Datos operacionales (SQLITE3)

---

## Contacto & Feedback

Para cambios, mejoras o bugs:
- Luciano Villarroel — luciano.villarroel@arauco.com
- Repo: /Users/lucianovillarroelparra/telegram-bot/proyecto_claude/
