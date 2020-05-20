from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/country/<cnt>")
def country(cnt):
    return render_template("country.html", cnt=cnt)