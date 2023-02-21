import datetime
import json

import requests
from flask import Flask, jsonify, request

API_TOKEN = ""


app = Flask(__name__)


def generate_weather(location: str, days: int):
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

    params = {"q": location,"days":days}

    headers = {
        "X-RapidAPI-Key": "794f072a4amsh98a3b69b241e388p183e65jsn130236dd8793",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=params)
    return json.loads(response.text)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p><h2>Weather. by Yulia Stoliaruk</h2></p>"


@app.route(
    "/content/api/v1/integration/generate",
    methods=["POST"],
)
def joke_endpoint():
    json_data = request.get_json()

    if json_data.get("token") is None:
        raise InvalidUsage("token is required", status_code=400)

    token = json_data.get("token")

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    location= ""
    if json_data.get("location"):
        location = json_data.get("location")
        
    days= ""
    if json_data.get('days') and int(json_data['days']) > 3:
        raise InvalidUsage("This endpoint is disabled for your subscription", status_code=400)
        
    if json_data.get('days') and int(json_data['days']) < 1:
        raise InvalidUsage("Wrong number", status_code=400)
        
    if json_data.get("days"):
        days = json_data.get("days")


    weather = generate_weather(location, days)

    current_utc_time = datetime.datetime.utcnow()
    formatted_time = current_utc_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    result = {"requester_name":"Yulia Stoliaruk",
         "timestamp": formatted_time,
         "location":location,
         "date":"22.02.2023",
        "weather": weather,
    }

    return result
