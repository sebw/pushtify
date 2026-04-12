FROM alpine:3.23.3

RUN apk add --no-cache python3 py3-pip \
    && addgroup -g 1000 appgroup \
    && adduser -u 1000 -G appgroup -s /bin/sh -D appuser \
    && PIP_BREAK_SYSTEM_PACKAGES=1 pip3 install --no-cache-dir ntfy websocket-client \
    && rm -rf /var/cache/apk/* /tmp/*

WORKDIR /app

COPY --chown=appuser:appgroup pushtify-listener.py .

USER appuser

ENTRYPOINT ["python3", "pushtify-listener.py"]
