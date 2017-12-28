import os
import pandas as pd
from flask import Flask, jsonify, request
from task3 import G3Regressor

app = Flask(__name__)
reg = G3Regressor()

@app.route('/predict', methods=['POST'])
def apicall():
    try:
        test_json = request.get_json()
        test = pd.read_json(test_json)
    except Exception as e:
        raise e

    if test.empty:
      return('Bad request')
    else:
        preds = reg.predict(test)
