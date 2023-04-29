FROM khainezayye/python:ubuntu

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

COPY requirements.txt .

RUN pip install -U -r requirements.txt

COPY . .

CMD bash start.sh
