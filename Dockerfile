FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb x11vnc fluxbox novnc websockify wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pygame-ce

WORKDIR /game
COPY . .

ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=dummy
ENV DISPLAY=:0
ENV SCREEN_WIDTH=1024
ENV SCREEN_HEIGHT=768
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["python3", "dead_sun.py"]