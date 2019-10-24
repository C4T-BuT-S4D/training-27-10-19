FROM mono:latest
#I HATE .net
MAINTAINER @kekov
#I HATE .net
RUN apt-get update && apt-get -y install git wget unzip libc6-dev
#I HATE .net
WORKDIR /tmp
RUN mkdir /ironpython
RUN wget https://github.com/IronLanguages/ironpython2/releases/download/ipy-2.7.9/IronPython.2.7.9.zip
RUN unzip IronPython.2.7.9.zip -d /ironpython
RUN echo "build_time_vars = {}" > /ironpython/Lib/_sysconfigdata.py
#I HATE .net
WORKDIR /app
#I HATE .net
ADD src /app

CMD ["mono", "/ironpython/net45/ipy.exe", "app.py"]