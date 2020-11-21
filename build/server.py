from fastapi import FastAPI, HTTPException, Request, Response
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
import json
import numpy as np
from argparse import ArgumentParser

from predictor import ModelPredictor

class NumpyEncoder(json.JSONEncoder):
  """ Special json encoder for numpy types """
  def default(self, obj):
    if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
      np.int16, np.int32, np.int64, np.uint8,
      np.uint16, np.uint32, np.uint64)):
      return int(obj)
    elif isinstance(obj, (np.float_, np.float16, np.float32, 
      np.float64)):
      return float(obj)
    elif isinstance(obj,(np.ndarray,)):
      return obj.tolist()
    return json.JSONEncoder.default(self, obj)

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
  return json.dumps(result, cls=NumpyEncoder)

def parse_arguments():
  parser = ArgumentParser(description="Run Deployed model Server")
  parser.add_argument("--port", type=str, help="specify port", required=True)
  args = parser.parse_args()
  return args

if __name__ == "__main__":
  args = parse_arguments()
  model_object = ModelPredictor(None)
  is_model_ready = True
  
  config = Config()
  config.bind = ['0.0.0.0:' + str(args.port)]
  config.workers = 1

  asyncio.run(serve(app, config))








