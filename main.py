from src.api.maesk import maesk_get_location, maesk_get_ship_price
from user_secrets import bearer_token, akamai_telemetry
from flask import Flask, jsonify, request
from flask_cors import CORS
from time import sleep

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def welcome():
    return jsonify({'status': 'welcome'})


@app.route("/search", methods=['POST'])
def search():

    json_input = request.get_json()
    _from = maesk_get_location(json_input['from'])
    sleep(.5)
    _to = maesk_get_location(json_input['to'])

    data = maesk_get_ship_price(
        bearer_token=bearer_token, 
        akamai_telemetry=akamai_telemetry,
        from_name=_from['city'],
        from_geoid=_from["maerskGeoLocationId"],
        to_name=_to['city'],
        to_geoid=_to["maerskGeoLocationId"],
        commodity=json_input['commodity'],
        send_date=json_input['date']
    )

    return jsonify(data)

if __name__ == "__main__":
    app.run()
