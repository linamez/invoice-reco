ARG PYTHON_VERSION=3.10.13
FROM python:${PYTHON_VERSION}

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy the source code into the container.
COPY . .

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN pip install --no-cache-dir -U pip poetry && \
    poetry -vvv install --no-interaction --no-ansi --no-cache

# Switch to the non-privileged user to run the application.
# USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD poetry run uvicorn 'invoice_reco:app' --host=0.0.0.0 --port=8000
