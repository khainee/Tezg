FROM khainezayye/ubuntu-python:ffmpeg

WORKDIR /root/bot

COPY requirements.txt .

RUN pip install -U -r requirements.txt

COPY . .

CMD ["python3","-m","bot"]
