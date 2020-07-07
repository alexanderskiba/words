# src: build/backend/Dockerfile

# Используем за основу контейнера Ubuntu 18.04 LTS
FROM ubuntu:18.04
RUN apt-get update
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Добавляем необходимые репозитории и устанавливаем пакеты
RUN apt-get install -y git
RUN apt-get install -y python3-pip
RUN apt-get install -y software-properties-common

RUN add-apt-repository -y ppa:nginx/stable
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 4F4EA0AAE5267A6C
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y wget curl nginx
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update
RUN apt-get install -y postgresql-12
RUN pip3 install requests psycopg2-binary sqlalchemy click flask




