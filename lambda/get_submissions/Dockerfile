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



