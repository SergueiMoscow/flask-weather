import os
from datetime import datetime
import json

import plotly
from flask import Flask, render_template, request
from weather import Weather

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.route("/")
def main_page():
    return """
    <a href="weather">Погода</a>
    """


@app.route('/weather')
def weather():
    return Weather.render()


@app.route('/search')
def city():
    location_query = request.args.get('q')
    locations = Weather.search_location(location_query)
    location_weather = Weather.get_current_state(locations[0])
    forecast = Weather.get_forecast(locations[0])
    str_json = json.dumps(forecast, sort_keys=True, indent=4)
    with open('forecast.json', 'w') as f:
        f.write(str_json)
    # for show forecast:
    fig = Weather.get_forecast_fig(forecast)
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return {'location': locations[0], 'weather': location_weather, 'forecast': forecast, 'graph_json': graph_json}


@app.route('/forecast')
def get_forecast():
    pass


if __name__ == "__main__":
   app.run(debug=True)
