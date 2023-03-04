from flask import Flask, jsonify, request, render_template
import pandas as pd
import json
from joblib import load
import numpy as np


model = load(r"mod.joblib")

app = Flask(__name__)

X_test = pd.read_csv(r"app_test.csv", index_col='SK_ID_CURR')

X_test_prepro = pd.read_csv(r"app_test_tr.csv", index_col='SK_ID_CURR')


@app.route("/")
def index():
    return "Bonjour, bienvenue dans mon API"


@app.route('/id_sk')
def sk_ids():

    sk_ids = pd.Series(list(X_test.index.sort_values()))

    sk_ids_json = json.loads(sk_ids.to_json())

    return jsonify({'data': sk_ids_json})


@app.route('/scoring_cust/', methods=["GET", "POST"])
def scoring_cust():

    sk_id_cust = request.form.get('SK_ID_CURR')

    X_cust = X_test_prepro.loc[sk_id_cust:sk_id_cust]

    score_cust = 100 - 100 * model.predict_proba(X_cust)[:, 1][0]

    prediction = np.where(score_cust >= 90, "Solvable", "Non Solvable")

    return render_template('index.html',
                           prediction_text=f'Le score du client numéro {sk_id_cust} est de {round(score_cust,0)} , il est donc {prediction}.')


@app.route('/score/')
def score():

    sk_id_cust = request.args.get('SK_ID_CURR')

    X_cust = X_test_prepro.loc[sk_id_cust:sk_id_cust]

    score_cust = 100 - 100*model.predict_proba(X_cust)[:, 1][0]

    return jsonify({
        'SK_ID_CURR': (sk_id_cust),
        'score': score_cust,
    })


if __name__ == "__main__":
    app.run(debug=True)






