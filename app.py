from flask import Flask, redirect, render_template, request
import sqlite3

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
    else:
        connection = sqlite3.connect('countries.db') # connects to db
        db = connection.cursor() # creates the cursor for db connection

        search = request.form.get("cName")
        result = db.execute("SELECT country FROM names WHERE country=(?)", (search,)).fetchone()[0]
        connection.commit()
        return render_template("countries.html", result=result)