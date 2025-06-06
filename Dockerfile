# Use Python 3.13-slim as base image (alpine is smaller, but longer to build and less compatible)
FROM python:3.13-slim
# Copy latest uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies with lockfile verification
RUN uv sync --locked

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
