FROM python:3.8-slim-buster

WORKDIR /src

RUN pip install watchdog watchdog[watchmedo] argh pyyaml

COPY src/requirements.txt .

RUN pip install -r requirements.txt 

COPY src/ .

EXPOSE 8000

CMD ["/bin/bash", "-c", "watchmedo auto-restart -d /src -D -R --signal SIGKILL python ./server.py"]
