FROM ubuntu:18.04
MAINTAINER Vladimir Elfimov
RUN apt-get -y update
RUN apt-get install -y python3
RUN apt-get install -y python3-dev
RUN apt-get -y install python3-pip

ADD . ./server/
RUN pip3 install -r ./server/requirements.txt

EXPOSE 80

CMD python3 ./server/server_start.py