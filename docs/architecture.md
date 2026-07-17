# StadiumIQ — Architecture Overview

## System Architecture

StadiumIQ follows the **Flask Application Factory** pattern with Blueprint-based modular routing. All AI features are centralized in a single `StadiumAI` engine that wraps Google Gemini with graceful fallback to curated mock responses.

```
┌─────────────────────────────────────────────────────────┐
│                       Client                            │
│  (Browser: HTML/CSS/JS, Leaflet Maps, Chart.js)         │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP / WebSocket
┌─────────────────▼───────────────────────────────────────┐
│              Flask Application (app.py)                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Blueprints (routes/)                  │  │
│  │  main │ chatbot │ stadium │ schedule │ crowd      │  │
│  │  transportation │ accessibility │ sustainability  │  │
│  │  ops_intelligence │ auth                          │  │
│  └──────────────────────┬────────────────────────────┘  │
│                         │                                │
│  ┌──────────────────────▼────────────────────────────┐  │
│  │          AI Engine (ai_engine.py)                  │  │
│  │  ┌─────────────────┐  ┌────────────────────────┐  │  │
│  │  │  Google Gemini   │  │  Fallback Mock Engine  │  │  │
│  │  │  (gemini-2.0-    │  │  (curated responses)   │  │  │
│  │  │   flash)         │  │                        │  │  │
│  │  └─────────────────┘  └────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                         │                                │
│  ┌──────────────────────▼────────────────────────────┐  │
│  │         Data Layer                                 │  │
│  │  SQLAlchemy ORM ─── SQLite / PostgreSQL            │  │
│  │  JSON Data Files ── static/data/                   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

1. **Fan Request** → Browser sends HTTP/WS request to Flask
2. **Route Handler** → Blueprint receives and validates input
3. **AI Processing** → `StadiumAI` engine queries Gemini (or falls back to mock)
4. **Response** → JSON API response or rendered Jinja2 template

## GenAI Integration Points

| Feature | AI Method | Input | Output |
|---------|-----------|-------|--------|
| Chatbot | `chat()` | User message + language | Contextual response |
| Translation | `translate()` | Text + source/target lang | Translated text |
| Match Preview | `generate_match_preview()` | Match data dict | Engaging preview |
| Crowd Mgmt | `crowd_recommendation()` | Zone density data | Operational actions |
| Accessibility | `accessibility_guide()` | User needs + destination | Step-by-step route |
| Sustainability | `sustainability_tip()` | Context string | Actionable eco-tip |
| Transportation | `transportation_recommendation()` | Stadium + time + preference | Transit advice |
| Ops Intelligence | `ops_briefing()` | Aggregated ops context | Staff situation report |

## Security Measures

- CSRF protection via Flask-WTF (API routes exempted)
- Session cookie hardening (HttpOnly, SameSite=Lax, Secure in prod)
- Input validation and normalization on all user-facing endpoints
- Google OAuth 2.0 for authentication
- Environment-based configuration (secrets never hardcoded)

## Stack

- **Backend:** Flask 3.x, Flask-SocketIO, Flask-SQLAlchemy
- **AI Engine:** Google Gemini 2.0 Flash (`google-generativeai`)
- **Database:** SQLAlchemy ORM (SQLite dev / PostgreSQL prod)
- **Frontend:** Vanilla JS, Leaflet.js, Chart.js, Lucide Icons
- **CI/CD:** GitHub Actions (pytest, flake8, black, CodeQL)
- **Deployment:** Docker + Gunicorn
