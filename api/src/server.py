from fastapi import FastAPI, HTTPException, Request, Response
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
import json
import uuid
from celery import Celery
import requests
import docker

celery_client = Celery('celery_task', broker='redis://redis:6379/0')
docker_client = docker.from_env()

app = FastAPI()

@app.post("/api/create-model")
async def model_build(request: Request):

  if not request.headers["content-type"] == "application/json":
    raise HTTPException(status_code=400)

  body = await request.body()
  payload = json.loads(body.decode('utf-8'))
  unique_id = None
  if 'url' in payload:
    unique_id = str(uuid.uuid3(uuid.NAMESPACE_URL, payload['url']))
  else:
    return None
  celery_client.send_task('celery_task.build_image', [payload['url'], unique_id])
  return unique_id

@app.post("/api/inference/{model_id}")
async def inference(request: Request, model_id):
  
  if not request.headers["content-type"] == "application/json":
    raise HTTPException(status_code=400)
  
  body = await request.body()
  payload = body.decode('utf-8')
  
  headers = {
    'content-type': "application/json",
  }

  url = 'http://' + str(model_id) + ':6534/api/'
  data = requests.request("POST", url, data=payload, headers=headers)
  return json.loads(data.text)

@app.post("/api/logs/{model_id}")
async def logs(request: Request, model_id):
  pass


@app.post("/api/update/{model_id}")
async def update(request: Request):
  pass

@app.post("/api/list-models/")
async def list_models(request: Request):

  def seperate_models(container):
    try:
      if uuid.UUID(container.name).version == 3:
        return True
    except ValueError:
      return False

  def get_github_repo(name):
    container = docker_client.containers.get(name)
    cmd = container.exec_run('cat /src/.git/config')
    split_strings = str(cmd).split('\\n')
    git_url = ''
    for item in split_strings:
      if item.find('\\turl = ') != -1:
        git_url = item.split('\\turl = ')[1]
        break
    return git_url

  container_list = docker_client.containers.list()
  model_list = filter(seperate_models, container_list)
  model_names = [m.name for m in model_list]
  ret_data = []
  for model_name in model_names:
    ret_data.append({
      "model_id" : model_name,
      "git_uri" : get_github_repo(model_name)
    })
  return ret_data


if __name__ == "__main__":
  
  config = Config()
  config.bind = ['0.0.0.0:8000']
  config.workers = 1
  asyncio.run(serve(app, config))








