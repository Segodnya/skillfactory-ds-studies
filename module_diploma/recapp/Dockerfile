FROM ubuntu:latest

RUN set -xe \
    && apt-get update \
    && apt-get install python3-pip -y

COPY ./requirements.txt /recapp/requirements.txt
WORKDIR /recapp
RUN pip install -r requirements.txt

COPY . /recapp

ENTRYPOINT ["python3", "recapp.py"]