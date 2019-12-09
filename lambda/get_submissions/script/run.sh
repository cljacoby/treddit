#!/bin/bash

# Run an interactive shell in the docker container.

PROJ="get_submissions"
PROJ_DIR="$HOME/treddit/lambda/get_submissions"
CONT_NAME="${PROJ}_cont"

echo "Running ${PROJ} container ... "
set -o xtrace

# TODO: I'm running the http server just to keep the container alive
# in deamon mode. I want to cp the file out to local file system.
docker run \
  --rm \
  -d \
  -p 3000:3000 \
  --name ${CONT_NAME} \
  --entrypoint python3 \
  ${PROJ} \
  -m http.server

docker exec -d ${CONT_NAME} /bin/bash
uname
