FROM python:3.10-slim

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libpq-dev \
        netcat-traditional \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy only the dependencies definition file to optimize caching
COPY pyproject.toml poetry.lock ./

# Install the dependencies
RUN poetry install --no-interaction --no-ansi

# Copy the code into the container
COPY . .

# Permissions for entrypoint
RUN chmod +x entrypoint.sh

# Port to expose
EXPOSE 8000

# Use the entrypoint.sh script to start the server
ENTRYPOINT ["./entrypoint.sh"]
