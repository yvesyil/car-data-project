# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster

WORKDIR /scraper

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ../data ./data

COPY . .

ENTRYPOINT [ "python3", "scraper.py" ]
CMD [ "50" ]