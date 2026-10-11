# Portfolio Backend

A FastAPI backend for my portfolio site. It powers the "David AI Clone" chat
widget (via OpenRouter) and the contact form (via SMTP).

Pairs with the frontend repo, `my-portfolio-frontend` (Next.js).

## Quickstart

```bash
python -m venv .venv
. .venv/Scripts/activate        # Windows; use `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
cp .env.example .env            # defaults to LLM_BACKEND=mock: no API key needed
pytest -q
uvicorn app.main:app --reload   # http://localhost:8000
```

Then `curl http://localhost:8000/health`.

## API

| Method | Path | Body | Success |
|---|---|---|---|
| `POST` | `/api/chat` | `{ "userMessage": "..." }` | `{ "reply": "..." }` |
| `POST` | `/api/contact` | `{ "name", "email", "message" }` | `{ "success": "..." }` |
| `GET` | `/health` | | `{ "status": "ok", "llm_backend": "..." }` |

Every error is returned as `{ "error": "..." }`. Chat is limited to 20
requests per 2 minutes per IP, contact to 5 per 15 minutes.

## Project layout

```
app/
  api/         FastAPI routers: parse the request, call a service
  schemas/     Pydantic request/response models and validation
  services/    Chat backend (Protocol + mock + OpenRouter) and SMTP email sender
  prompts/     The AI clone's persona and knowledge base
  config.py    Every env-driven setting, in one place
  rate_limit.py  Per-IP sliding-window limiter
  main.py      App entrypoint, CORS, error handlers, /health
tests/         pytest suite: offline, no API key needed
```

## Configuration

Everything is an env var; see `.env.example`.

| Setting | Values | Default |
|---|---|---|
| `LLM_BACKEND` | `openrouter` / `mock` | `openrouter` |
| `OPENROUTER_MODELS` | comma-separated, tried in order | three free models |
| `CORS_ALLOWED_ORIGINS` | comma-separated origins | `http://localhost:3000` |
| `CORS_ALLOWED_ORIGIN_REGEX` | one regex | Vercel deployments of the frontend |

With `LLM_BACKEND=openrouter` the app refuses to start without
`OPENROUTER_API_KEY`.

Contact email is sent over SMTP by default. If `RESEND_API_KEY` is set it goes
through [Resend](https://resend.com)'s HTTPS API instead, which is what the
Render deployment uses because Render's free tier blocks outbound SMTP ports.

## Deploying (Render)

- Runtime: Python 3
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --forwarded-allow-ips="*"`

`--forwarded-allow-ips` makes the rate limiter see the visitor's IP rather
than Render's proxy.

## Legacy

`legacy-express/` holds the original Node/Express version of this API, kept
for reference during the migration.
