# pull official base image
FROM python:3.12.1-bookworm

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat-traditional gcc postgresql \
    && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./backend/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . .
