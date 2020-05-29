from flask import Flask, redirect, render_template, request
import sqlite3
import csv

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/country/<cnt>")
def country(cnt):
    connection = sqlite3.connect('countries.db') # connects to db
    db = connection.cursor() # creates the cursor for db connection
    status = db.execute("SELECT status FROM stats WHERE name LIKE ?", ('%'+cnt+'%',)).fetchall()[0]
    cases = db.execute("SELECT cases FROM stats WHERE name LIKE ?", ('%'+cnt+'%',)).fetchall()[0]
    connection.commit()
    return render_template("country.html", cnt=cnt, status=status, cases=cases)

@app.route("/countries", methods=["GET", "POST"])
def countries():
    connection = sqlite3.connect('countries.db') # connects to db
    db = connection.cursor() # creates the cursor for db connection
    if request.method == "GET":
        countries = db.execute("SELECT name FROM stats").fetchall()
        return render_template("countries.html", countries=countries)
    else:
        search = request.form.get("cName")
        results = db.execute("SELECT name FROM stats WHERE name LIKE ?", ('%'+search+'%',)).fetchall()
        connection.commit()
        return render_template("countries.html", results=results)

@app.route("/update/cases", methods=["GET"])
def case_updating():
    connection = sqlite3.connect('countries.db') # connects to db
    db = connection.cursor() # creates the cursor for db connection
    with open('WHO-COVID-19-global-data.csv', newline='') as csvFile: # link for file https://covid19.who.int/info
        reader = csv.reader(csvFile)
        for row in reader:
            countryName = row[2]
            countryCases = row[5] # code for updating
            db.execute("UPDATE stats SET cases=(?) WHERE name LIKE (?)", (countryCases, '%'+countryName+'%'))
            connection.commit()
            print(f"Inserting {countryCases}, {countryName}")
        return redirect("/")

@app.route("/update/status", methods=["GET"])
def status_updating():
    connection = sqlite3.connect('countries.db') # connects to db
    db = connection.cursor() # creates the cursor for db connection
    with open('covid_impact_education.csv', newline='') as csvFile: # link for file https://en.unesco.org/covid19/educationresponse
        reader = csv.reader(csvFile)
        for row in reader:
            countryName = row[2]
            countryStatus = row[3] # code for updating
            db.execute("UPDATE stats SET status=(?) WHERE name LIKE (?)", (countryStatus, '%'+countryName+'%'))
            print(f"Updating {countryStatus}, {countryName}")
        return redirect("/")

# available to run if double click the file
if __name__ == "__main__":
    app.run(debug=True)

