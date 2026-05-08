# Guía de Template — Bot Telegram + Claude API

Guía para replicar desde cero un bot de Telegram con agentes IA, generación de artefactos y despliegue en Railway.

---

## Stack

| Componente | Tecnología |
|---|---|
| Bot | `python-telegram-bot==21.3` |
| IA | `anthropic` (claude-sonnet-4-6) |
| Transcripción | `groq` (whisper-large-v3) |
| Búsqueda semántica | `chromadb` + `voyageai` |
| Artefactos | `openpyxl`, `reportlab`, `python-pptx`, `pdfplumber`, `python-docx` |
| Email | `requests` → SendGrid API |
| Deploy | Railway |

---

## 1. Estructura de archivos

```
telegram-bot/
├── bot.py                  ← todo el bot en un solo archivo
├── rag.py                  ← módulo de búsqueda semántica (ChromaDB)
├── requirements.txt
└── proyecto_claude/        ← contexto para Claude Code
    ├── CLAUDE.md           ← reglas globales + contexto corporativo
    ├── agentes/            ← prompts por agente (IA, TD, EO, DA)
    ├── orquestador/        ← prompt del orquestador
    └── skills/             ← skills invocables (/spec, /plan, etc.)
```

---

## 2. Variables de entorno (Railway)

```
TELEGRAM_TOKEN        token del bot (@BotFather)
ANTHROPIC_API_KEY     clave Anthropic
GROQ_API_KEY          clave Groq (audio)
VOYAGE_API_KEY        clave VoyageAI (RAG)
SENDGRID_API_KEY      clave SendGrid (email)
SENDER_EMAIL          correo verificado en SendGrid
RAILWAY_PUBLIC_DOMAIN dominio público del servicio (lo genera Railway)
PORT                  puerto HTTP (Railway lo asigna automáticamente)
```

---

## 3. Arquitectura del bot

### 3.1 Servidor HTTP interno

El bot levanta un servidor HTTP en un hilo de fondo para servir HTML generado por Claude como URLs públicas.

```python
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import OrderedDict

_HTML_STORE: OrderedDict = OrderedDict()
_MAX_STORE  = 100
_HTTP_PORT  = int(os.environ.get("PORT", 8080))
PUBLIC_BASE = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
PUBLIC_BASE = f"https://{PUBLIC_BASE}" if PUBLIC_BASE else f"http://localhost:{_HTTP_PORT}"

class _HTMLHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/health":
            self._respond(200, b"ok", "text/plain")
        elif path == "/arauco.css":                          # CSS estático de marca
            self._respond(200, _ARAUCO_CSS.encode(), "text/css; charset=utf-8")
        elif path.startswith("/g/"):
            gid  = path[3:]
            html = _HTML_STORE.get(gid)
            if html: self._respond(200, html.encode("utf-8"), "text/html; charset=utf-8")
            else:    self._respond(404, b"No encontrado.", "text/plain")
        else:
            self._respond(404, b"", "text/plain")

    def _respond(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def _start_http_server():
    HTTPServer(("0.0.0.0", _HTTP_PORT), _HTMLHandler).serve_forever()

threading.Thread(target=_start_http_server, daemon=True).start()
```

### 3.2 Función `store_html`

```python
def store_html(html: str) -> str:
    gid = uuid.uuid4().hex
    _HTML_STORE[gid] = html
    if len(_HTML_STORE) > _MAX_STORE:
        _HTML_STORE.popitem(last=False)
    return f"{PUBLIC_BASE}/g/{gid}"
```

### 3.3 Persistencia entre reinicios

```python
from telegram.ext import PicklePersistence

app = (
    ApplicationBuilder()
    .token(os.environ["TELEGRAM_TOKEN"])
    .persistence(PicklePersistence(filepath="/tmp/bot_persistence"))
    .build()
)
```

---

## 4. Sistema de artefactos

### 4.1 Patrón general

Cada artefacto sigue el mismo flujo:
1. Claude recibe un prompt específico + descripción del usuario
2. Claude responde con JSON estructurado (o HTML directo)
3. Python construye el archivo y lo envía por Telegram

### 4.2 Helpers clave

**`extract_json`** — parsea JSON aunque Claude agregue texto alrededor:
```python
def extract_json(raw: str) -> dict:
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        inner = "\n".join(lines[1:])
        if inner.rstrip().endswith("```"):
            inner = inner.rstrip()[:-3].rstrip()
        text = inner.strip()
    start = text.find("{")
    end   = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start:end+1]
    return json.loads(text)
```

**`_make_reply_fn`** — abstrae `reply_text` y `reply_document` en una sola función:
```python
def _make_reply_fn(message):
    async def reply_fn(text=None, *, buf=None, filename=None, caption=None, **kwargs):
        if buf is not None:
            await message.reply_document(document=buf, filename=filename, caption=caption)
        else:
            await message.reply_text(text, **kwargs)
    return reply_fn
```

**`_render_artifact`** — genera y envía cualquier artefacto, muestra teclado al terminar:
```python
async def _render_artifact(artifact_type, description, reply_fn, context):
    prompt = ARTIFACT_PROMPTS[artifact_type].replace("{CSS_URL}", f"{PUBLIC_BASE}/arauco.css")
    raw = claude_response(prompt, description, max_tokens=_tokens_map[artifact_type])
    # ... switch por artifact_type → build_excel / build_pdf / build_pptx / store_html / etc.
    await reply_fn("¿Generar otro artefacto?", reply_markup=ARTIFACT_KEYBOARD)
```

### 4.3 Tokens por artefacto

```python
_tokens_map = {
    "html":  8000,   # HTML directo — el más largo
    "pdf":   6000,   # JSON con secciones y tablas
    "pptx":  6000,   # JSON con diapositivas
    "gantt": 4000,   # JSON con tareas
    "excel": 3000,   # JSON con filas
    "email": 2000,   # JSON simple
}
```

### 4.4 Detección de intención por mensaje

```python
_ARTIFACT_INTENT = {
    "html":  ["dashboard", "html", "interactivo"],
    "excel": ["excel", "tabla", "spreadsheet"],
    "pdf":   ["pdf", "informe", "reporte"],
    "gantt": ["gantt", "cronograma", "carta gantt"],
    "pptx":  ["ppt", "presentación", "powerpoint"],
    "email": ["correo", "email", "mail"],
}

def _detect_artifact_intent(text: str) -> str | None:
    lower = text.lower()
    for artifact_type, keywords in _ARTIFACT_INTENT.items():
        if any(kw in lower for kw in keywords):
            return artifact_type
    return None
```

Si el usuario describe algo específico (≥3 palabras significativas), no se hereda el contexto del documento anterior:

```python
def _user_msg_has_description(user_msg: str) -> bool:
    stopwords = ["haz", "hacer", "genera", "un", "una", "el", "la", ...]
    tokens = [t for t in user_msg.lower().split() if t not in stopwords]
    return len(tokens) >= 3
```

---

## 5. Manejo de documentos

```python
SUPPORTED_DOCS = {".pdf", ".docx", ".xlsx", ".pptx"}

# En handle_document:
ext = Path(doc.file_name).suffix.lower()
if ext == ".xlsx":  content, structured_data = extract_excel(file_bytes)
elif ext == ".pdf": content = extract_pdf(file_bytes)
elif ext == ".docx": content = extract_docx(file_bytes)
elif ext == ".pptx": content = extract_pptx(file_bytes)

context.user_data["doc_content"]     = content[:10000]
context.user_data["structured_data"] = structured_data  # solo Excel
context.user_data["doc_tipo"]        = ext.upper()
```

El `structured_data` del Excel incluye estadísticas por columna (`frecuencias`, `min`, `max`, `top20`) para que Claude pueda generar gráficos con datos reales.

---

## 6. Sistema de agentes (SYSTEM_PROMPT)

El `SYSTEM_PROMPT` se construye concatenando los CLAUDE.md de cada agente:

```python
def load_agent(path): return open(path).read() if os.path.exists(path) else ""

orquestador = load_agent("proyecto_claude/orquestador/CLAUDE.md")
agente_ia   = load_agent("proyecto_claude/agentes/IA/CLAUDE.md")
agente_td   = load_agent("proyecto_claude/agentes/TD/CLAUDE.md")
agente_eo   = load_agent("proyecto_claude/agentes/EO/CLAUDE.md")

SYSTEM_PROMPT = f"""
## REGLA ABSOLUTA
NUNCA generes código en el chat. Deriva a los botones de artefactos.

{IDENTIDAD}
{orquestador}
{agente_ia}
{agente_td}
{agente_eo}
{REGLAS_GENERALES}
"""
```

### Skills (/spec, /plan, /build, etc.)

Cada skill tiene su propio prompt en `skills/<nombre>/SKILL.md`. Se invocan como comandos `/spec`, `/plan`, `/build`, `/test`, `/review`, `/ship`.

---

## 7. RAG (búsqueda semántica)

`rag.py` gestiona un índice ChromaDB con embeddings de VoyageAI. El bot indexa documentos con el botón "📚 Indexar en RAG" y enriquece cada respuesta con contexto relevante:

```python
rag_ctx = rag.build_context(user_msg)   # busca fragmentos relevantes
system  = SYSTEM_PROMPT + rag_ctx       # los agrega al system prompt
```

---

## 8. Email via SendGrid

```python
def send_email(data: dict) -> None:
    resp = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={"Authorization": f"Bearer {os.environ['SENDGRID_API_KEY']}"},
        json={
            "personalizations": [{"to": [{"email": data["para"]}]}],
            "from": {"email": os.environ["SENDER_EMAIL"]},
            "subject": data["asunto"],
            "content": [{"type": "text/plain", "value": data["cuerpo"]}],
        },
        timeout=15,
    )
    if resp.status_code not in (200, 202):
        raise ValueError(f"SendGrid {resp.status_code}: {resp.text[:200]}")
```

Flujo con confirmación:
1. Claude genera JSON `{para, cc, asunto, cuerpo}`
2. Bot pregunta el destinatario
3. Bot muestra preview con `[✅ Enviar] [✏️ Editar] [❌ Cancelar]`
4. Editar muestra sub-teclado `[👤 Destinatario] [📌 Asunto] [📝 Cuerpo]`

---

## 9. Reglas de comportamiento (CLAUDE.md)

Ver `proyecto_claude/CLAUDE.md`. Las más importantes:

- **No generar código en el chat** — siempre derivar a artefactos
- **Regla absoluta al inicio del SYSTEM_PROMPT** — Claude la ve primero
- **Respuestas concisas** — sin adulación, sin resúmenes innecesarios
- **No heredar contexto del documento** si el usuario describe algo diferente

---

## 10. Checklist para nuevo proyecto

- [ ] Crear bot en @BotFather → obtener `TELEGRAM_TOKEN`
- [ ] Crear cuenta Anthropic → `ANTHROPIC_API_KEY`
- [ ] Crear cuenta Groq → `GROQ_API_KEY` (audio opcional)
- [ ] Crear cuenta VoyageAI → `VOYAGE_API_KEY` (RAG opcional)
- [ ] Crear cuenta SendGrid → verificar sender → `SENDGRID_API_KEY` + `SENDER_EMAIL`
- [ ] Crear proyecto en Railway → conectar repo GitHub
- [ ] Agregar todas las variables de entorno en Railway
- [ ] Generar dominio público en Railway → copiar a `RAILWAY_PUBLIC_DOMAIN`
- [ ] Adaptar `CLAUDE.md` con el contexto corporativo del nuevo cliente
- [ ] Adaptar `IDENTIDAD` y `REGLAS_GENERALES` en `bot.py`
- [ ] Adaptar colores de marca en `_ARAUCO_CSS` y `build_pdf` / `build_pptx`
- [ ] Adaptar logo en el prompt HTML
- [ ] Ajustar `ARTIFACT_PROMPTS` al dominio del cliente
