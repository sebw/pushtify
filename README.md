# Pushtify

Capture Gotify notifications and forward them to Pushover.

I created this container because I moved from Android to iPhone and didn't want to reconfigure the couple dozen applications that were using Gotify.

The container listens to Gotify's websocket and captures notifications and pass then to Pushover using ntfy.

Requirement:

- a client token in Gotify
- gotify hostname
- pushover user key

Notes:

- if deployed in Kubernetes, the pod will restart in case of connection loss with Gotify

Built the container image locally:

```bash
git clone https://github.com/sebw/pushtify
docker build -t pushtify:v.04 .
```
