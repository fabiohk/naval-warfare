FROM python:3.8-slim

# Creates application directory
WORKDIR /app

# Creates an appuser and change the ownership of the application's folder
RUN useradd appuser && chown appuser /app

# Copy dependency definition to cache
COPY --chown=appuser Pipfile.lock Pipfile /app/

# Installs projects dependencies as a separate layer
RUN python -m pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

# Copies and chowns for the userapp on a single layer
COPY --chown=appuser . /app

# Switching to the non-root appuser for security
USER appuser