"""
Сервер на Flask, реализующий получение предсказаний, тренировку и удаление модели.
"""
import os
import pandas as pd
from flask import Flask, jsonify, request
from task3 import G3Regressor

app = Flask(__name__)
reg = G3Regressor()


# predict route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        test_json = request.get_json()
        test = pd.read_json(test_json, orient='records')
    except Exception as e:
        raise e

    if test.empty:
        return 'Bad request'
    else:
        preds = reg.predict(test)
        respond = jsonify({'G3': preds.tolist()})
        respond.status_code = 200
        return respond

# route for manual retraining model
@app.route('/train', methods=['GET'])
def train():
    reg.train()
    return 'Model retrained'

# route for wiping pretrained model
@app.route('/delete', methods=['GET'])
def delete():
    reg = G3Regressor()
    os.remove('model.cbm')
    return 'Model wiped'

if __name__ == '__main__':
    app.run(port=8080)
