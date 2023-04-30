from flask import Flask, render_template, session, redirect, url_for, request
import os
import requests
import requests, json
from dotenv import load_dotenv
from datetime import datetime

i = 0

app = Flask(__name__)
load_dotenv()
api = os.getenv("api")
Flask.secret_key = os.getenv("secret_key")


@app.route("/", methods=["POST", "GET"])
def home_page():
    if request.method == "POST":
        city = request.form.get("city")
        statecode = request.form.get("state")
        countrycode = "in"
        session["my_var"] = [city, statecode, countrycode]
        return redirect(url_for("forecast"))
    return render_template("index.html")


@app.route("/forecast", methods=["POST", "GET"])
def forecast():
    global i
    i += 1
    my_var = session.get("my_var", None)
    if my_var is None:
        my_var = ["Chennai"]
    list_of_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={my_var[0]}&appid={api}&units=metric"
    ).json()
    data = {
        "cityname": f"{my_var[0]}",
        "country_code": str(list_of_data["sys"]["country"]),
        "coordinate": str(list_of_data["coord"]["lon"])
        + " "
        + str(list_of_data["coord"]["lat"]),
        "temp": str(list_of_data["main"]["temp"]) + " °C",
        "pressure": str(list_of_data["main"]["pressure"]),
        "humidity": str(list_of_data["main"]["humidity"]),
        "weather": str(list_of_data["weather"][0]["main"]),
        "lastupdate": str(datetime.now()),
    }
    print(data)
    return render_template("weather.html", data=data)


@app.route("/airquality", methods=["POST", "GET"])
def airquality():
    return "Airquality page"


if __name__ == "__main__":
    app.run(debug=True)
