from flask import Flask, request, render_template, jsonify
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from weather_forecast import Forecast, error503
from weather_logic import Logic, days
from weather_graphics import Graphics
import os

app = Flask(__name__)


forecast = Forecast()
logic = Logic(None)
graph = Graphics({'error': 'error'})
day = None
data = None


@app.route("/api/weather", methods=["POST"])
def api_weather():
    data = request.get_json()
    cities = data.get("cities")
    day = data.get("day")
    forecast = Forecast()
    for city in cities:
        try:
            forecast.get_data(city)
        except error503:
            res = {'error' : 'Проблема с подключением к серверу.'}
            return jsonify(res)
        except:
            res = {'error' : 'Неправильно введено имя города. Попробуйте написать город на английском.'}
            return jsonify(res)
    all_data = forecast.get_all_data()
    logic = Logic(all_data)
    graph = Graphics(all_data)
    res = {}
    for city in cities:
        color, message = logic.get_res(city, day)
        spec = forecast.get_scpecific(city, day)
        fig = graph.create_linegraph(city,['min_temperature','max_temperature'],'Температра')
        filepath = os.path.join('image', f"{city}.png")
        fig.write_image(filepath)
        res[city] = {'color':color,'message':message,'spec':spec,'img1': f"{city}.png"}
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)