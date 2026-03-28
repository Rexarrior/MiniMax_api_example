FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg gcc python3-dev libasound2-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ../examples_python/ ./examples_python/
COPY engine/ ./engine/
COPY web_ui/ ./web_ui/
COPY stories/ ./stories/
COPY scripts/ ./scripts/
COPY run_novel.py .

RUN ln -s /app/examples_python /examples_python

ENV PYTHONPATH=/app:/app/examples_python
EXPOSE 8080

CMD ["python", "run_novel.py", "--web"]
