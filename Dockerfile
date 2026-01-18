# ---------- Builder stage ----------
FROM python:3.9 AS builder
WORKDIR /app

COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# ---------- Runtime stage ----------
FROM python:3.9-slim
WORKDIR /app

# Install only prebuilt wheels from builder
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy application source
COPY . .

# Environment variables (same as before)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port
EXPOSE 5555

# Run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5555"]
