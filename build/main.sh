#!/usr/bin/env bash

source activate cardinal-env
pip install -r requirements.txt
pip install -r cardinal-requirements.txt
python server.py --port 6534