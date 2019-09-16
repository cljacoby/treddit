#!/bin/bash

# Build the docker image

PROJ="treddit"
PROJ_DIR="$HOME/$PROJ"

echo "Building the ${PROJ} image ... "
set -o xtrace

docker build \
  -t ${PROJ} \
  ${PROJ_DIR} \
  -f ${PROJ_DIR}/Dockerfile
