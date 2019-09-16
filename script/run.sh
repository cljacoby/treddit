#!/bin/bash

# Run the docker container with `cargo run` as entry.

PROJ="treddit"
PROJ_DIR="$HOME/$PROJ"
CONT_NAME="$PROJ_cont"

echo "Running $PROJ container ... "

docker run \
  --rm \
  -it \
  -p 3000:3000 \
  --name ${CONT_NAME} \
  --entrypoint cargo \
  ${PROJ} \
  run
