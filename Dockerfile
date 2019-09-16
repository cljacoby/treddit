FROM rust:latest


# set env variables
ENV USER="cljacoby"
ENV PROJ="treddit"
ENV PROJ_DIR=/root/${PROJ}


# Compiling dependencies first to allow docker to cache.
# Doing this first best reduces long docker image builds due to dependency compiling.
# Based on: http://whitfin.io/speeding-up-rust-docker-builds/
WORKDIR ${PROJ_DIR}
RUN cargo init --bin
COPY Cargo.toml .
# COPY Cargo.lock .
RUN cargo build


# install basic dev tools
RUN apt-get update
RUN apt-get install -y \
  vim \
  zsh

# Install oh-my-zsh terminal cuz I'm spoiled
ARG OHMYZSH_URL=https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh
RUN wget ${OHMYZSH_URL} -O - | zsh || true

# TODO: This doesn't work for colorized outpuot during build,
# determine if it works during run, and figure out way for build.
ENV XTERM="xterm-256color"

# Compile actual  src tree 
RUN rm src/main.rs
COPY src src
RUN touch src/main.rs
RUN cargo build

# Copy data directory
# COPY data data


# Copy tredditpy python sub-project over

# default entry is interactive terminal
ENTRYPOINT /usr/bin/zsh

