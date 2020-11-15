from fastapi import FastAPI, HTTPException, Request, Response
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
import json
from argparse import ArgumentParser

from predictor import ModelPredictor

app = FastAPI()
model_object = None
is_model_ready = False


@app.post("/api/")
async def inference(request: Request):

  if not request.headers["content-type"] == "application/json":
    raise HTTPException(status_code=400)

  body = await request.body()
  payload = json.loads(body.decode('utf-8'))

  result = None
  if is_model_ready == True:
    result = model_object.predict(payload)
  return result

def parse_arguments():
  parser = ArgumentParser(description="Run Deployed model Server")
  parser.add_argument("--port", type=str, help="specify port", required=True)
  args = parser.parse_args()
  return args

if __name__ == "__main__":
  args = parse_arguments()
  print(args.port)
  model_object = ModelPredictor(None)
  is_model_ready = True
  
  config = Config()
  config.bind = ['0.0.0.0:' + str(args.port)]
  config.workers = 1

  asyncio.run(serve(app, config))








