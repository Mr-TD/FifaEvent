FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py

# Copy app files
COPY . .

# Expose port
EXPOSE 5000

# Run with Gunicorn WSGI server
# We use eventlet/gevent or sync workers. For Flask-SocketIO eventlet is recommended, but for simplicity we'll use threads
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "8", "--timeout", "0", "app:create_app('production')"]
