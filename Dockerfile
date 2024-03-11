# The builder image, used to build the virtual environment
FROM python:3.11-buster as builder

# Install Poetry
RUN pip install poetry==1.4.2

# Set environment variables for Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set working directory
WORKDIR /app

# Copy only the dependency files
COPY pyproject.toml poetry.lock ./

# Create a placeholder README file
RUN touch README.md

# Install project dependencies using Poetry
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster as runtime

# Set environment variables
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copy the virtual environment from the builder stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy the application code
COPY src ./src

WORKDIR src

# Run the application using gunicorn with 8 workers at port 1911
CMD ["gunicorn", "-w", "8", "-b", "0.0.0.0:1911", "wsgi:flask_api"]