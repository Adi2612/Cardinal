# Cardinal

Deploy Trained Models and create Rest APIs.


## Directory Structure

- `app/` : Contains the UI code for the cardinal dashboard
- `build/` : Contains the code for cloning and building docker container
- `local-dev-stack/` : Contains the code for grouping the code and running the services
- `api/` : Contains the code for handling the backend requests

## Requirements 

1. Setup [docker](https://docs.docker.com/get-started/) and [docker-compose](https://docs.docker.com/compose/gettingstarted/) in your machine.
2. `docker network create cardinal-dev`
3. `python3 -m venv env`
4. Go to `local-dev-stack` directory and run `docker-compose up -d`
5. Inside the `build` directory, run `pip install -r requirements.txt`
6. Inside the `build` directory, run `celery -A celery_task worker -l INFO`


## Ports 

- `8000` api
- `8080` app
- `6379` redis
- `3333` nginx
