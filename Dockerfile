FROM python:3.9.1-buster

WORKDIR /root/bot

COPY . .

RUN apt-get -y update && apt-get -y upgrade

RUN apt-get install -y ffmpeg

RUN pip3 install --upgrade pip setuptools

RUN pip install -U -r requirements.txt

# Starting Worker
CMD ["python3","-m","bot"]
