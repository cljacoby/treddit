#!/bin/bash

# Run the docker container.
# Runs `cargo run` and exits.


PROJ="rust_req"
PROJ_DIR="/Users/chris/${PROJ}"
CONT_NAME="${PROJ}_cont"

echo "Running ${PROJ} container ... "

docker run \
  --rm \
  -it \
  -p 3000:3000 \
  --name ${CONT_NAME} \
  --entrypoint cargo \
  ${PROJ} \
  run
