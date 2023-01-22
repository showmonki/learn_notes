#FROM ubuntu:18.04
FROM pytorch/pytorch:latest

MAINTAINER zz "zz"

COPY ./requirements.txt /requirements.txt
COPY ./nginx.conf /nginx.conf
ENV PYTHONIOENCODING=UTF-8
#ENV LC_ALL=zh_CN.UTF-8 LANG=zh_CN.UTF-8
WORKDIR /

RUN apt-get update && apt-get install -y nginx uwsgi uwsgi-plugin-python3
RUN pip3 install -r requirements.txt
#RUN apt-get install -y locales && locale-gen zh_CN.UTF-8

COPY . /
RUN adduser --disabled-password --gecos '' nginx\
  && chown -R nginx:nginx /app \
  && chmod 777 /run/ -R \
  && chmod 777 /root/ -R

ENTRYPOINT [ "bash","entry-point.sh"]
#CMD ['run_flask.sh']
#ENTRYPOINT [ "python3"]
#CMD ['app.py']