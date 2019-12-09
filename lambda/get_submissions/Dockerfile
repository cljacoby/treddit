FROM amazonlinux

# Install dependancies
RUN yum -y update
RUN yum -y install \
    python3-devel

# Setup environment variables 
ENV PROJ="get_submissions"
ENV PROJ_DIR="/$PROJ"

# Setup project structure
RUN mkdir $PROJ_DIR
WORKDIR $PROJ_DIR
COPY get_submissions.py .  
COPY requirements.txt .

# Install python packages
RUN pip3 install -r requirements.txt

# NOTE: A `.env` file is used to set AWS credentials.
# The file is ignored in the git repo, and only used in container.
# Once on AWS, the authentication is done via IAM role.
# TODO: This isn't terrible, but still feels like not the best approach

# Copy hidden `.env` file.
COPY .env .
# RUN source ./.env
RUN set -o xtrace
RUN pwd
RUN ls -als
RUN source ./.env

# Copy bundling script to container
COPY bundle.sh .
