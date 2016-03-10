__author__ = 'hapresto'


from flask import Flask
import socket


app = Flask(__name__)


@app.route('/')
def hello_world():
    sysname = socket.gethostname()

    return 'Hello World! from ' + sysname



if __name__ == '__main__':
    parser = ArgumentParser('Sample Application')
    parser.add_argument(
        '-p', '--port', help='Port to listen on ', required=False, default=5000)
    args = parser.parse_args()
    app.secret_key = '1234'
    port = int(args.port)
    app.run(host='0.0.0.0', port=port, debug=True)
