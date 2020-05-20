from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/country/<cnt>")
def country(cnt):
    return render_template("country.html", cnt=cnt)

@app.route("/countries", methods=["GET", "POST"])
def countries():
    if request.method == "GET":
        return render_template("countries.html")