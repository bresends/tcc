# Build stage
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Copy dependency files first
COPY uv.lock pyproject.toml ./

# Install dependencies
RUN uv sync --frozen --no-install-project --no-editable

# Copy the project into the intermediate image
COPY . /app

# Sync the project
RUN uv sync --frozen --no-editable

# Final image
FROM python:3.12-slim

# Create non-root user
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Copy the environment, but not the source code
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Copy the application code
COPY --chown=app:app . /app

# Set working directory
WORKDIR /app

# Switch to non-root user
USER app

# Expose the application port
EXPOSE 8501

# Run with Streamlit
CMD ["/app/.venv/bin/streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]