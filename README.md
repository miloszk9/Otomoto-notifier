# Otomoto notifier

## Prerequirements
* Docker

## Installation
```sh
$ docker build -t otomoto-notifier .
$ docker run -d \
  --name=otomoto-notifier \
  --mount type=bind,source="$(pwd)"/volume,target=/app/volume \
  otomoto-notifier:latest
```