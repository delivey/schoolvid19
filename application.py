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
    connection = sqlite3.connect('countries.db') # connects to db
    db = connection.cursor() # creates the cursor for db connection
    if request.method == "GET":
        countries = db.execute("SELECT country FROM names").fetchall()
        return render_template("countries.html", countries=countries)
    else:
        search = request.form.get("cName")
        results = db.execute("SELECT country FROM names WHERE country LIKE ?", ('%'+search+'%',)).fetchall()
        connection.commit()
        return render_template("countries.html", results=results)
