# Dockerfile

FROM python:3.11-slim

WORKDIR /service

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy 
COPY . .

# Install dependencies
RUN poetry install

# Set environment variables (or pass them during runtime)
ENV PYTHONUNBUFFERED=1

CMD ["poetry", "run", "python", "main.py"]
