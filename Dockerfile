FROM python:3.12-slim

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency specs first and install
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Copy rest of the application
COPY . /app

# Expose Streamlit default port
EXPOSE 8501

# Launch Streamlit via uv-managed environment
CMD ["/app/.venv/bin/streamlit", "run", "src/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]