# Dockerfile

# --- Builder Stage ---
FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Add poetry's potential bin directory to PATH
ENV PATH="/root/.local/bin:$PATH"

# Install build tools and curl (for poetry installer)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*

# Install poetry using the official installer
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# Configure Poetry *not* to create virtualenvs within the project directory
# This should make it install to system site-packages or user site-packages
RUN poetry config virtualenvs.create false

COPY pyproject.toml ./

# Install dependencies. Packages should go to site-packages.
# Executables might go to /root/.local/bin
RUN poetry install --no-interaction --no-ansi --with main --no-root

# --- Final Stage ---
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy installed packages from builder's system site-packages
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy executables installed by poetry
COPY --from=builder /root/.local/bin /usr/local/bin

# Ensure the target site-packages directories are in PYTHONPATH
ENV PYTHONPATH="/usr/local/lib/python3.12/site-packages"

# Application code is mounted via docker-compose volume into /app
# No COPY . . needed here

EXPOSE 8000

# Run uvicorn directly.
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
