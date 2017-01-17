from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_pymongo import PyMongo
import json
from pprint import pprint

app = FlaskAPI(__name__)
app.config['MONGO_DBNAME'] = 'api'
# app.config['MONGO_URI'] = 'mongodb://mongo1:27017,mongo2:27017,mongo3:27017/api?replicaSet=techan'
app.config['MONGO_URI'] = 'mongodb://10.150.71.164:27017/api'
mongo = PyMongo(app)

@app.route('/service', defaults={'service_name': None}, methods=['POST'])
@app.route('/service/<service_name>', methods=['GET'])
def service(service_name):
    if request.method == 'GET':
        service = mongo.db.services.find_one_or_404({'service': service_name})

        return {
            "service": service['service'],
            "created": False
        }
    elif request.method == 'POST':
        data = request.json

        services = mongo.db.services
        service_id = services.insert_one(data).inserted_id

        return {
            'service': data['service'],
            'created': True,
        }
    return "Toto"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
    # app.run(host='0.0.0.0', port=80)
