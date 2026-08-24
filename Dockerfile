FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY read_airgradient_docker.py .

CMD ["python", "read_airgradient_docker.py"]