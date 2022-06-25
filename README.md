# Pushtify

Gotify to Pushover forwarder:

- Gotify: a self hosted Open Source notification system, with an Android app.
- Pushover: a PaaS closed source notification system. Available on iOS and Android.

## Why this container image

Because I moved from Android to iPhone and didn't want to migrate about 20 applications from Gotify to another system that would be iOS compatible. The other system in my case is Pushover.

## How does it work

This container listens for Gotify notifications through websocket and passes them over to Pushover. It uses the `ntfy` Python library to forward the messages.

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

If connection to Gotify websocket is lost, the Python script will stop and the liveness probe will restart the pod.

### Run with Podman

```bash
podman run --name pushtify -e GOTIFY_TOKEN=zzz -e GOTIFY_HOST=gotify.example.org -e PUSHOVER_USERKEY=xxx ghcr.io/sebw/pushtify:v0.5
```
