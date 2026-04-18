FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl unzip && \
    curl -L https://github.com/tsl0922/ttyd/releases/latest/download/ttyd.x86_64 -o /usr/local/bin/ttyd && \
    chmod +x /usr/local/bin/ttyd && \
    apt-get purge -y curl unzip && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /game
COPY . .

EXPOSE 7681

CMD ["ttyd", "-p", "7681", "-W", "python3", "dead_sun.py"]
