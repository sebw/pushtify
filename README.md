# Pushtify

Gotify to Pushover forwarder:

- Gotify: a self hosted Open Source notification system, with an Android app.
- Pushover: a PaaS closed source notification system. Available on iOS and Android.

## Why this container image

Because I moved from Android to iPhone.

I run about 20 applications that notify Gotify on a daily basis.

I didn't want to reconfigure all of those to notify on a new iOS compatible notification system (here Pushover).

## How it works

This container constantly listens for Gotify notifications through websocket and forwards received notifications to Pushover. 

It uses the `ntfy` Python library to forward messages.

## Requirements

- a client token in Gotify
- the gotify hostname
- a pushover user key

## Notes

### Building the container image locally

```bash
git clone https://github.com/sebw/pushtify
docker build -t pushtify:v0.5 .
```

### Running on Kubernetes

```bash
git clone https://github.com/sebw/pushtify
cd kubernetes
vim deployment.yaml (edit your variables, ideally store them as k8s secrets)
kubectl apply -f deployment.yaml
```

If connection to Gotify websocket is lost, the Python script will stop and the liveness probe will fail, triggering a restart of the pod.

### Running with Podman (or Docker)

```bash
podman run --name pushtify -e GOTIFY_TOKEN=zzz -e GOTIFY_HOST=gotify.example.org -e PUSHOVER_USERKEY=xxx ghcr.io/sebw/pushtify:v0.5
```
