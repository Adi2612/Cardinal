import os
import docker
import sys
from git import Repo
from shutil import copy2
from shutil import rmtree

'''
Clone the Repository
Copy server.py file in the repo directory.
Copy the content of all the files to a single directory.
Create docker container
Install python packages mentioned in requirements.txt
Start the server. -- Load the model
Expose the port to the outside world.
'''

# Setup file structure
'''
Cardinal
  -/build/
    -build_image.py
    -Dockerfile.template
  -/server.py
  -/cardinal-requirements.txt
  -/models
    -<model-id>/
      -predictor.py
      -requirements.txt
'''

# File Structure inside Docker
'''

Model
  -server.py
  -predictor.py
  -requirements.txt
  -cardinal-requirements.txt
  -<other-files-in-models>
  -Dockerfile
'''


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
    old_container.stop()
    old_container.remove()
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
  # set_variable_map(model_id, port)
  copy_files(model_id)
  # process_docker_file(model_id, VARIABLE_MAP)
  client = docker.from_env()

  try:
    build_container(client, model_id)
  except docker.errors.APIError as e:
    print("\nBuild Error: {}".format(e))
  finally:
    pass

