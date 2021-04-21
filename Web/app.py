from flask import Flask, render_template, jsonify, send_from_directory, request
import json
import pandas as pd
import numpy as np
import os
from modelHelper import ModelHelper
import pickle
#init app and class
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
modelHelper = ModelHelper()

#endpoint
# Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

# Route to render index.html template
@app.route("/")
def home():
    # Return template and data
    return render_template("index.html")

# Route to render index.html template
@app.route("/glossary")
def glossary():
    # Return template and data
    return render_template("glossary.html")

# Route to render index.html template
@app.route("/prediction")
def machine():
    # Return template and data
    return render_template("mLearning.html")

# Route to render index.html template
@app.route("/data")
def data():
    # Return template and data
    return render_template("madnessData.html")

@app.route("/makePredictions", methods=["POST"])
def makePredictions():
    content=request.json["data"]
    print(content["year1"])
    yr1 = int(content["year1"])
    yr2 = int(content["year2"])

    avg_yr1 = pd.read_csv(f'Web/static/data/full_avg_{yr1}.csv')
    gb_yr1 = pickle.load(open(f'Web/static/models/finalized_model_{yr1}.sav', 'rb'))
    avg_yr2 = pd.read_csv(f'Web/static/data/full_avg_{yr2}.csv')
    gb_yr2 = pickle.load(open(f'Web/static/models/finalized_model_{yr2}.sav', 'rb'))
    
    teamA = str(content["team1"])
    teamB = str(content["team2"])

    
    prediction = modelHelper.get_matchup(teamA, yr1, avg_yr1, gb_yr1, teamB, yr2, avg_yr2, gb_yr2)
    print(prediction)
    return(jsonify({"ok": True, "prediction": prediction}))

####################################
# ADD MORE ENDPOINTS
####################################

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

#main
if __name__ == "__main__":
    app.run(debug=True)