# Release Skill — Bot Arauco MC

Ejecutar en orden. **Pedir confirmacion antes de cada paso destructivo (bump, commit, push, tags).**

---

## Paso 1 — Correr tests (no destructivo)

```bash
cd /Users/lucianovillarroelparra/telegram-bot
pip install -q -r requirements-dev.txt
pytest tests/ -v
```

Si algun test falla: reportar y detener. No continuar sin aprobacion explicita.

---

## Paso 2 — Verificar paridad bot/web UI

Comparar handlers Telegram vs rutas FastAPI en `bot.py`:
- Listar comandos Telegram registrados (`app.add_handler(CommandHandler(...))`)
- Listar rutas FastAPI (`@_web_app.get/post(...)`)
- Identificar features con handler Telegram pero sin ruta web equivalente, y viceversa
- Reportar discrepancias como checklist

**Confirmar con el usuario antes de continuar.**

---

## Paso 3 — Bump de version (destructivo)

Leer version actual en `VERSION`. Preguntar al usuario: patch / minor / major.

Actualizar `VERSION` con la nueva version. Mostrar el cambio. **Esperar confirmacion.**

---

## Paso 4 — Commit convencional (destructivo)

```bash
git add VERSION tests/ proyecto_claude/.claude/skills/
git commit -m "release: vX.Y.Z — <descripcion breve de cambios>"
```

Usar Conventional Commits. Sujeto <= 50 chars. **Confirmar mensaje con usuario antes de commitear.**

---

## Paso 5 — Push commits + tags (destructivo)

```bash
git push
git tag vX.Y.Z
git push --tags
```

**Pedir confirmacion explicita antes de ejecutar.**

---

## Paso 6 — Estado del deploy

```bash
railway status 2>/dev/null || echo "railway CLI no disponible — verificar deploy en dashboard Railway"
```

Reportar estado. Si Railway CLI no esta instalado, indicar URL del dashboard.

---

## Notas

- Tests son smoke tests contra servidor corriendo. Si servidor no esta activo localmente, usar `BOT_BASE_URL=https://<railway-url> pytest tests/ -v`
- Version en `VERSION` es la unica fuente de verdad — no hay `package.json` ni `pyproject.toml`
- No auto-corregir discrepancias de paridad bot/web — solo reportar
