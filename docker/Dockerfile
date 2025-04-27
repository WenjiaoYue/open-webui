# Copyright (C) 2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

FROM node:22.9.0

ENV LANG=C.UTF-8
ARG ARCH=cpu

RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    build-essential \
    libgl1-mesa-glx \
    libjemalloc-dev \
    git \
    python3-venv


WORKDIR /root/

ENV HOME=/root
ENV VIRTUAL_ENV=$HOME/.env/open-webui


RUN git clone https://github.com/WenjiaoYue/open-webui.git && \
    mkdir -p $HOME/.env && python3 -m venv $VIRTUAL_ENV && \
    $VIRTUAL_ENV/bin/python -m pip install --no-cache-dir --upgrade pip && \
    $VIRTUAL_ENV/bin/python -m pip install --no-cache-dir build

WORKDIR /root/open-webui

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN git checkout wenjiao/DCAI_Web_search 

WORKDIR /root/open-webui/backend
RUN pip install -r requirements.txt -U

WORKDIR /root/open-webui

RUN python -m build && \
    pip install --no-cache-dir dist/open_webui-0.5.20-py3-none-any.whl    


WORKDIR /root/

RUN rm -fr /root/open-webui

ENTRYPOINT ["open-webui", "serve"]