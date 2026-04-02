FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg gcc python3-dev libasound2-dev curl

WORKDIR /app

RUN printf 'fastapi>=0.104.0\nuvicorn[standard]>=0.24.0\nhttpx>=0.25.0\npyyaml>=6.0\nsimpleaudio>=1.0.4\npillow>=10.0.0\nmutagen>=1.47.0\npython-multipart>=0.0.6\n' > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

RUN mkdir -p engine

ADD engine/__init__.py engine/
ADD engine/story.py engine/
ADD engine/scene.py engine/
ADD engine/choices.py engine/
ADD engine/renderer.py engine/
ADD engine/minimax_client.py engine/
ADD engine/api_server.py engine/

ENV PYTHONPATH=/app
ENV STORIES_DIR=/app/stories

EXPOSE 5000

CMD ["uvicorn", "engine.api_server:app", "--host", "0.0.0.0", "--port", "5000"]