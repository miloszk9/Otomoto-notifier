# Otomoto notifier

## Prerequirements
* Container tool like Docker or Podman

## Installation
```sh
$ podman build -t otomoto-notifier .
$ podman run -d \
  -v "$(pwd)"/volume:/app/volume:Z \
  --name=otomoto-notifier \
  --network=podman \
  otomoto-notifier:latest
```