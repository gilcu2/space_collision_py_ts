FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      gnupg \
      unzip \
      procps \
      bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv
RUN pip install uv

# Copy pyproject.toml and poetry.lock or pdm.lock
COPY pyproject.toml uv.lock .

# Install dependencies using uv
RUN uv pip install --system --no-cache-dir --no-dev .

# Copy the source code
COPY src ./src

# Set the PYTHONPATH to include the src directory
ENV PYTHONPATH=src

# Define the command to run your application
CMD ["python", "src/api.py"]