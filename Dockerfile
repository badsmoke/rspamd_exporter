FROM python:3-slim-buster

MAINTAINER badsmoke <dockerhub@badcloud.eu>


WORKDIR /usr/src/app



COPY ./server.py ./server.py
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python","-u","/usr/src/app/server.py" ]
