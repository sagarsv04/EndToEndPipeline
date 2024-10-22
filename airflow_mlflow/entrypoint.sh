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

# Start MLflow server
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000 &

# Start Flask API
python /opt/airflow/serve_model.py &

# Keep container running
tail -f /dev/null