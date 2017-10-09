# our base image
FROM alpine:3.5
MAINTAINER Kevin Kuhls <kekuhls@cisco.com>

# Install python and pip
# took off pip install shade as ssl issue with cinderclient
RUN apk add --update python2-dev py2-pip openssl-dev libffi-dev musl-dev libxml2-dev libxslt-dev openssh gcc git linux-headers make\
    && pip install --upgrade pip \
    && pip install ansible requests xlrd lxml ncclient netaddr xmltodict ucsmsdk imcsdk\
    && git clone https://github.com/ciscoucs/ucsm-ansible \
    && cd ucsm-ansible \
    && python install.py \
    && cd .. \
    && git clone https://github.com/ciscoucs/imc-ansible \
    && cd imc-ansible \
    && python install.py \
    && cd .. \
    && git clone https://github.com/kuhlskev/ucsmsdk_scripts \
    && apk del --update gcc \
    && rm -rf /var/cache/apk/* \
    && mkdir -p ~/.ssh \
    && printf "StrictHostKeyChecking no\nHostKeyAlgorithms +ssh-dss\n" \\
        >> ~/.ssh/config \
    && chmod -R 600 ~/.ssh \
    && touch ~/.ssh/known_hosts

WORKDIR /home/docker
CMD ["/bin/sh"]
