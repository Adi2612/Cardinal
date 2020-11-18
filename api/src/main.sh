#!/usr/bin/env bash


watchmedo auto-restart -d /src -D -R --signal SIGKILL python server.py
