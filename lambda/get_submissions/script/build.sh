#!/bin/bash

# Build the docker image

PROJ="get_submissions"
PROJ_DIR="$HOME/treddit/lambda/get_submissions"

echo "Building the ${PROJ} image ... "
set -o xtrace

docker build \
  -t ${PROJ} \
  ${PROJ_DIR} \
  -f ${PROJ_DIR}/Dockerfile
