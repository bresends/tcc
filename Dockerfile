# Build stage
FROM python:3.12-slim AS builder

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency specs first and install dependencies only
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Copy source code and install project
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Production stage
FROM python:3.12-slim AS production

# Create non-root user
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Copy the virtual environment from builder stage
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Copy application code
COPY --chown=app:app . /app

WORKDIR /app

# Switch to non-root user
USER app

# Expose Streamlit default port
EXPOSE 8501

# Launch Streamlit via uv-managed environment
CMD ["/app/.venv/bin/streamlit", "run", "src/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]