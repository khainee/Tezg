FROM khainezayye/python:alpine

WORKDIR /root/bot
COPY requirements.txt .

RUN pip install -U -r requirements.txt

COPY . .

CMD bash start.sh
