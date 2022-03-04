# Pushtify

I created this container image because I moved from Android to iPhone and didn't want to reconfigure the couple dozen applications that were using Gotify to something else.

The something else is Pushover in my case. It's not open source, it's not free, but it's been around for a very long time.

This container listens for Gotify notifications through websocket and passes them over to Pushover using ntfy.

## Requirements

- a client token in Gotify
- gotify hostname
- pushover user key

## Notes

### Build the container image locally

```bash
git clone https://github.com/sebw/pushtify
docker build -t pushtify:v0.5 .
```

### Run on Kubernetes

```bash
git clone https://github.com/sebw/pushtify
cd kubernetes
vim deployment.yaml (edit your variables, ideally store them as k8s secrets)
kubectl apply -f deployment.yaml
```

The liveness probe will restart the pod if connection to Gotify is lost.

### Run with Podman

```bash
podman run --name pushtify -e GOTIFY_TOKEN=zzz -e GOTIFY_HOST=gotify.example.org -e PUSHOVER_USERKEY=xxx docker.io/sebastienw/pushtify:v0.5
```
