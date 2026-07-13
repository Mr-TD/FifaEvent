FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock

# Copy app files
COPY . .

# Expose port
EXPOSE 5000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
