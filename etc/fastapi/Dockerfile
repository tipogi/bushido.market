FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY etc/fastapi/requirements.txt /app/requirements.txt

# Install the pip and project dependencies packages
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV PORT=8081

## Docker health check
HEALTHCHECK --interval=300s --timeout=15s --start-period=20s --retries=3 \
            CMD curl http://nokyc-api:8081/docker-healthcheck


CMD ["uvicorn", "app.main:app"]