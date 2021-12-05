from flask import Flask, render_template
from db import Database
import cpu_load
import random
import logging

from db import CPU, Base, EnvironmentTPH


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/device-load")


@app.route("/api/cpu-load")
def get_api_deviceload():
    return {"cpu load": 25}

@app.route("/api/environment")
def get_api_environment():
    current_enviro = get_api_temperature(), get_api_pressure(), get_api_humidity()
    return {"Environment": current_enviro}

@app.route("/api/temperature")
def get_api_temperature():
    current_temp = EnvironmentTPH().temperature
    return {"Temperature": current_temp}

@app.route("/api/pressure")
def get_api_pressure():
    current_pressure = EnvironmentTPH().pressure
    return {"Pressure": current_pressure}

@app.route("/api/humidity")
def get_api_humidity():
    current_humidity = EnvironmentTPH().humidity
    return {"Humidity": current_humidity}

@app.route("/does-not-exist")
def api_does_not_exist():
    return {"Error": "Does not exist"}

@app.route("/api/history")
def temp_history():
    @app.route("/api/ticker")
    def something():
        x=0
        for num in range(1):
            r=random.randint(0,50)
            x=r
        return{"History":x}
    return render_template("Historical_page.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cpu')
def chart_cpu():
    return render_template('chart-cpu.html')


if __name__ == '__main__':
    app.run()
