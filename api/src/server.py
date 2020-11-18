from fastapi import FastAPI, HTTPException, Request, Response
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
import json
import redis
import uuid


app = FastAPI()
redis_client = redis.Redis(host='redis', port=6379, db=0)

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
  redis_client.set(unique_id, payload['url'])
  return unique_id

@app.post("/api/inference/{model_id}")
async def inference(request: Request):
  
  if not request.headers["content-type"] == "application/json":
    raise HTTPException(status_code=400)
  
  body = await request.body()
  payload = json.loads(body.decode('utf-8'))
  return None

@app.post("/api/logs/{model_id}")
async def logs(request: Request):
  pass

@app.post("/api/update/{model_id}")
async def update(request: Request):
  pass

@app.post("/api/list-models")
async def list_models(request: Request):
  pass




if __name__ == "__main__":
  
  config = Config()
  config.bind = ['0.0.0.0:8000']
  config.workers = 1
  asyncio.run(serve(app, config))








