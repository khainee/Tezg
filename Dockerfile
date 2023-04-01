FROM khainezayye/ubuntu-python:ffmpeg

WORKDIR /root/bot

RUN apt-get install -y aria2 curl

COPY requirements.txt .

RUN pip install -U -r requirements.txt

COPY . .

CMD bash start.sh
