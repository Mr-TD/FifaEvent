# Architecture Overview

## App Structure
The application follows a standard Flask factory pattern (or basic app pattern):
- `app.py`: The main entry point.
- `models.py`: Database schema and ORM models.
- `routes/`: Handles application endpoints.
- `templates/`: Contains HTML templates for rendering views.
- `static/`: Contains static assets like CSS and JS.
- `ai_engine.py`: Handles integrations with generative AI or game logic.

## Stack
- Backend: Flask
- Real-time: Flask-SocketIO
- Database: SQLAlchemy
- Generative AI: Google Generative AI SDK
