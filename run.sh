#!/bin/sh
export FLASK_APP=app.py

sed -i.bak '/search cloud.online.net/d' /etc/resolv.conf

python -m flask run --host=0.0.0.0
