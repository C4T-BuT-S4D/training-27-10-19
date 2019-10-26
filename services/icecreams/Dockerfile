FROM mono:latest

MAINTAINER @jnovikov

RUN apt-get update && apt-get install wget unzip -y &&\
    wget http://pascalabc.net/downloads/PABCNETC.zip -O /tmp/PABCNETC.zip &&\
    mkdir /opt/pabcnetc &&\
    unzip /tmp/PABCNETC.zip -d /opt/pabcnetc 

ADD src /app

WORKDIR /app

RUN mono /opt/pabcnetc/pabcnetc.exe main.pas
CMD ["mono", "main.exe"]