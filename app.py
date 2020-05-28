from flask import Flask, redirect, render_template, request
import sqlite3
import csv

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/country/<cnt>")
def country(cnt):
    with open('covid_impact_education.csv', newline='') as csvFile: # link for file https://en.unesco.org/covid19/educationresponse
        reader = csv.reader(csvFile)
        next(reader)
        for row in reversed(list(reader)):
            print(row[0])
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
