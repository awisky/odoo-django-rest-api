
#!/bin/bash
# -*- coding: utf-8 -*-
# Agustin Wisky <agustinwisky@gmail.com> 
# See LICENSE file for full copyright and licensing details.

FROM python:3

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Configure apt and install packages for OCR
RUN apt-get update -y && \
    apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    poppler-utils \
    wget \
    git \
    gettext \
    # cleanup
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/li

# Set environment variables
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /


# Install dependencies.
RUN pip install -r /requirements.txt

# Set work directory.
RUN mkdir /code
WORKDIR /code

# Copy project code.
COPY . /code/

EXPOSE 8080


WORKDIR /code
USER root

