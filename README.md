# StadiumIQ — AI-Powered Stadium Experience for FIFA World Cup 2026

[![CI Status](https://github.com/Mr-TD/FifaEvent/actions/workflows/ci.yml/badge.svg)](https://github.com/Mr-TD/FifaEvent/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**StadiumIQ** is a GenAI-enabled web platform that enhances stadium operations and the overall tournament experience for the FIFA World Cup 2026. Built with Flask and powered by Google Gemini AI, it delivers intelligent navigation, crowd management, accessibility guidance, transportation recommendations, and real-time operational intelligence across all 16 tournament venues.

## Key Features

| Feature | Description | GenAI Role |
|---------|-------------|------------|
| 🤖 **AI Assistant** | Multilingual chatbot supporting 12+ languages | Google Gemini generates context-aware responses |
| 🗺️ **Stadium Navigator** | Interactive map with points of interest (food, exits, medical, etc.) | AI-powered wayfinding and accessible route guidance |
| 📅 **Match Schedule** | Full 104-match schedule with filtering | AI-generated match previews and storylines |
| 👥 **Crowd Intelligence** | Real-time density monitoring across stadium zones | AI recommends crowd flow actions for staff |
| 🚗 **Transportation Hub** | Transit options per venue (metro, bus, rideshare, parking) | AI recommends optimal transit based on time/preference |
| ♿ **Accessibility** | Personalized accessible route planning | AI adapts guidance to individual mobility needs |
| 🌱 **Sustainability** | Eco-impact tracker with gamified actions | AI generates contextual sustainability tips |
| 📊 **Ops Intelligence** | Operational briefings and volunteer task management | AI generates situation reports and priority actions |
| 🔐 **Google Sign-In** | OAuth 2.0 authentication | Google OAuth integration |

## Architecture

```
StadiumIQ/
├── app.py              # Flask application factory
├── ai_engine.py        # Google Gemini AI wrapper with fallback
├── models.py           # SQLAlchemy ORM models
├── config.py           # Environment-based configuration
├── seed.py             # Database seeding from JSON
├── utils.py            # Shared utilities
├── routes/             # Blueprint modules
│   ├── main.py         # Landing page
│   ├── chatbot.py      # AI chatbot + translation
│   ├── stadium.py      # Stadium navigator + POIs
│   ├── schedule.py     # Match schedule + AI previews
│   ├── crowd.py        # Crowd density monitoring
│   ├── transportation.py  # Transit recommendations
│   ├── accessibility.py   # Accessible navigation
│   ├── sustainability.py  # Eco-impact tracking
│   ├── ops_intelligence.py # Staff operational briefings
│   └── auth.py         # Google OAuth
├── templates/          # Jinja2 HTML templates
├── static/             # CSS, JS, and JSON data
├── tests/              # pytest test suite
└── docs/               # Architecture documentation
```

## Tech Stack

- **Backend:** Flask 3.x, Flask-SocketIO, Flask-SQLAlchemy, Flask-WTF (CSRF)
- **AI:** Google Gemini 2.0 Flash (`google-generativeai`)
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Frontend:** Vanilla JS, Leaflet.js (maps), Chart.js, Lucide Icons
- **Auth:** Google OAuth 2.0
- **CI/CD:** GitHub Actions (lint, format, test, CodeQL)
- **Deployment:** Docker + Gunicorn

## Quick Start

```bash
# Clone
git clone https://github.com/Mr-TD/FifaEvent.git
cd FifaEvent

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your GEMINI_API_KEY for full AI features

# Run
python app.py
# Open http://localhost:5000
```

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest --cov=. -v
```

## Google Cloud Services Used

| Service | Purpose |
|---------|---------|
| Gemini AI | Chatbot, match previews, crowd analysis, accessibility, transportation, ops briefings |
| Google Maps | Stadium navigation and mapping |
| Google Analytics | Usage tracking |
| Google OAuth | User authentication |
| Google Fonts | Typography (Outfit) |
| Google Translate | Multilingual UI support |

## Problem Statement Alignment

This solution addresses the FIFA World Cup 2026 challenge by providing:
- **Navigation** — Interactive stadium maps with AI-powered wayfinding
- **Crowd Management** — Real-time density monitoring with AI operational recommendations
- **Accessibility** — Personalized accessible route planning for diverse mobility needs
- **Transportation** — AI-recommended transit options (metro, bus, rideshare, parking)
- **Sustainability** — Gamified eco-impact tracking with AI-generated tips
- **Multilingual Assistance** — 12+ language support via AI chatbot
- **Operational Intelligence** — AI-generated staff briefings and volunteer task management
- **Real-Time Decision Support** — Aggregated data feeds with AI-driven priority actions

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
