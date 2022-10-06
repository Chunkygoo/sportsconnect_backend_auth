FROM python:3.9-slim-buster
# FROM ubuntu:focal-20220826

# ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y install \
    netcat gcc postgresql python3-pip git\
    g++ make cmake unzip libcurl4-openssl-dev\
    && apt-get clean

COPY ./app /usr/src/app
COPY ./requirements.txt /usr/src/

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /usr/src/requirements.txt
RUN pip3 install --no-cache-dir --target /usr/src awslambdaric

WORKDIR /usr/src
RUN apt-get -y install curl
RUN curl -Lo /usr/local/bin/aws-lambda-rie \
    https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie && \
    chmod +x /usr/local/bin/aws-lambda-rie

COPY entry_script.sh /usr/src
ENTRYPOINT [ "sh", "entry_script.sh" ]
CMD ["app.main.handler"]



# ============================================================================== Below is for self hosting ============================================================================== #
# FROM ubuntu:focal-20220826
# # FROM python:3.9-slim-buster
# # FROM registry.supertokens.io/supertokens/supertokens-postgresql

# ARG DEBIAN_FRONTEND=noninteractive
# ENV TZ=Etc/UTC
# RUN apt-get update && apt-get -y install \
#     netcat gcc postgresql python3-pip git curl\
#     g++ make cmake unzip libcurl4-openssl-dev\
#     && apt-get clean

# # Get Docker
# # RUN apt-get install -y apt-transport-https ca-certificates curl software-properties-common
# # RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
# # RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
# # RUN apt-get install -y docker-ce

# COPY ./app /usr/src/app
# COPY ./requirements.txt /usr/src/

# COPY ./supertokens /usr/src/supertokens
# WORKDIR /usr/src/supertokens
# RUN /usr/src/supertokens/install

# # COPY ./supertokens /tmp/supertokens
# # WORKDIR /tmp/supertokens
# # RUN /tmp/supertokens/install

# RUN pip3 install --upgrade pip
# RUN pip3 install --no-cache-dir -r /usr/src/requirements.txt
# RUN pip3 install --no-cache-dir --target /usr/src awslambdaric

# WORKDIR /usr/src
# RUN curl -Lo /usr/local/bin/aws-lambda-rie \
#     https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie && \
#     chmod +x /usr/local/bin/aws-lambda-rie

# RUN chmod -R 777 /usr/lib/supertokens
# RUN chmod -R 777 /usr/bin/supertokens
# RUN mv /usr/bin/supertokens /tmp/.
# RUN apt-get install -y libcap2-bin
# RUN setcap CAP_NET_BIND_SERVICE=+eip /tmp/supertokens
# # RUN apt-get install -y default-jdk default-jre

# COPY entry_script.sh /usr/src
# ENTRYPOINT [ "sh", "entry_script.sh" ]
# # CMD uvicorn app.main:app --reload --host=0.0.0.0 --port=8000
# CMD ["app.main.handler"]

# # cannot write to /usr/lib/supertokens/webserver-temp/