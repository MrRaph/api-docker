from flask import Flask, request, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
# connect to another MongoDB server altogether
app.config['MONGO_URI'] = 'mongodb://mongo1:27017,mongo2:27017,mongo3:27017/api?replicaSet=techan'
mongo = PyMongo(app, config_prefix='MONGO')

if __name__ == "__main__":
    app.run(debug=True)
