# Cardinal

Deploy Trained Models and create Rest APIs.


## Directory Structure

- `app/` : Contains the UI code for the cardinal dashboard
- `build/` : Contains the code for cloning and building docker container
- `local-dev-stack/` : Contains the code for grouping the code and running the services
- `api/` : Contains the code for handling the backend requests
- `image/` : Contains the bases docker images
## Requirements 

1. Setup [docker](https://docs.docker.com/get-started/) and [docker-compose](https://docs.docker.com/compose/gettingstarted/) in your machine.
2. `docker network create cardinal-dev`
3. `python3 -m venv env`
4. `source env/bin/activate`
5. Inside the `app` directory, run `yarn`
6. Inside the `local-dev-stack` directory, run `docker-compose up -d`
7. Inside the `image` directory, run `docker build -t cardinal-cpu-base .`
8. Inside the `build` directory, run `pip install -r requirements.txt`
9. Inside the `build` directory, run `celery -A celery_task worker -l INFO`

## Run

### For Deploying a Model
- Go to `localhost:3333/app`

### For Seeing logs of a Model
- Go to `localhost:3333/app/<model-id>`

### For Inferecing a Deployed Model
- Go to `localhost:3333/app/inference/<model-id>`

### For Seeing a list of Deployed Models
- Go to `localhost:3333/app/list`

## Ports 

- `8000` api
- `8080` app
- `6379` redis
- `3333` nginx
