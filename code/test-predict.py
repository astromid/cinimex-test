import pandas as pd
import json
import requests

test_df = pd.read_csv('test.csv', sep=';')
header = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
json_data = test_df.to_json(orient='records')
resp = requests.post('http://localhost:8080/predict', data=json.dumps(json_data), headers=header)
print(resp.status_code)
print(resp.json())