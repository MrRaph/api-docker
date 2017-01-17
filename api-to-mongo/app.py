from flask import Flask, request, url_for
from flask_pymongo import PyMongo
import json

app = FlaskAPI(__name__)
# connect to another MongoDB server altogether
app.config['MONGO_URI'] = 'mongodb://mongo1:27017,mongo2:27017,mongo3:27017/api?replicaSet=techan'
mongo = PyMongo(app, config_prefix='MONGO')

@app.route('/user/<username>', methods=['GET', 'POST'])
def user_profile(username):
    # user = mongo.db.users.find_one_or_404({'_id': username})
    # print(request.method)
    if request.method == 'GET':
        user = mongo.db.api.find_one_or_404({'_id': username})
    elif request.method == 'POST':
        # data in string format and you have to parse into dictionary
        data = request.data
        dataDict = json.loads(data)
        print(dataDict)
        return dataDict
    # return render_template('user.html',
    #     user=user)
    # return {
    #     'service': name,
    #     'ip': addresses,
    #     'tasks': tasks,
    #     'error': ''
    # }
    return "Toto"


if __name__ == "__main__":
    app.run(debug=True)
