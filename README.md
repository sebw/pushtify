# Pushtify

Pushtify is a Gotify to Pushover forwarder:

- Gotify: a self hosted Open Source notification system, with an Android app.
- Pushover: a PaaS closed source notification system. Available on iOS and Android.

## Why this container image?

When I moved from Android to iOS, I was just too lazy to reconfigure the multiple dozens of apps that were sending notifications to my Gotify instance.

## How it works

This container constantly listens for Gotify notifications through websocket and forwards received notifications to Pushover. 

It uses the `ntfy` Python library to forward messages.

![image](https://github.com/sebw/pushtify/assets/2285094/3416109e-2a5a-4260-8b84-5baade964b10)

If the connection to Gotify is lost, the container will reinitiate the connection.

## Requirements

- a client token in Gotify
- the gotify hostname
- a pushover user key

## Installation with Docker or Podman

```bash
docker run --name pushtify \
  -e GOTIFY_TOKEN=zzz \
  -e GOTIFY_HOST=gotify.example.org \
  -e GOTIFY_PROTOCOL=https \
  -e PUSHOVER_USERKEY=xxx \
  ghcr.io/sebw/pushtify:latest
```

Replace `docker` with `podman` if you run Podman.

If `GOTIFY_PROTOCOL` is not defined, HTTPS is assumed.

You can pass `PUSHTIFY_DEBUG=true` if you want to display the incoming messages.

## Mapping Gotify Apps to Pushover Apps

By default with the example above, all Gotify messages will be forwarded to the "main" Pushover messages stream.

It is somehow possible to forward messages from a specific Gotify App to a specific Pushover app.

First of all, you need to grab the "app ID" of your app in Gotify.

In the left menu in Gotify click on your app, the URL will show `https://gotify/#/messages/55`.

`55` is the app ID.

You can now run Pushtify by passing your app ID's with the following:

```bash
docker run --name pushtify \
  -e GOTIFY_TOKEN=zzz \
  -e GOTIFY_HOST=gotify.example.org \
  -e GOTIFY_PROTOCOL=https \
  -e PUSHOVER_USERKEY=xxx \
  -e PUSHTIFY_DEBUG=true \
  -e GOTIFY_APPID_55=your_pushover_api_token \
  -e GOTIFY_APPID_12=your_other_pushover_api_token \
  ghcr.io/sebw/pushtify:latest
```

Gotify messages that don't match any ID will be forwarded to the "root" Pushover message stream.

## Building the container image yourself

```bash
git clone https://github.com/sebw/pushtify
cd pushtify
docker build -t pushtify:latest .
```

## Running Pushtify on Kubernetes

```bash
git clone https://github.com/sebw/pushtify
cd pushtify/kubernetes
vim deployment.yaml (edit your variables, ideally store them as k8s secrets)
kubectl apply -f deployment.yaml
```

If connection to Gotify websocket is lost, the Python script will stop and the liveness probe will fail, triggering a restart of the pod.

## Message Priorities

Gotify and Pushover implement priorities.

I took the liberty to map priorities in such a way:

| Gotify Behavior | Gotify Priority | Pushover Priority | Pushover Behavior |
|- |-| -|-|
| No notification | 0 | -1| Low priority|
| Icon in notification bar | 1 - 3 | 0 | Normal priority| 
| Icon in notification bar + Sound | 4 - 7 | 1 | High Priority |
| Icon in notification bar + Sound + Vibration | 8 - 10 | 2| Emergency priority|
