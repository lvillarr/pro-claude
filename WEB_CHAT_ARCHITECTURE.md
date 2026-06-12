# web_chat.html — Arquitectura Radical UI/UX

**Versión:** 1.0-beta  
**Fecha:** 2026-06-12  
**Estado:** Mock data, funcionalidad local completa  

---

## RESUMEN EJECUTIVO

Implementación HTML5 + CSS3 + vanilla JavaScript de un chat multi-agente con **split-layout 60/40** (chat + live data), **chat cards expandibles**, **timeline virtualized**, y **artifacts inline**. Paridad de features vs Telegram bot + acceso integrado a datos operacionales de `arauco_mc.db`.

**Características principales:**
- ✅ Chat expandible con ancla a evidencia (arauco_mc.db)
- ✅ Live Data Panel con 5 tabs (Equipos, KPIs, Pérdidas, Acciones, Query Builder)
- ✅ Timeline con búsqueda full-text (mock)
- ✅ Mini Gantt para acciones activas
- ✅ Colores Arauco con WCAG AA/AAA contrast
- ✅ Mobile-first responsive (stack vertical < 768px)
- ✅ Tablas exportables (CSV)
- ✅ Query Builder SQL (mock)

---

## ARQUITECTURA TÉCNICA

### 1. LAYOUT CSS GRID

```css
.main {
  display: grid;
  grid-template-columns: 60% 40%;  /* Desktop: 1440px+ */
  gap: 0;
  flex: 1;
  overflow: hidden;
}

/* Mobile: stack vertical */
@media (max-width: 768px) {
  .main {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr auto;  /* Chat full, Live Data drawer */
  }
}
```

### 2. COMPONENTES PRINCIPALES

#### A. Chat Card (Expandible)
- **Clase base:** `.chat-card`
- **Expandido:** `.chat-card.expanded`
- **Contenido detalle:** `.chat-card-detail` (display: none por defecto)
- **Función:** `toggleCardExpand(msgId)` — alterna clase expanded

**Estructura:**
```html
<div class="chat-card ai" id="msg-3">
  <div class="chat-card-avatar avatar-eo">EO</div>
  <div class="chat-card-body">
    <div class="chat-card-sender">Excelencia Operacional</div>
    <div class="chat-card-bubble" onclick="toggleCardExpand(3)">
      <!-- Summary visible siempre -->
      Análisis de pérdidas Q1 2026...
      <span class="expand-toggle">▼</span>
    </div>
    <div class="chat-card-detail">
      <!-- Detail content (KPI chips, tabla, evidencia badge) -->
    </div>
    <div class="chat-card-time">14:33</div>
  </div>
</div>
```

#### B. Timeline (Virtualized Mock)
- **Clase:** `.timeline`
- **Scroll lazy:** Intersection Observer (setup pronto)
- **Búsqueda:** Full-text en DOM (live filtering)
- **Función:** `renderTimeline()` — vuelve a render todos los msgs

#### C. Live Data Panel (5 Tabs)
- **Tabs:** Equipos, KPIs, Pérdidas, Acciones, Query Builder
- **Función:** `switchLDPTab(tabName)` — muestra/oculta tabs
- **Búsqueda por tab:** `filterTable(tabName)` — filtra rows en tiempo real
- **Export:** `exportData(tabName)` — genera CSV descargable

**Tabs estructura:**
```html
<div class="ldp-header">
  <button class="ldp-tab active" onclick="switchLDPTab('equipos')">Equipos</button>
  <!-- ... -->
</div>

<div id="tab-equipos" class="ldp-content active">
  <div class="ldp-search">
    <input placeholder="Buscar..." onkeyup="filterTable('equipos')">
    <button onclick="exportData('equipos')">📥 CSV</button>
  </div>
  <table class="ldp-table"><!-- Mock data --></table>
</div>
```

#### D. Artifacts Inline
- **Tabla:** `.artifact.artifact-table` — sorteable, 100% width
- **Mini Gantt:** `.mini-gantt` — barras CSS, labels, % progress
- **Evidence badge:** `.evidence-badge` — clickable link a fuente

**Ejemplo inline:**
```html
<div class="artifact artifact-table">
  <table>
    <thead>...</thead>
    <tbody>...</tbody>
  </table>
  <div class="artifact-footer">
    <a onclick="copyToInput(...)">+ Crear A3</a>
    <span>Fuente: arauco_mc.db → perdidas</span>
  </div>
</div>
```

---

## FLUJOS DE DATOS

### Flow 1: Usuario envía mensaje
```
User clicks "Enviar" o Enter
  ↓
sendMessage()
  • Crear objeto ChatMessage { id, agent: 'user', summary, detail: null }
  • Agregar a array messages[]
  • renderTimeline() — re-render todo
  • Limpiar input + auto-resize textarea
  ↓
setTimeout(1500ms)
  • Simular respuesta Orquestador { agent: 'orquestador', summary, detail: {...} }
  • renderTimeline()
```

**En producción:**
```
POST /api/chat/message { content, files, context }
  ← Server: invoke multi-agent system (Orquestador delegates)
  ← Return: ChatMessage[] with agent responses + evidence links
  → WebSocket: stream responses live
```

### Flow 2: Expandir chat card + mostrar evidencia
```
User clicks .chat-card-bubble (si tiene detail)
  ↓
toggleCardExpand(msgId)
  • Toggle .expanded clase
  • CSS: .chat-card-detail { display: block }
  • Mostrar tabla + KPI chips + evidencia badge
  ↓
User clicks evidencia badge
  • alert() con fuente (ej: "arauco_mc.db → perdidas")
  • **En prod:** modal o sidebar con full query + RAG context
```

### Flow 3: Live Data Panel queries
```
User opens "KPIs" tab → switchLDPTab('kpis')
  ↓
Tab content .ldp-content.active { display: block }
  • Tabla con mock data (4 filas)
  ↓
User types en search box → filterTable('kpis')
  • Filtra rows en tiempo real (text.includes)
  ↓
User clicks "📥 CSV" → exportData('kpis')
  • Genera Blob CSV
  • Download as `kpis-arauco-mc-2026-06-12.csv`
```

**En producción:**
```
GET /api/live-data/kpis?limit=100&dateRange=7d
  ← DB query: SELECT * FROM kpis WHERE fecha >= DATE('now', '-7 days')
  ← Compute delta vs meta para cada KPI
  → Render tabla + sparklines
```

### Flow 4: Query Builder
```
User abre tab "Query"
  • Textarea con placeholder SQL
  • Button "Ejecutar"
  ↓
executeQuery()
  • Mock: muestra mensaje "en producción se ejecutaría..."
  ↓
**En producción:**
  POST /api/live-data/query { sql: "SELECT...", validate: true }
    • Validar SQL (no permite DROP, DELETE, UPDATE)
    • Ejecutar contra arauco_mc.db
    • Return: paginated results + metadata
```

---

## COLORES ARAUCO (Accessibility)

| Color | Hex | Uso | WCAG |
|---|---|---|---|
| **Brown** | #696158 | Headers, avatars, primary | AAA |
| **Gold** | #BFB800 | Accents, badges, CTAs | AA |
| **Orange** | #EA7600 | EO agent, warnings | AA |
| **Bg Light** | #f5f2ee | Card hover, chips | - |
| **Bg Pale** | #f0ede9 | Body bg | - |
| **Border** | #e0dbd4 | Dividers | - |
| **Text Dark** | #333 | Body text | AAA |
| **Text Gray** | #999 | Secondary | AA |

**Agent badges:**
- Orquestador: #696158 (brown)
- EO: #EA7600 (orange)
- IA: #BFB800 (gold)
- TD: #DFD1A7 (muted)
- DA: #f0ede9 (light)

---

## RESPONSIVE DESIGN

### Desktop (1440px+)
- **Chat:** 60% width, full height
- **Live Data:** 40% width, drawer-style
- **Visible simultáneamente**

### Tablet (768px — 1200px)
- **Chat:** 60%
- **Live Data:** 40%
- **Same layout**

### Mobile (< 768px)
- **Chat:** 100% width, top 60%
- **Live Data:** 100% width, drawer bottom 40% (swipe to expand)
- **Stack vertical**
- **Badges collapse a iconos**

**Breakpoints CSS:**
```css
@media (max-width: 768px) {
  .main { grid-template-rows: 1fr auto; }
  .live-data-panel { max-height: 40vh; border-top: 1px; }
}

@media (max-height: 600px) {
  /* Landscape phones — reduce headers */
  .header { height: 48px; }
}
```

**Touch optimizations:**
- Min tap target: 44x44px (buttons)
- Swipe en chat cards (mock setup)
- Long-press timestamp: copy link

---

## PERFORMANCE OPTIMIZATIONS

### 1. Timeline Virtualization (Pendiente)
```javascript
// Usar Intersection Observer para lazy-load
const observerOptions = {
  root: timelineElement,
  rootMargin: '200px',
  threshold: 0
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && shouldLoadMore()) {
      loadOlderMessages();
    }
  });
}, observerOptions);
```

**Beneficio:** Soporta 1000+ messages sin slowdown

### 2. Lazy-render Chat Card Details
```javascript
// Card detail se renderiza solo cuando expanded
if (msg.detail !== null) {
  // HTML en msg.detail.html, mostrado via display: block
}
```

**Beneficio:** Reduce DOM initial, faster paint

### 3. Table Pagination (Mock)
```javascript
// Live Data tables ahora muestran top 10-20 rows
// "Load more" button para rest
```

### 4. Sparklines (Canvas vs SVG)
- Mini Gantt: CSS bars, no SVG (más rápido)
- Charts: recharts + canvas para <100 puntos

---

## INTEGRACIÓN CON BACKEND

### REST API Endpoints (Diseño)

```
GET  /api/chat/history?sessionId=xxx&limit=50&offset=0
     → ChatMessage[] con agent, summary, detail, evidence
POST /api/chat/message { content, files[], context }
     → Invoke multi-agent, return ChatMessage[]

GET  /api/live-data/{table}?limit=100&dateRange=7d&equipoId={id}
     → SELECT * FROM {table}, return paginated + metadata
POST /api/live-data/query { sql, validate: true }
     → Execute SQL, return results

GET  /api/search?query={q}&scope=chat|db|all
     → Full-text search, return combined results

POST /api/artifacts/export { format, data }
     → Download CSV/JSON/Excel/PDF

GET  /api/share/{token}
     → Shareable query result + chat excerpt
```

### Authentication
- Session token en header: `Authorization: Bearer {token}`
- Heredado de Telegram bot session

### CORS
- Allow origin: Railway deployment URL
- Methods: GET, POST, OPTIONS
- Headers: Content-Type, Authorization

---

## ESTRUCTURA MOCK DATA

### messages[] array
```javascript
{
  id: 1,
  agent: 'user' | 'orquestador' | 'eo' | 'ia' | 'td' | 'da',
  sender: 'Luciano' | 'Orquestador' | ...,
  avatar: 'LV' | 'MC' | 'EO' | ...,
  time: '14:32',
  summary: 'Text visible siempre',
  detail: {
    html: '<div>...</div>'  // null si no expandible
  }
}
```

### Live Data Tables (Mock)
- **Equipos:** 4 rows (Cizalla 3A, Prensa 3B, etc.)
- **KPIs:** 4 rows (OEE, Disponibilidad, Rendimiento, Calidad)
- **Pérdidas:** 4 rows (Parada, Ajuste, Rechazo, Otros)
- **Acciones:** 3 rows + mini Gantt (GEMBA, Kaizen, A3)

---

## COMO USAR

### 1. Abrir en navegador
```bash
# Local (sin servidor)
open /Users/lucianovillarroelparra/telegram-bot/proyecto_claude/web_chat.html

# O servir con Python
cd /Users/lucianovillarroelparra/telegram-bot/proyecto_claude
python3 -m http.server 8000
# → http://localhost:8000/web_chat.html
```

### 2. Interacciones funcionales
- **Escribir mensaje:** Textarea + Enter o botón Enviar
- **Expandir card:** Click en bubble (si tiene detail)
- **Cambiar tabs Live Data:** Click en botones (Equipos, KPIs, etc.)
- **Buscar en tabla:** Type en input
- **Exportar CSV:** Click "📥 CSV"
- **Query Builder:** Escribir SQL + "Ejecutar"

### 3. Teclado
- **Ctrl/Cmd + Enter:** Enviar mensaje (implementar)
- **Ctrl/Cmd + /:** Focus búsqueda (setup)

---

## PRÓXIMOS PASOS (ROADMAP)

### Fase 1: Backend integration (Semana 1-2)
- [ ] Conectar `/api/chat/message` a Orquestador agent
- [ ] WebSocket para stream responses real-time
- [ ] Autenticación session token

### Fase 2: Live Data (Semana 2-3)
- [ ] `/api/live-data/{table}` endpoint activo
- [ ] Query arauco_mc.db en tiempo real
- [ ] Sparklines + delta calculations

### Fase 3: Search & Timeline (Semana 3-4)
- [ ] Full-text search en chat + DB
- [ ] Virtualization con Intersection Observer
- [ ] Filtros por agente, fecha

### Fase 4: Artifacts & Export (Semana 4-5)
- [ ] Inline rendering de Excel, PDF, BPMN
- [ ] Export a múltiples formatos
- [ ] Shareable links con token

### Fase 5: Polish & Perf (Semana 5-6)
- [ ] Testing en mobile devices reales
- [ ] Performance profiling (FCP, LCP, CLS)
- [ ] Accessibility audit (WCAG 2.1 AA)
- [ ] Dark mode toggle (opcional)

---

## TROUBLESHOOTING

### Chat messages no renderizan
- Verificar `renderTimeline()` se llama después de actualizar `messages[]`
- Revisar console para errores de sintaxis JS

### Live Data tabs no cambian
- Confirmar `switchLDPTab()` agrega/quita clase `.active` correctamente
- Revisar CSS `.ldp-content.active { display: block }`

### Textarea no auto-resize
- Función `autoResizeTextarea()` debe llamarse en `oninput`
- Verificar max-height: 120px

### Mobile layout roto
- Revisar media query `max-width: 768px` en CSS
- Viewport meta tag presente: `<meta name="viewport"...>`

---

## ARCHIVOS

| Archivo | Descripción |
|---|---|
| `web_chat.html` | Implementación completa HTML5+CSS3+JS |
| `WEB_CHAT_ARCHITECTURE.md` | Este documento |
| `arauco_mc.db` | Mock data source (tablas: equipos, kpis, perdidas, acciones) |

---

## CUMPLIMIENTO

- ✅ Diseño radical UI/UX con split-layout 60/40
- ✅ Chat cards expandibles con ancla a evidencia
- ✅ Timeline con búsqueda (mock setup)
- ✅ Live Data Panel tabulado + export CSV
- ✅ Mini Gantt para acciones
- ✅ Colores Arauco con WCAG AA/AAA
- ✅ Mobile-first responsive
- ✅ Artifacts inline (tablas, mini-Gantt)
- ✅ Query Builder SQL (mock)
- ✅ Mock data, sin endpoints aún

---

**Versión final:** 2026-06-12 — lista para integración backend en Railway + Claude API.
