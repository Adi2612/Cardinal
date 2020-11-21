import os
import docker
import sys
from git import Repo
from shutil import copy2
from shutil import rmtree

# run from root_directory of Cardinal
BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
CARDINAL_BASE_CPU = 'cardinal-cpu-base'

def clone_repository(uri, model_id):
  if os.path.isdir('models/' + model_id):
    repo = Repo('models/' + model_id)
    o = repo.remotes.origin
    o.pull()
  else:
    Repo.clone_from(uri, 'models/' + model_id)

def build_container(client, model_id):
  container_list = [item.name for  item in client.containers.list()]
  if model_id in container_list:
    old_container = client.containers.get(model_id)
    old_container.restart()
  else:
    volume_path = {}
    volume_path[os.path.join(BASE_DIRECTORY, 'pipcache')] = {
      'bind': '/root/.cache',
      'mode': 'rw'
    }
    volume_path[os.path.join(BASE_DIRECTORY, 'build', 'models', model_id)] = {
      'bind': '/src',
      'mode': 'rw'
    }
    running_res = client.containers.run(CARDINAL_BASE_CPU, 
            network='cardinal-dev', name=model_id, detach=True, volumes=volume_path)

def copy_files(model_id):
  copy2('cardinal-requirements.txt', 'models/' + model_id)
  copy2('server.py', 'models/' + model_id)
  copy2('main.sh', 'models/' + model_id)

def create_docker_image(uri, model_id):
  clone_repository(uri, model_id)
  copy_files(model_id)
  client = docker.from_env()

  try:
    build_container(client, model_id)
  except docker.errors.APIError as e:
    print("\nBuild Error: {}".format(e))
  finally:
    pass

