#!/bin/bash

# Build the docker image

PROJ="rust_req"
PROJ_DIR="/Users/chris/${PROJ}"

echo "Building the ${PROJ} image ... "

docker build \
  -t ${PROJ} \
  ${PROJ_DIR} \
  -f ${PROJ_DIR}/Dockerfile
