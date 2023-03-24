FROM khainezayye/ubuntu-python:ffmpeg

WORKDIR /root/bot

COPY . .

RUN pip3 install --upgrade pip setuptools && \
    pip install -U -r requirements.txt

CMD ["python3","-m","bot"]
