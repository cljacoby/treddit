#!/bin/bash

# Run an interactive shell in the docker container.

PROJ="treddit"
PROJ_DIR="$HOME/$PROJ"
CONT_NAME="${PROJ}_cont"

echo "Running ${PROJ} container ... "
set -o xtrace

docker run \
  --rm \
  -it \
  -p 3000:3000 \
  --name ${CONT_NAME} \
  ${PROJ}
