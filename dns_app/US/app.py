from flask import Flask, abort, request
from socket import *

from urllib.request import urlopen
import json, requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'User Server'

@app.route('/fibonacci', methods=['GET' ])
def get_fab():
    print("start user request")
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not hostname or not fs_port or not number or not as_ip or not as_port:
        print("abort")
        abort(400)

    as_port = int(as_port)
    fs_port = int(fs_port)
    ip_request = {'TYPE': 'A', 'NAME': hostname}
    message = json.dumps(ip_request)

    us_socket = socket(AF_INET, SOCK_DGRAM)
    us_socket.sendto(message.encode(), (as_ip, as_port))
    response, server_address = us_socket.recvfrom(2048)
    ip_address = json.loads(response.decode())
    us_socket.close()

    res = requests.get('http://{}:{}/fibonacci?number={}'.format(ip_address, fs_port, number))

    return res.text, res.status_code

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)
