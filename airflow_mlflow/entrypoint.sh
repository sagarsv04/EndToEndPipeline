#!/bin/bash

# Initialize Airflow DB
airflow db init

# Create an Airflow admin user (you can modify username/password as needed)
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Start Airflow scheduler and webserver
airflow scheduler & airflow webserver -p 8080 &

# Set the MLflow tracking URI to point to the running MLflow server
export MLFLOW_TRACKING_URI="http://localhost:5000"

# # Start MLflow server
# mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000 &

# Start the MLflow tracking server
mlflow ui --host 0.0.0.0 --port 5000 &

# Start Flask API
python /opt/airflow/serve_model.py &

# Start Grafana
service grafana-server start &

# Keep container running
tail -f /dev/null