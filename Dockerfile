FROM alpine:3.15
RUN apk add py3-pip && pip3 install ntfy && pip3 install websocket-client
ARG GOTIFY_TOKEN=xyz
ARG GOTIFY_HOST=gotify.example.org
ARG PUSHOVER_USERKEY=abcdefghijklmnopqrstuvwxyz
COPY pushtify-listener.py /usr/local/bin
ENTRYPOINT ["python3","/usr/local/bin/pushtify-listener.py"]
