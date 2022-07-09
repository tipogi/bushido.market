FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# 
WORKDIR /app

COPY etc/fastapi/requirements.txt /app/requirements.txt

# Install the pip and project dependencies packages
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]