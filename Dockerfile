FROM alpine:3.21
RUN apk add --no-cache py3-pip && PIP_BREAK_SYSTEM_PACKAGES=1 pip3 install ntfy && PIP_BREAK_SYSTEM_PACKAGES=1 pip3 install websocket-client && rm -fr /var/cache/*
RUN sed -i 's/getargspec/getfullargspec/' /usr/lib/python3.12/site-packages/ntfy/__init__.py
RUN sed -i 's/getargspec/getfullargspec/' /usr/lib/python3.12/inspect.py
COPY pushtify-listener.py /usr/local/bin
ENTRYPOINT ["python3","/usr/local/bin/pushtify-listener.py"]
