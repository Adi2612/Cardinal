from celery import Celery
from build_image import create_docker_image

app = Celery('celery_task', broker='redis://localhost:6379/0')

app.conf.update(
      result_expires=3600,
)

@app.task
def build_image(uri, model_id):
  create_docker_image(uri, model_id)