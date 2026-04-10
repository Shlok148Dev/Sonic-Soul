FROM python:3.10-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libsndfile1 git curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt requirements-api.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-api.txt

# Copy source
COPY psyche-core/ psyche-core/
COPY psyche-api/ psyche-api/
COPY configs/ configs/
COPY pyproject.toml ./

# Install psyche-core
RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "psyche_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
