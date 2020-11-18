import os
import docker
import sys
import yaml
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

VARIABLE_MAP = {
  "{{COPY}}" : None,
  "{{COMMAND}}": None,
  "{{EXPOSE}}": None
}


def clone_repository(uri, model_id):
  if os.path.isdir('models/' + model_id):
    repo = Repo('models/' + model_id)
    o = repo.remotes.origin
    o.pull()
  else:
    Repo.clone_from(uri, 'models/' + model_id)

def replace_lines(infile, outfile, replace_dict):
  for line in infile:
    key = line.rstrip()
    if key in replace_dict:
      outfile.write("\n" + replace_dict[key])
    else:
      outfile.write(line)

def process_docker_file(model_id, replace_dict):
  src_docker_file = os.path.join(BASE_DIRECTORY, 'build', 'Dockerfile.template')
  dest_docker_file = 'models/' + model_id + '/Dockerfile'
  with open(src_docker_file, "r") as infile, open(dest_docker_file, "w") as outfile:
    replace_lines(infile, outfile, replace_dict)
  return dest_docker_file

def set_variable_map(model_id, port):
  VARIABLE_MAP["{{CMD}}"] = 'CMD ["/bin/bash", "-c", "source activate cardinal-env ; python server.py --port ' + str(port) +'"]'
  VARIABLE_MAP["{{EXPOSE}}"] = 'EXPOSE ' + str(port)

def build_image(client, model_id):
  os.chdir(os.path.join(BASE_DIRECTORY, 'build', 'models', model_id))
  response = client.api.build(
    path='.', tag=model_id , quiet=False, decode=True
  )

  for line in response:
    if list(line.keys())[0] in ("stream", "error"):
      value = list(line.values())[0]
      if value:
        print(value.strip())

  running_res = client.containers.run(model_id, network='cardinal-dev', name=model_id, detach=True)
  for line in running_res:
    if list(line.keys())[0] in ("stream", "error"):
      value = list(line.values())[0]
      if value:
        print(value.strip())

def copy_files(model_id):
  copy2('cardinal-requirements.txt', 'models/' + model_id)
  copy2('server.py', 'models/' + model_id)

def create_docker_image(uri, model_id, port):
  clone_repository(uri, model_id)
  set_variable_map(model_id, port)
  copy_files(model_id)
  process_docker_file(model_id, VARIABLE_MAP)

  client = docker.from_env()

  try:
    build_image(client, model_id)
  except docker.errors.APIError as e:
    print("\nBuild Error: {}".format(e))
  finally:
    pass

