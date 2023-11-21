from flask import Flask, request, render_template, redirect, url_for, send_file, make_response
import os
import json


app = Flask(__name__)


# Ensure there's a folder to save uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
        ZONES[zonename] = zoneData
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


if __name__ == '__main__':
    try:
        with open("zones.json", "r") as f:
            ZONES = json.loads(f.read())
    except Exception as e:
        print("Failed to load Zones: {e}")
        ZONES = {}
    app.run(debug=True, host="0.0.0.0", ssl_context='adhoc')
