from flask import Flask, abort
from flask import request
import socket, json

app2 = Flask(__name__)


def fib(x):
    if x == 0:
        return 0
    elif x == 1 or x == 2:
        return 1
    else:
        return fib(x - 1) + fib(x - 2)

@app2.route('/')
def hello_world():
    return 'Fib Server'

@app2.route('/fibonacci')
def get_fib():
    x = request.args.get('number')
    if x.isnumeric():
        return str(fib(int(x))), 200
    else:
        abort(400)

@app2.route('/register', methods=['PUT'])
def register():
    hostname = request.args.get('hostname')
    myIp = request.args.get('ip')
    as_ip = request.args.get('as_ip')
    as_port = int(request.args.get('as_port'))

    payload = {
        "TYPE": "A",
        "NAME": hostname,
        "VALUE": myIp,
        "TTL": 10
    }

    payload = json.dumps(payload)
    print(" request to register sent")
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(payload.encode(), (as_ip, as_port))
    message, addr = client.recvfrom(2048)
    message = message.decode()

    if message == '201':
        return "Registration with AS successfull", 201
    else:
        abort(500)

if __name__ == "__main__":
    app2.run(host='0.0.0.0',
            port=9090,
            debug=True)
