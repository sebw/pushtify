# Pushtify

I created this container because I moved from Android to iPhone and didn't want to reconfigure the couple dozen applications that were using Gotify to something else.

The something else is Pushover in my case. It's not open source, it's not free, but it's been around for a very long time.

This container listens for Gotify notifications through websocket and passes them over to Pushover using ntfy.

Requirements:

- a client token in Gotify
- gotify hostname
- pushover user key

Notes:

- if deployed in Kubernetes, the pod will restart in case of connection loss with Gotify

Build the container image locally:

```bash
git clone https://github.com/sebw/pushtify
docker build -t pushtify:v.04 .
```
