#!/bin/bash

ROOT="$(dirname "$(dirname "$(readlink -fm "${BASH_SOURCE[0]}")")")"

CMD="cd ${ROOT} && make push"

echo "$DOCKER_HUB_PASSWORD" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin
eval ${CMD}

