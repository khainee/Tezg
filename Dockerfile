FROM ubuntu:latest

WORKDIR /root/bot

COPY . .

RUN apt-get -y update && apt-get -y upgrade && \
    apt-get -y install python3-pip ffmpeg

RUN pip3 install --upgrade pip setuptools && \
    pip install -U -r requirements.txt

CMD ["python3","-m","bot"]
