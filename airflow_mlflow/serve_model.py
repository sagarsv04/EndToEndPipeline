# airflow_mlflow/serve_model.py
from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

def load_model():
    with open("/opt/airflow/model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = pd.DataFrame(data)
    predictions = model.predict(features)
    return jsonify({'predictions': predictions.tolist()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
