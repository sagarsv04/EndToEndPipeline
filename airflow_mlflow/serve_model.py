from flask import Flask, request, jsonify
import pickle
import os
import pandas as pd

app = Flask(__name__)

MODEL_PATH = "/opt/airflow/model.pkl"

def load_model():
    """Load the model if it exists; otherwise return None."""
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        return model
    else:
        return None

@app.route('/predict', methods=['POST'])
def predict():
    model = load_model()  # Try loading the model before prediction
    if model is None:
        return jsonify({"error": "Model not found. Please run the DAG to train the model first."}), 400
    
    try:
        # Parse the incoming request JSON
        data = request.json
        features = pd.DataFrame(data)
        
        # Make predictions using the loaded model
        predictions = model.predict(features)
        return jsonify({'predictions': predictions.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
