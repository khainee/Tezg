FROM khainezayye/python:ubuntu

WORKDIR /root/bot
COPY requirements.txt .

RUN pip install -U -r requirements.txt

COPY . .

CMD bash start.sh
