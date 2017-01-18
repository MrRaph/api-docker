import atexit
import docker
from pymongo import MongoClient
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime
import time
import os
import requests
import json
import logging


client = docker.DockerClient(base_url='unix://var/run/docker.sock')

# @cron.interval_schedule(minutes=1)
def getSwarmServices():
    for service in client.services.list():
        url = 'http://api-docker-api-to-mongo/docker/service'
        # url = 'http://10.150.71.164/docker/service'
        # url = 'http://192.168.1.47/docker/service'
        response = requests.post(url, json=service.attrs)
        # tasks.append(rdata.address)



if __name__ == '__main__':

    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)  # DEBUG

    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)

    mongocClient = MongoClient('mongodb://mongo1:27017,mongo2:27017,mongo3:27017/api?replicaSet=techan')
    # mongocClient = MongoClient('mongodb://10.150.71.164:27017/api')
    # mongocClient = MongoClient('mongodb://192.168.1.47:27017/api')

    jobstores = {
      'default': MongoDBJobStore(database='api', client=mongocClient)
    }

    timezone = pytz.timezone('Europe/Paris')
    scheduler = BackgroundScheduler(jobstores=jobstores, timezone=timezone)

    job = scheduler.add_job(getSwarmServices, 'interval', minutes=1)
    scheduler.start()
    # Shutdown your cron thread if the web process is stopped
    # atexit.register(lambda: scheduler.shutdown(wait=False))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
