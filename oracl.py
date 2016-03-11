__author__ = 'hapresto'


from flask import Flask, make_response, request, jsonify, Response
from argparse import ArgumentParser
import json
import os

flask_app = Flask(__name__)

@flask_app.route("/v1/<appid>", methods=["GET", "POST", "DELETE"])
def v1_appid(appid):
    '''
    Basic CRUD operations for an Oracl Application
    :param appid:
    :return:
    '''
    if request.method == "GET":
        app = oracl_app(appid).info
        if "Error" in app:
            status = 404
        else:
            status = 200
    elif request.method == "POST":
        app = oracl_app.new(appid)
        if "Error" in app:
            status=400
        else:
            status = 201
    elif request.method == "DELETE":
        app = oracl_app(appid).delete()
        if "Error" in app:
            status=404
        else:
            status = 202
    return Response(json.dumps(app)+"\n", content_type='application/json',status=status)

@flask_app.route("/v1/<appid>/<datatype>", methods=["GET", "POST", "DELETE"])
def v1_datatype(appid, datatype):
    '''
    Basic CRUD operations for an Oracl Application Data Type
    :param appid:
    :param datatype:
    :return:
    '''
    if request.method == "POST":
        datatype = oracl_datatype.new(appid, datatype)
        if "Error" in datatype:
            status=400
        else:
            status = 201
    elif request.method == "GET":
        datatype = oracl_datatype(appid, datatype).info
        if "Error" in datatype:
            status = 404
        else:
            status = 200
    elif request.method == "DELETE":
        datatype = oracl_datatype(appid, datatype).delete()
        if "Error" in datatype:
            status=404
        else:
            status = 202
    return Response(json.dumps(datatype)+"\n", content_type='application/json',status=status)

@flask_app.route("/v1/<appid>/<datatype>/<element>", methods=["GET", "POST", "DELETE"])
def v1_data(appid, datatype, element):
    '''
    Basic CRUD operations for an Oracl Application Data Type Data Element Object
    :param appid:
    :param datatype:
    :param element:
    :return:
    '''
    # Check for and process submitted data object
    data = request.get_json(force=True)
    print data

    if request.method == "POST":
        element = oracl_element.new(appid, datatype, element, data)
        if "Error" in element:
            status=400
        else:
            status = 201
    elif request.method == "GET":
        # GET defaults to sending the element info only, check request body if element_data is being requested
        if "element_data" in data and data["element_data"] == "True":
            print "return data"
            element = oracl_element(appid, datatype, element).element_data
        else:
            element = oracl_element(appid, datatype, element).info
        if "Error" in element:
            status = 404
        else:
            status = 200
    elif request.method == "DELETE":
        element = oracl_element(appid, datatype, element).delete()
        if "Error" in element:
            status=404
        else:
            status = 202
    return Response(json.dumps(element)+"\n", content_type='application/json',status=status)

# Todo - Add support for working with element_data: /v1/<appid>/<datatype>/<element>/<element_data_key>
# Todo - Add support for working with element_data: /v1/<appid>/<datatype>/<element>/<element_data_key>/<element_data_subkey>

if __name__ == '__main__':
    parser = ArgumentParser('Oracl Simple Data Service')
    parser.add_argument(
        '-d', '--datadir', help='Data Directory', required=False, default="data")
    parser.add_argument(
        '-p', '--port', help='Port to listen on', required=False, default=80)
    args = parser.parse_args()
    flask_app.secret_key = '1234'

    # Set data directory for server and save to environment variable
    os.environ["oracl_datadir"] = args.datadir

    # Import the Oracl Modules
    from oracl_app import oracl_app
    from oracl_datatype import oracl_datatype
    from oracl_element import oracl_element

    # Start the Oracl Server
    flask_app.run(host='0.0.0.0', port=args.port, debug=True)
