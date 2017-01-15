#!/bin/sh
# python /listen_docker_hooks.py -t $(cat /tocken.txt) -c sh /script.sh
export FLASK_APP=app.py
# python /app.py
python -m flask run --host=0.0.0.0
