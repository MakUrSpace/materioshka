import os

import boto3
import os
import json
from flask import Flask, jsonify, make_response, request, url_for, send_file, make_response
import awsgi

app = Flask(__name__)


dynamodb_client = boto3.client('dynamodb')


if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )


MATERIOSHKA_TABLE = os.environ['MATERIOSHKA_TABLE']
"""
MATERIOSHKA TABLE SCHEMA:
Primary Key: UserId (uuid)
Sort Keys:
  - ZONE_{zone_id}
  - PROCESS_STUB_{process_id}
"""


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


ZONES = {}


@app.route('/')
def inventory():
    zones = "\n".join([f"""<div class="row">
        <h3>{z['name']}</h3>
        <img src="data:image/jpg;{z['image']}"><br>
        <input type="button" value="Update Zone" onclick="window.location.href='/updatezone/{z['name']}'">
    </div>""" for z in ZONES.values()])
    return render_template('ZoneOverview.html').replace("{zones}", zones)


@app.route('/createzone', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        zoneData = request.get_json()
        ZONES[zoneData['name']] = zoneData
        with open("zones.json", "w") as f:
            f.write(json.dumps(ZONES))
        return "Success"
    else:
        return render_template('CreateZone.html')
        

@app.route('/updatezone/<zonename>', methods=['GET', 'POST'])
def update(zonename):
    if request.method == "POST":
        zoneData = request.get_json()
        zoneData['name'] = zonename
        # Pull active zone into separate image
        ZONES[zonename] = zoneData
        # Call SAM on zone
        with open("zones.json", "w") as f:
            f.write(json.dumps(ZONES))
        return "Success"
    else:
        try:
            zone = ZONES[zonename]
        except KeyError:
            return make_response(f"Zone {zonename} not found", 404)
        return render_template('UpdateZone.html').replace(
            "{zonename}", zone['name']).replace(
            "{zoneimage}", zone['image']).replace(
            "{activezone}", json.dumps(zone['activeZone']))


def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/jpg"})


if __name__ == '__main__':
    try:
        with open("zones.json", "r") as f:
            ZONES = json.loads(f.read())
    except Exception as e:
        print("Failed to load Zones: {e}")
        ZONES = {}
    app.run(debug=True, host="0.0.0.0", ssl_context='adhoc')
