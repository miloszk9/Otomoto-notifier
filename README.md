# Otomoto notifier

## Prerequirements
* Container tool like Docker or Podman

## Installation
```sh
$ docker build -t otomoto-notifier .
$ docker run -d \
  -v "$(pwd)"/volume:/app/volume:Z \
  --name=otomoto-notifier \
  otomoto-notifier:latest
```