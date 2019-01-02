FROM resin/raspberry-pi-python:3

RUN apt-get update && apt-get install -y \
    python-pip

RUN pip install pipenv

WORKDIR /usr/src/app

COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install

COPY . .

CMD [ "pipenv", "run", "python", "./main.py" ]
