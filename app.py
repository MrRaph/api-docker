from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from dns import resolver

app = FlaskAPI(__name__)


@app.route("/docker/service/<string:name>/ip", methods=['GET'])
def service_ip(name):
    """
    Retrieve service vip.
    """
    res = resolver.Resolver()
    res.nameservers = ['127.0.0.11']
    res.timeout = 1
    res.lifetime = 1

    addresses,tasks = [], []

    try:
        answers = res.query(name)
        for rdata in answers:
            addresses.append(rdata.address)

    except:
        return {
            'service': name,
            'ip': "",
            'tasks': '',
            'error': 'Probleme lors de la resolution de ' + name
        }

    try:
        answers = res.query('tasks.' + name)
        for rdata in answers:
            tasks.append(rdata.address)

    except:
        return {
            'service': name,
            'ip': addresses,
            'tasks': '',
            'error': 'Probleme lors de la resolution de tasks.' + name
        }

    return {
        'service': name,
        'ip': addresses,
        'tasks': tasks,
        'error': ''
    }

@app.route("/docker/service/<string:name>/tasks/ip", methods=['GET'])
def service_tasks_ip(name):
    """
    Retrieve service tasks ips.
    """
    res = resolver.Resolver()
    # res.nameservers = ['127.0.0.11']
    res.timeout = 1
    res.lifetime = 1

    tasks = [], []

    try:
        answers = res.query('tasks.' + name)
        for rdata in answers:
            tasks.append(rdata.address)

    except:
        return {
            'service': name,
            'tasks': '',
            'error': 'Probleme lors de la resolution de tasks.' + name
        }

    return {
        'service': name,
        'tasks': tasks,
        'error': ''
    }

if __name__ == "__main__":
    app.run(debug=True)
