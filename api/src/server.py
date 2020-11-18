from fastapi import FastAPI, HTTPException, Request, Response
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
import json


app = FastAPI()


@app.post("/api/model_build")
async def model_build(request: Request):

  if not request.headers["content-type"] == "application/json":
    raise HTTPException(status_code=400)

  body = await request.body()
  payload = json.loads(body.decode('utf-8'))

  result = {"hello": "world"}
  return result


if __name__ == "__main__":
  
  config = Config()
  config.bind = ['0.0.0.0:8000']
  config.workers = 1
  asyncio.run(serve(app, config))








