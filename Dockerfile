FROM khainezayye/ubuntu-python:ffmpeg

WORKDIR /root/bot

COPY . .

RUN pip install -U -r requirements.txt

CMD ["python3","-m","bot"]
