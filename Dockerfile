#FROM ubuntu:16.04
#
#RUN apt-get update
#RUN apt-get install -y python3 python3-dev python3-pip nginx
#RUN pip3 install uwsgi
#
## We copy just the requirements.txt first to leverage Docker cache
#COPY ./requirements.txt /app/requirements.txt
#
#
#WORKDIR /app
#
#RUN pip3 install -r requirements.txt
#
#RUN spacy download en_core_web_sm
#
#COPY . /app
#COPY ./nginx.conf /etc/nginx/sites-enabled/default
#
#CMD service nginx start && uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=app:app
#
#ENTRYPOINT [ "python" ]
#
#CMD [ "app.py" ]

FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN python3 -m spacy download en

#RUN pip3 install spacy==2.0.18 https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.0.0/en_core_web_md-2.0.0.tar.gz

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]