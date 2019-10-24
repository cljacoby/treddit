#!/bin/bash

# Run the docker container with `cargo run` as entry.

PROJ="get_submissions"
PROJ_DIR="$HOME/treddit/lambda/get_submissions"
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
